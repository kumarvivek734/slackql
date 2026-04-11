from app.db.connection import get_connection
from sqlalchemy import text
from collections import defaultdict

def get_schema_context():
    try:
        with get_connection() as conn:
            query = '''SELECT table_name, column_name, data_type 
                    FROM information_schema.columns 
                    WHERE table_schema = 'public' 
                    ORDER BY table_name, ordinal_position'''
            result = conn.execute(text(query))
            rows = [dict(row._mapping) for row in result]
            
        tables = defaultdict(list)
            
        for row in rows:
            tables[row["table_name"]].append(f" - {row['column_name']} ({row['data_type']})")
        
        schema_str=""
        for table_name, columns in tables.items():
            schema_str += f"Table: {table_name}\n"
            schema_str += "\n".join(columns) + "\n\n"
            
        return schema_str
            
    except Exception as e:
        return {"error": f"Error occured: {e}"}
        