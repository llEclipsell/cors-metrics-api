import time
import uuid

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

ALLOWED_ORIGIN = "https://dash-rnccdn.example.com"
MY_EMAIL = "24f2001120@ds.study.iitm.ac.in"

# CORS: only the assigned origin gets Access-Control-Allow-Origin
app.add_middleware(
    CORSMiddleware,
    allow_origins=[ALLOWED_ORIGIN],
    allow_credentials=True,
    allow_methods=["GET", "OPTIONS"],
    allow_headers=["*"],
)


@app.middleware("http")
async def add_custom_headers(request: Request, call_next):
    start = time.time()
    response = await call_next(request)
    process_time = time.time() - start
    response.headers["X-Request-ID"] = str(uuid.uuid4())
    response.headers["X-Process-Time"] = f"{process_time:.6f}"
    return response


@app.get("/stats")
async def stats(values: str):
    nums = [int(x.strip()) for x in values.split(",") if x.strip() != ""]
    count = len(nums)
    total = sum(nums)
    mean = (total / count) if count else 0.0
    return {
        "email": MY_EMAIL,
        "count": count,
        "sum": total,
        "min": min(nums) if nums else None,
        "max": max(nums) if nums else None,
        "mean": mean,
    }
