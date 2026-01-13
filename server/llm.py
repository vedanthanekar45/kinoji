from typing import List
from fastapi import HTTPException
from pydantic import BaseModel
from groq import Groq
import os
import sqlalchemy
from dotenv import load_dotenv

load_dotenv()


# Models for return type
class InsightRequest(BaseModel):
    query: str

class ChartData(BaseModel):
    title: str
    chart_type: str # 'bar', 'line', 'pie'
    labels: List[str]
    data: List[float]
    summary: str


# Getting the LLM and DB
client = Groq(api_key=os.getenv("GROQ_API"))
AI_DB_URL = os.getenv("AI_DB_URL")
engine = sqlalchemy.create_engine(AI_DB_URL)



SYSTEM_PROMPT = """
You are a PostgreSQL expert. Given a natural language question, return ONLY a valid SQL query.
Do not wrap it in markdown. Do not explain. Just the SQL.

The Schema:
- Table: movies (id, name, release, rating, runtime)
- Table: genres (id, genre_name)
- Table: movie_genres (movie_id, genre_id) - Bridge table
- Table: studios (id, studio_name)
- Table: movie_studios (movie_id, studio_id) - Bridge table
- Table: actors (id, name, gender)
- Table: movie_actors (movie_id, actor_id) - Bridge table
- Table: countries (id, country_name, iso_3166_1)
- Table: movie_countries (movie_id, country_id) - Bridge table
- Table: directors (id, director_name)
- Table: movie_directors (movie_id, director_id) - Bridge table
- Table: languages (id, name, iso_639_1)
- Table: movie_languages (movie_id, language_id) - Bridge table

Rules:
1. Use ILIKE for text search.
2. Limit results to 20 rows if selecting list data.
3. If aggregating by year, use EXTRACT(YEAR FROM release_date).

CRITICAL CHARTING RULES:
1. If the user asks for a comparison, trend, or count (aggregation), you MUST return exactly two columns.
2. Alias the X-Axis column (e.g. Year, Genre, Studio) as 'label'.
3. Alias the Y-Axis column (e.g. Count, Average) as 'value'.
4. Example: SELECT name AS label, count(*) AS value FROM ...
"""


def get_insight (request: InsightRequest):
    try:
        chat_completion = client.chat.completions.create(
            messages = [
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": request.query}
            ],
            model="meta-llama/llama-4-scout-17b-16e-instruct",
            temperature=0.1,
        )

        generated_sql = chat_completion.choices[0].message.content.strip()

        generated_sql = generated_sql.replace("```sql", "").replace("```", "")

        with engine.connect() as connection:
            result = connection.execute(sqlalchemy.text(generated_sql))
            data = [dict(row._mapping) for row in result]

        chart_type = "list"
        summary = "No data found to summarize."

        if data:
            keys = data[0].keys()
            
            if "label" in keys and "value" in keys:
                first_label = str(data[0]['label'])
                if first_label.isdigit() and int(float(first_label)) > 1900:
                    chart_type = "line"
                else:
                    chart_type = "bar"
            
            elif len(data) == 1 and len(keys) == 1:
                chart_type = "pie"

        data_str = str(data[:20]) 
            
        SUMMARY_PROMPT = f"""
        You are a Data Analyst. 
        The user asked: "{request.query}"
        The database returned this data: {data_str}
            
        Task: Write a ONE sentence summary of the most interesting trend or fact in this data.
        Do not mention "the data shows". Just state the fact.
        Example: "Action movies peaked in popularity in 2018 with 45 releases."
        """

        summary_completion = client.chat.completions.create(
            messages=[{"role": "user", "content": SUMMARY_PROMPT}],
            model="meta-llama/llama-4-scout-17b-16e-instruct",
            temperature=0.5
        )
        summary = summary_completion.choices[0].message.content.strip()

        return {
            "sql": generated_sql,
            "data": data,
            "type": chart_type,
            "summary": summary
        }
    
    except Exception as e:
        print(f"AI Error: {e}") 
        raise HTTPException(status_code=400, detail="Could not generate insight.")