# import sys
# import os
# import pandas as pd
#
# # Add the parent directory to sys.path
# parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# sys.path.insert(0, parent_dir)
#
# from agent.executor import run_with_retry
# from agent.config import SCHEMA_CSV_PATH
# if __name__ == "__main__":
#     # query = "Get average income grouped by city"
#     # code = generate_pandas_code(query)
#     df = pd.read_csv(SCHEMA_CSV_PATH)
#     query = "List all the people with income above average, grouped by city"
#     result = run_with_retry(query, df)
#
#     if result['success']:
#         print("✅ Final Working Code:\n", result["final_code"])
#         print("🔍 Sample Output:\n", result["result_locals"])
#     else:
#         print("❌ Failed after retries.")
#         print("Error:\n", result["error"])

# app/main.py

from fastapi import FastAPI, UploadFile, File, Form
from pydantic import BaseModel
import pandas as pd
from io import StringIO
from agent.executor import run_with_retry

app = FastAPI(
    title="LangChain Self-Healing Agent",
    description="Pandas code generator with retry & error correction",
    version="1.0"
)

class QueryRequest(BaseModel):
    query: str


@app.post("/run-query")
async def run_query(query: str = Form(...), file: UploadFile = File(...)):
    try:
        # Read uploaded CSV
        contents = await file.read()
        df = pd.read_csv(StringIO(contents.decode("utf-8")))

        # Run agent
        result = run_with_retry(query, df)

        if not result["success"]:
            return {
                "success": False,
                "error": result["error"],
                "attempts": len(result["attempts"])
            }

        # Return preview of final output
        output_df = result["result_locals"].get("result")
        preview = output_df.head(5).to_dict(orient="records") if isinstance(output_df, pd.DataFrame) else {}

        return {
            "success": True,
            "final_code": result["final_code"],
            "output_preview": preview,
            "attempts": len(result["attempts"])
        }

    except Exception as e:
        return {"success": False, "error": str(e)}
