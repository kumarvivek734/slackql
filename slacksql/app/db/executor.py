import time
from sqlalchemy import text
from app.config import settings
from app.db.connection import get_connection


def execute_query(sql:str):
    dml_keywords = ['INSERT', 'UPDATE', 'DELETE', 'DROP', 'ALTER', 'CREATE', 'TRUNCATE', 'GRANT', 'EXECUTE']
    try:
        sql = sql.strip()
        sql = sql.rstrip(";")
        clean_sql = sql.upper()
        if not clean_sql.startswith("SELECT"):
            return {"error": "Only SELECT queries are allowed"}
        for keyword in dml_keywords:
            if keyword in clean_sql:
                return {"error": f"Forbidden keyword: {keyword}"}
            
        start_time = time.time()
        with get_connection() as conn:
            wrapped_sql = f"SELECT * FROM ({sql}) AS limited_result LIMIT {settings.DB_MAX_ROWS}"
            result = conn.execute(text(wrapped_sql))
            rows = [dict(row._mapping) for row in result]
            
        end_time = time.time()
        
        return {
            "columns": list(rows[0].keys()) if rows else [],
            "rows": rows,
            "row_count": len(rows),
            "execution_time_ms": round((end_time - start_time) * 1000, 2)
        } 
        
    except Exception as e:
        return {"error": f"Could not complete the query: {e}"}
    