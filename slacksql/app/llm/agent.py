from google import genai
from app.config import settings
from app.llm.schema import get_schema_context

def generate_sql(user_question: str):
    try:
        schema = get_schema_context()
        client = genai.Client(api_key=settings.GEMINI_API_KEY.get_secret_value())
        system_prompt = f'''
            You are SQL expert. Given a database schema and a user's question, generate a PostgreSQL SELECT query.
            Here is the database schema {schema}.
            # Context About This Database
                - When listing or ranking customers, always SELECT both customer_id AND company_name (or customer name column) for clarity.
                - "Revenue", "order value", "sales", and "total sales" all mean the same thing.
                - "Month-wise" means group by month using TO_CHAR(date_column, 'FMMonth YYYY') and order chronologically
                - "Week-wise" means group by ISO week using TO_CHAR(date_column, 'IYYY-IW') and order chronologically.
                - For time-based results (dates, months, weeks), always order chronologically ascending
                - For "top N" or "ranking" queries, order DESC by the metric being ranked
                - For all other queries, choose the most intuitive order for the question
            # Rules:
                - Return ONLY the raw SQL query, nothing else.
                - No explanations, no markdown, no code blocks.
                - Do not answer any personal questions. 
                - Do not create DML queries.
                - Do not answer subjective questions.
        '''

        response = client.models.generate_content(
            model=settings.GEMINI_MODEL,
            contents=user_question,
            config=genai.types.GenerateContentConfig(
                system_instruction=system_prompt,
                max_output_tokens=1024,
                thinking_config=genai.types.ThinkingConfig(thinking_budget=0),
            )
        )
        print(f"Response text: {response.text}", flush=True)
        parts = response.candidates[0].content.parts
        # if parts:
        #     result = parts[0].text.strip()
        # else:
        #     return {"error": "Model returned empty response"}
        result = response.text.strip()
        return result
    except Exception as e:
        return {"error": f"Error occured: {e}"}
    