import pyodbc
import json
from .config import DB_CONFIG, GENAI_API_KEY
from google import genai

def get_db_connection():
    conn_str = (
        f"DRIVER={DB_CONFIG['driver']};"
        f"SERVER={DB_CONFIG['server']};"
        f"DATABASE={DB_CONFIG['database']};"
        f"UID={DB_CONFIG['username']};"
        f"PWD={DB_CONFIG['password']}"
    )
    return pyodbc.connect(conn_str)

def get_schema_info(cursor):
    schema_info = {}
    cursor.execute("""
        SELECT TABLE_SCHEMA, TABLE_NAME 
        FROM INFORMATION_SCHEMA.TABLES 
        WHERE TABLE_TYPE = 'BASE TABLE'
    """)
    tables = cursor.fetchall()

    for schema, table in tables:
        cursor.execute("""
            SELECT COLUMN_NAME, DATA_TYPE 
            FROM INFORMATION_SCHEMA.COLUMNS 
            WHERE TABLE_SCHEMA = ? AND TABLE_NAME = ?
        """, (schema, table))
        
        columns = cursor.fetchall()
        schema_info[f"{schema}.{table}"] = [
            {"name": col[0], "type": col[1]} for col in columns
        ]

    return schema_info

def generate_sql(query: str, schema_info: dict) -> str:
    genai_client = genai.Client(api_key=GENAI_API_KEY)

    prompt = f"""Here is the database schema in JSON format:

{json.dumps(schema_info, indent=2)}

Based on this schema, write ONLY a SQL query to answer this question:
"{query}"
"""

    response = genai_client.models.generate_content(
        model="gemini-2.0-flash",
        contents=prompt
    )
    
    return response.text.strip().removeprefix("```sql").removesuffix("```")

def execute_sql(sql: str, cursor):
    cursor.execute(sql)
    columns = [col[0] for col in cursor.description]
    rows = cursor.fetchall()
    return [dict(zip(columns, row)) for row in rows]
