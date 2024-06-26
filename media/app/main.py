from fastapi import FastAPI, File, UploadFile
from minio import Minio
import os

app = FastAPI()

client = Minio(
    endpoint="minio:9000",
    access_key=os.getenv("MINIO_ACCESS_KEY"),
    secret_key=os.getenv("MINIO_SECRET_KEY"),
    secure=False
)

bucket_name = "memes"

@app.get("/health")
async def health_check():
    return {"status": "ok"}

@app.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    if not client.bucket_exists(bucket_name):
        client.make_bucket(bucket_name)
    client.put_object(bucket_name, file.filename, file.file, length=-1, part_size=10*1024*1024)
    return {"filename": file.filename}
