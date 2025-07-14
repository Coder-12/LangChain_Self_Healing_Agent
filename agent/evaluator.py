# agent/evaluator.py

import pandas as pd

def evaluate_result(actual_locals: dict, expected_df: pd.DataFrame, key: str = "result") -> dict:
    """
    Compare the DataFrame result inside `actual_locals[key]` to the expected DataFrame.
    """
    if key not in actual_locals:
        return {"pass": False, "reason": f"'{key}' not in agent output."}

    result_df = actual_locals[key]

    if not isinstance(result_df, pd.DataFrame):
        return {"pass": False, "reason": f"'{key}' is not a DataFrame."}

    try:
        # Reset index for consistent comparison
        result_df = result_df.reset_index(drop=True)
        expected_df = expected_df.reset_index(drop=True)

        if result_df.equals(expected_df):
            return {"pass": True, "reason": "Exact match ✅"}
        else:
            return {"pass": False, "reason": "Mismatch in values or rows ❌"}
    except Exception as e:
        return {"pass": False, "reason": str(e)}
