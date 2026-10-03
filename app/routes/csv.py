from fastapi import APIRouter, UploadFile, File

router= APIRouter()

@router.post("/upload")
async def upload_csv(file: UploadFile= File(...)):
    content= await file.read()

    with open(f"../uploads/{file.filename}", "wb") as f:
        f.write(content)
    
    return{
        "message": "file uploaded successfully",
        "filename": file.filename
    }