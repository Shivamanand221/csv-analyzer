from fastapi import APIRouter, UploadFile, File, HTTPException
from app.services.analyzer import read_csv_file
import pandas as pd
import numpy as np

router= APIRouter()

@router.post("/upload")
async def upload_csv(file: UploadFile= File(...)):
    content= await file.read()

    if not file.filename.endswith(".csv"):
        raise HTTPException(
            status_code=400,
            detail="only csv file is allowed"
        )

    with open(f"../uploads/{file.filename}", "wb") as f:
        f.write(content)

    return{
        "message": "file uploaded successfully",
        "filename": file.filename
    }

@router.get("/analyze")
async def analyze_csv(filename: str):
    file_path= f"../uploads/{filename}"

    df= read_csv_file(file_path)

    return{
        "rows": len(df),
        "columns": len(df.columns),
        "column_names": df.columns.tolist(),
        "data_types": df.dtypes.astype(str).to_dict(),
        "missing_values": df.isnull().sum().to_dict(),
        "numerical_columns": df.select_dtypes(include="number").columns.to_list(),
        "statistics": {
            "mean": df.mean(numeric_only=True).to_dict(),
            "median": df.median(numeric_only=True).to_dict(),
            "min": df.min(numeric_only=True).to_dict(),
            "max": df.max(numeric_only=True).to_dict(),
            "std": df.std(numeric_only=True).to_dict(),
        },
        "numerical_analysis":{
            "variance": df.select_dtypes(include="number").apply(np.var).to_dict(),
            "percentile": {
                "25":df.select_dtypes(include="number").quantile(0.25).to_dict(),
                "50":df.select_dtypes(include="number").quantile(0.50).to_dict(),
                "75":df.select_dtypes(include="number").quantile(0.75).to_dict()
            },
            "sum":{
                column: np.sum(df[column].dropna())
                for column in df.select_dtypes(include="number").columns
            },
            "range": {
                column: np.ptp(df[column].dropna())
                for column in df.select_dtypes(include="number").columns
            }
        }
    }