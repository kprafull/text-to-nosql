from openai import OpenAI
import agents.iceberg_agent as ia
import ui.util as util
import json
import re

tools = [
    {
        "type": "function",
        "function": {
            "name": "nosql_db_list_tables",
            "description": "Lists the tables in the database",
            "parameters": {
            }
        },
    },
    {
        "type": "function",
        "function": {
            "name": "nosql_db_schema",
            "description": "Fetch the schmea of a given table",
            "parameters": {
                "type": "object",
                "properties": {
                    "name": {
                        "type": "string",
                        "description": "The name of table"
                    }
                },
                "required": ["name"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "nosql_db_query_checker",
            "description": "Checks the given SQL query corretness before execution",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "The sql query"
                    }
                },
                "required": ["query"]
            }
        },
    },
    {
        "type": "function",
        "function": {
            "name": "nosql_db_query",
            "description": "runs the given SQL query",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "The sql query"
                    }
                },
                "required": ["query"]
            }
        },
    },
]

def invoke_tools(response):
    # Check if OpenAI requests tool execution
    tool_calls = response.choices[0].message.tool_calls if response.choices[0].message.tool_calls else []

    print('====Tools=====', tool_calls)

    tool_responses = []  # Store tool responses

    for tool_call in tool_calls:
        print('====Tool=====', tool_call)
        function_name = tool_call.function.name
        arguments = json.loads(tool_call.function.arguments)

        # Execute the appropriate function
        if function_name == "nosql_db_list_tables":
            result = ia.nosql_db_list_tables()
        elif function_name == "nosql_db_schema":
            result = ia.nosql_db_schema(arguments["name"])
        elif function_name == "nosql_db_query_checker":
            result = ia.nosql_db_query_checker(arguments["query"])
        elif function_name == "nosql_db_query":
            result = ia.nosql_db_query(arguments["query"])

        # Store tool response
        tool_responses.append(
            {
                "role": "tool",
                "name": function_name,
                "tool_call_id": tool_call.id,
                "content": json.dumps(result)
            }
        )
    print('====Tool Response=====', tool_responses)
    return tool_responses

def call_llm_chain(api_key, user_prompt,  debug_mode=False):
    prompt = f"""
    User: Answer the following questions as best you can. You have access to the following tools:

    nosql_db_query - Input to this tool is a detailed and correct Apache Iceberg SQL query, output is a result from the database.
    If the query is not correct, an error message will be returned. If an error is returned, rewrite the query,
    check the query, and try again. If you encounter an issue with Unknown column 'xxxx' in 'field list',
    use nosql_db_schema to query the correct table fields.

    nosql_db_schema - Input to this tool is a comma-separated list of tables, output is the schema and sample
    rows for those tables. Be sure that the tables actually exist by calling nosql_db_list_tables first!
    Example Input: table1, table2, table3

    nosql_db_list_tables - Input is an empty string, output is a comma-separated list of tables in the database.

    nosql_db_query_checker - Use this tool to double check if your query is correct before executing it. Always
    use this tool before executing a query with nosql_db_query!

    Use the following format:

    Question: the input question you must answer
    Thought: you should always think about what to do
    Action: the action to take, should be one of [nosql_db_query, nosql_db_schema, nosql_db_list_tables, nosql_db_query_checker]
    Action Input: the input to the action
    Observation: the result of the action
    ... (this Thought/Action/Action Input/Observation can repeat N times)
    Thought: I now know the final answer
    Final Answer: the final answer to the original input question

    Begin!

    Question: {user_prompt}
    Thought:
    """

    messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {
                "role": "user",
                "content": prompt
            }
        ]
    return call_llm(api_key, messages, debug_mode)

def call_llm(api_key, messages, debug_mode):
    # call LLM
    client = OpenAI(api_key=api_key)
    print('====LLM Request=====', messages)
    response = client.chat.completions.create(
        # model="gpt-4-turbo",
        model="gpt-4o-mini",
        messages=messages,
        tools = tools
    )
    print('====LLM Response=====', response)
    print('====LLM Response Message=====', response.choices[0].message)

    #Invoke tools
    if response.choices[0].message.tool_calls:
        tool_responses = invoke_tools(response)
        # print(messages + [response.choices[0].message] + tool_responses)
        # append response to chat
        arguments = json.loads(response.choices[0].message.tool_calls[0].function.arguments)
        if(debug_mode):
            util.add_chat_message("debug", f"Running tool {response.choices[0].message.tool_calls[0].function.name} with parameters {arguments}")
        return call_llm(api_key, messages + [response.choices[0].message] + tool_responses, debug_mode)
    else:
        # call_python_llm(api_key, response.choices[0].message.content)
        return response.choices[0].message.content

def call_python_llm(api_key, sql_response):
    """
    Create an agent for Python-related tasks.

    Args:
        agent_llm_name (str): The name or identifier of the language model for the agent.
    Returns:
        AgentExecutor: An agent executor configured for Python-related tasks.
    """
    instructions = """You are an agent designed to write python code to answer questions.
            You have access to a python REPL, which you can use to execute python code.
            If you get an error, debug your code and try again.
            You might know the answer without running any code, but you should still run the code to get the answer.
            If it does not seem like you can write code to answer the question, just return "I don't know" as the answer.
            Always output the python code only.
            Generate the code <code> for plotting the previous data in plotly, in the format requested. 
            The solution should be given using plotly and only plotly. Do not use matplotlib.
            The chart will be displayed in the streamlit app, so instead of diplaying generated figure using fig.show(),
            please use st.plotly_chart(fig, key="unique_key") and generate the unique_key as UUID.
            format <code>
            format ```python <code>```
            """
    print("===========>>", instructions)
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {
            "role": "user",
            "content": instructions + sql_response
        }
    ]

    client = OpenAI(api_key=api_key)
    print('====LLM Request=====', messages)
    response = client.chat.completions.create(
        # model="gpt-4-turbo",
        model="gpt-4o-mini",
        messages=messages,
        # tools = tools
    )

    print(response)
    response_content = response.choices[0].message.content
    print(response_content)
    # Remove Markdown code block markers
    cleaned_code = re.sub(r"```(?:python)?\n(.*?)\n```", r"\1", response_content, flags=re.DOTALL).strip()
    print(cleaned_code)
    return cleaned_code
