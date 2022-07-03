# from pulumi import automation as auto
from pulumi_gcp import storage
from fastapi import FastAPI
from pydantic import BaseModel


app = FastAPI()


def create_pulumi_bucket(bucket_name: str) -> storage.Bucket:
    static_site = storage.Bucket(
        resource_name=bucket_name,
        location="EUROPE-WEST2"
    )
    return static_site


class Bucket(BaseModel):
    bucket_id: int
    name: str
    bucket_location: str
    description: str | None


@app.post('/')
async def create_bucket(bucket: Bucket):
    return bucket


@app.get("/")
async def root():
    return {"message": "Hello John"}
