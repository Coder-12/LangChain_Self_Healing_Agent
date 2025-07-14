from langchain_community.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

import traceback
from agent.config import OPENAI_API_KEY, MODEL_NAME, SCHEMA_DESCRIPTION, MAX_RETRIES
from agent.logger import log_attempt


import pandas as pd

def get_schema_string(schema_dict: dict) -> str:
    return "\n".join([f"- {col}: {desc}" for col, desc in schema_dict.items()])

def build_prompt(query: str) -> str:
    schema_str = get_schema_string(SCHEMA_DESCRIPTION)
    return f"""
You are a pandas expert.

Here is the schema:
{schema_str}

User query:
"{query}"

Write Python pandas code to answer the query. 
Return only the exact query code by importing pandas without creating any your own table and use `df` as DataFrame object. 
Store the final result in a variable named `result`. Always converts the result to `DataFrame`. No explanation needed.
    """.strip()

def get_llm_chain():
    prompt = PromptTemplate(
        input_variables=["query"],
        template="{query}"
    )
    llm = ChatOpenAI(
        api_key=OPENAI_API_KEY,
        model=MODEL_NAME,
        temperature=0.1
    )
    return LLMChain(llm=llm, prompt=prompt)


def run_code(code: str, df: pd.DataFrame):
    local_vars = {"df": df.copy()}
    print(f"At run_code {code}")
    try:
        exec(code, {}, local_vars)
        return local_vars
    except Exception as e:
        raise e

def run_with_retry(query: str, df: pd.DataFrame):
    error = ""
    attempts = []

    for attempt in range(1, MAX_RETRIES + 1):
        if attempt == 1:
            prompt = build_prompt(query)
        else:
            prompt = f"""
            You wrote incorrect pandas code for the following query:
            "{query}"
            
            Here was the error:
            {error}
            
            Correct your code. Return only Python pandas code, no explanation.
            Here is the schema:
            {get_schema_string(SCHEMA_DESCRIPTION)}
            """.strip()

        # Generate the code
        code = get_llm_chain().run(query=prompt).strip()
        if code[0] == '`':
            code = code.split('```Python\n')[0].split('```python\n')[1].split('\n```')[0].strip()

        # Log this attempt
        attempts.append((code, error))
        log_attempt(query, attempt, code, error)

        # Try executing the generated pandas code of llm
        try:
            result = run_code(code, df)
            print(type(result), type(result['result']))
            return {
                "success": True,
                "final_code": code,
                "result_locals": result,
                "attempts": attempts
            }
        except Exception as e:
            error = traceback.format_exc()
    return {
        "success": False,
        "final_code": None,
        "error": error,
        "attempts": attempts
    }


# def generate_pandas_code(query: str) -> str:
#     chain = get_llm_chain()
#     full_prompt = build_prompt(query)
#     result = chain.run(query=full_prompt)
#     return result

