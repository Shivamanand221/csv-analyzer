from fastapi import FastAPI
from routes.csv import router

app= FastAPI(
    title= "CSV Analyzer",
    description= "CSV analysis API using Pandas and NumPy",
    version= "1.0.0"
)

app.include_router(router)

@app.get("/")
def status():
    return "CSV Analyzer API is running"

@app.get("/health")
def status():
    return {"status": "healthy"}