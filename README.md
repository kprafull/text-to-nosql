# NOSQL and Python Agent
This agent can help you with NOSQL queries and Python code for data analysis. Configure your Iceberg database connection.

# **text-to-nosql**  

**text-to-nosql** is a **Streamlit-based web application** that enables users to query NoSQL databases (such as **Apache Iceberg, Apache Hudi, and Delta Lake**) using **natural language**. Powered by **Large Language Models (LLMs)**, this app translates human-readable text into executable database queries, making NoSQL interactions seamless and intuitive.  

## **Features**  

✅ **Natural Language Querying** – Ask questions in plain English, and the LLM agent generates the appropriate NoSQL queries.  
✅ **Multi-Database Support** – Works with **Apache Iceberg, Apache Hudi, and Delta Lake**.  
✅ **Streamlit UI** – Interactive web interface for querying and visualizing results.  
✅ **LLM-Powered Automation** – Uses advanced AI models to generate accurate queries.  
✅ **Extensible Architecture** – Can be adapted for other databases or enhanced with additional features.  

---

## **Installation**  

### **1. Clone the Repository**  

```bash
git clone https://github.com/kprafull/text-to-nosql.git
cd text-to-nosql
```

### **2. Set Up a Virtual Environment (Recommended)**  

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows, use 'env\Scripts\activate'
```

### **3. Install Dependencies**  

```bash
pip install -r requirements.txt
```

---

## **Usage**  

### **Run the Streamlit App**  

```bash
streamlit run app.py
```

This will start the web application, and you can access it in your browser at:  
👉 **http://localhost:8501**  

---

## **How It Works**  

1. **Enter a query in natural language** (e.g., *"Show me the last 10 entries from the orders table."*)  
2. **LLM processes the input** and converts it into an optimized NoSQL query.  
3. **Query executes against the selected database** (Iceberg, Hudi, or Delta Lake).  
4. **Results are displayed in the Streamlit interface**.  

---

## **Architecture Diagram**  
![Home Page](https://github.com/kprafull/text-to-nosql/blob/main/src/media/arch.png)

---

## **Example Queries**  

✔️ *"Get all tables from the database."*  
✔️ *"Find all the trips made."*  
✔️ *"Graph all the trips and break them by payment mode."*  

---

## Sample UI Screenshots

### Home Page
![Home Page](https://github.com/kprafull/text-to-nosql/blob/main/src/media/tables.png)

### Query View
![Query View](https://github.com/kprafull/text-to-nosql/blob/main/src/media/trips.png)

### Graph View
![Graph View](https://github.com/kprafull/text-to-nosql/blob/main/src/media/graph.png)

---

## **Contributing**  

We welcome contributions! Follow these steps:  

1. **Fork the Repository**.  
2. **Create a New Branch**:  

   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **Implement Your Feature or Bug Fix**.  
4. **Commit Your Changes**:  

   ```bash
   git commit -m "Description of your changes"
   ```

5. **Push to Your Fork**:  

   ```bash
   git push origin feature/your-feature-name
   ```

6. **Create a Pull Request**.  

---

## **Acknowledgements**  

💡 Thanks to the open-source community for their support!  
🙏 This project utilizes **Streamlit, OpenAI/LLMs, and NoSQL connectors** for seamless interaction.  

---

🚀 *Ready to simplify NoSQL querying? Fire up the app and start exploring your data today!* 🚀

