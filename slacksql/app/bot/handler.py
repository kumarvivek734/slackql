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
            msg = f"*Query:* `{sql_generated}`\n"
            msg += f"*Results:* {query_output['row_count']} rows ({query_output['execution_time_ms']}ms)\n\n"
            for row in query_output["rows"]:
                msg += " | ".join(str(v) for v in row.values()) + "\n"
            say(msg)
    except Exception as e:
        say(f"Something went wrong: {e}")
               