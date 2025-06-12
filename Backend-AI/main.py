from fastapi import FastAPI, Request
from pydantic import BaseModel
from Backend-AI.utils import get_db_connection, get_schema_info, generate_sql, execute_sql

app = FastAPI()

class PromptInput(BaseModel):
    question: str

@app.post("/query")
def query_data(data: PromptInput):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        schema_info = get_schema_info(cursor)
        sql = generate_sql(data.question, schema_info)
        print("Generated SQL:", sql)

        results = execute_sql(sql, cursor)
        return {"success": True, "query": sql, "results": results}
    
    except Exception as e:
        return {"success": False, "error": str(e)}
    
    finally:
        cursor.close()
        conn.close()
