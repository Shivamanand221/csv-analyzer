from fastapi import APIRouter, UploadFile, File, HTTPException

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