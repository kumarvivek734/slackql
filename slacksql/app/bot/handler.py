from app.llm.agent import generate_sql
from app.db.executor import execute_query

def handle_ask_command(ack, command, say):
    try:
        ack()
        if not command.get("text"):
            say("Please type a question")
            return
        else:
            say("Thinking...")
            user_question = command["text"]
            sql_generated = generate_sql(user_question)
            if isinstance(sql_generated, dict) and "error" in sql_generated:
                say(f"Error: {sql_generated['error']}")
                return
            query_output = execute_query(sql_generated)
            if "error" in query_output:
                say(f"Error: {query_output['error']}")
                return
            rows = query_output.get("rows", [])
            msg = f"*Query:*\n```\n{sql_generated}\n```\n"
            msg += f"*Results:* {len(rows)} rows ({query_output.get('execution_time_ms', 0)}ms)\n\n"

            if rows:
                columns = list(rows[0].keys())
                # Calculate column widths based on header + all values
                col_widths = {
                    col: max(len(col), max(len(str(r[col])) for r in rows))
                    for col in columns
                }
                
                # Build header row
                header = " | ".join(col.ljust(col_widths[col]) for col in columns)
                separator = "-+-".join("-" * col_widths[col] for col in columns)
                
                msg += "```\n"
                msg += header + "\n"
                msg += separator + "\n"
                for row in rows:
                    msg += " | ".join(str(row[col]).ljust(col_widths[col]) for col in columns) + "\n"
                msg += "```"
            else:
                msg += "_No rows returned._"

            say(msg)
    except Exception as e:
        say(f"Something went wrong: {e}")
               