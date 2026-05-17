from pathlib import Path
import tomllib
import pyspark
from pyspark.sql import SparkSession

import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
namespace = "local.db"

def load_config(path: str = "config.toml") -> dict:
    with open(path, "rb") as f:
        return tomllib.load(f)


def build_spark_conf(cfg: dict) -> pyspark.SparkConf:
    conf = pyspark.SparkConf()

    conf.setAppName(cfg["app"]["name"])

    conf.set(
        "spark.jars.packages",
        cfg["spark"]["packages"]["iceberg"]
    )

    conf.set(
        "spark.driver.host",
        cfg["spark"]["driver_host"]
    )

    conf.set(
        "spark.driver.memory",
        cfg["spark"]["driver_memory"]
    )

    conf.set(
        "spark.sql.extensions",
        cfg["spark"]["sql"]["extensions"]
    )

    conf.set(
        "spark.sql.catalog.local",
        cfg["spark"]["catalog"]["local"]["catalog_impl"]
    )

    conf.set(
        "spark.sql.catalog.local.type",
        cfg["spark"]["catalog"]["local"]["type"]
    )

    conf.set(
        "spark.sql.catalog.local.warehouse",
        cfg["spark"]["catalog"]["local"]["warehouse"]
    )

    conf.set(
        "spark.namespace",
        cfg["spark"]["catalog"]["local"]["namespace"]
    )

    conf.set(
        "spark.sql.catalog.spark_catalog.type",
        cfg["spark"]["catalog"]["spark_catalog"]["type"]
    )

    return conf

def init():
    # Start Spark Session
    cfg = load_config("agents/config.toml")
    conf = build_spark_conf(cfg)
    namespace = conf.get("spark.namespace")
    spark = SparkSession.builder.config(conf=conf).getOrCreate()
    print("== Spark Running ==")
    return spark

def nosql_db_list_tables():
    """list tables in the database"""
    try:
        tables = spark.sql(f"SHOW TABLES IN {namespace}").collect()
        return [row['tableName'] for row in tables]
    except Exception as e:
        logger.error(f"Error listing tables: {e}")
        return []

def nosql_db_schema(table_name):
    """schema of table in DB"""
    try:
        schema_info = spark.sql(f"DESCRIBE TABLE {namespace}.{table_name}").collect()
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
        spark.sql(f"USE {namespace}")
        print("========query========", query)
        results = spark.sql(query).collect()
        return '\n'.join(str(row) for row in results)
    except Exception as e:
        logger.error(f"Query execution error: {e}")
        return "Error executing query."

spark = init()
nosql_db_list_tables()
