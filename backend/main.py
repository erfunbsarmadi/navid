# backend/main.py
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
import pandas as pd
import io
from agents import run_pipeline_for_csv
app = FastAPI(title="TradingAgents MVP")
@app.post("/upload_prices/{ticker}")
async def upload_prices(ticker: str, file: UploadFile = File(...)):
content = await file.read()
try:
df = pd.read_csv(io.BytesIO(content))
except Exception as e:
raise HTTPException(status_code=400, detail=f"Invalid CSV: {e}")
# expect columns: date, open, high, low, close, volume
signal = run_pipeline_for_csv(ticker, df)
return JSONResponse(content=signal)
@app.get("/signal/{ticker}")
async def get_signal(ticker: str):
# placeholder for live mode. For prototype, return error instructing to
upload CSV
raise HTTPException(status_code=404,
detail="No live feed configured. Upload CSV to /upload_prices/{ticker}")
if __name__ == "__main__":
import uvicorn
uvicorn.run(app, host="0.0.0.0", port=8000)
