import pyspark
from pyspark.sql import SparkSession

def init():
    conf = (
        pyspark.SparkConf()
            .setAppName('app_name')
        # first we will define the packages that we need. Iceberg Spark runtime
            #.set('spark.jars.packages', 'org.apache.iceberg:iceberg-spark-runtime-3.5_2.12:1.7.1')
            .set('spark.jars.packages', 'org.apache.iceberg:iceberg-spark-runtime-3.5_2.12:1.8.1')
            .set("spark.driver.host", "127.0.0.1")
            .set("spark.driver.memory", "4g")
        # This property allows us to add any extensions that we want to use
            .set('spark.sql.extensions', 'org.apache.iceberg.spark.extensions.IcebergSparkSessionExtensions')
        # configures a new catalog to a particular implementation of SparkCatalog
            .set('spark.sql.catalog.local', 'org.apache.iceberg.spark.SparkCatalog')
        # particular type of catalog we are using
            .set('spark.sql.catalog.local.type', 'hadoop')
        # engine writes to the warehouse
            .set('spark.sql.catalog.local.warehouse', '/Users/kumprafu/spark-3.5.4-bin-hadoop3/spark-warehouse')
        # changes IO impl of catalog, mainly for changing writing data to object storage
            .set('spark.sql.catalog.spark_catalog.type', 'hive')
    )

    # Start Spark Session
    spark = SparkSession.builder.config(conf=conf).getOrCreate()
    print("== Spark Running ==")
    return spark

def nosql_db_list_tables():
    """list tables in the database"""
    try:
        tables = spark.sql("SHOW TABLES IN local.db").collect()
        return [row['tableName'] for row in tables]
    except Exception as e:
        logger.error(f"Error listing tables: {e}")
        return []

def nosql_db_schema(table_name):
    """schema of table in DB"""
    try:
        schema_info = spark.sql(f"DESCRIBE TABLE local.db.{table_name}").collect()
        return '\n'.join(str(row) for row in schema_info)
    except Exception as e:
        logger.error(f"Error fetching schema for {table_name}: {e}")
        return "Schema information unavailable."

def nosql_db_query_checker(query):
    try:
        spark.sql(f"EXPLAIN {query}")
        return True
    except Exception:
        return False

def nosql_db_query(query):
    """Execute query"""
    try:
        spark.sql("USE local.db")
        print("========query========", query)
        results = spark.sql(query).collect()
        return '\n'.join(str(row) for row in results)
    except Exception as e:
        logger.error(f"Query execution error: {e}")
        return "Error executing query."

spark = init()
nosql_db_list_tables()
