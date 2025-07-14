# tests/test_eval.py

import pandas as pd
from agent.executor import run_with_retry
from agent.evaluator import evaluate_result
from agent.config import SCHEMA_CSV_PATH

df = pd.read_csv(SCHEMA_CSV_PATH)

def test_query_avg_income_by_city():
    query = "Get average income grouped by city"

    # What we expect manually
    expected = df.groupby("city")["income"].mean().reset_index()
    print(type(expected))

    result = run_with_retry(query, df)

    if not result["success"]:
        print("❌ Agent failed to generate working code")
        return

    eval_result = evaluate_result(result["result_locals"], expected, key="result")
    print(f"Query: {query}")
    print("✅ Pass" if eval_result["pass"] else f"❌ Fail: {eval_result['reason']}")
