import time
import uuid
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

# -------------------------------------------------------
# EDIT THIS: paste your actual student email and allowed origin
MY_EMAIL = "23f3001843@ds.study.iitm.ac.in"
ALLOWED_ORIGIN = "https://dash-aji2l6.example.com"
# -------------------------------------------------------

app = FastAPI()

# --- Custom CORS middleware (strict: only the assigned origin) ---
@app.middleware("http")
async def cors_and_metrics_middleware(request: Request, call_next):
    origin = request.headers.get("origin", "")
    start_time = time.perf_counter()
    request_id = str(uuid.uuid4())

    # Handle preflight (OPTIONS) requests
    if request.method == "OPTIONS":
        if origin == ALLOWED_ORIGIN:
            # ✅ Allowed origin: approve the preflight
            response = JSONResponse(content={}, status_code=200)
            response.headers["Access-Control-Allow-Origin"] = ALLOWED_ORIGIN
            response.headers["Access-Control-Allow-Methods"] = "GET, OPTIONS"
            response.headers["Access-Control-Allow-Headers"] = "*"
        else:
            # ❌ Evil origin: reject — no ACAO header at all
            response = JSONResponse(content={"detail": "Forbidden"}, status_code=403)

        process_time = time.perf_counter() - start_time
        response.headers["X-Request-ID"] = request_id
        response.headers["X-Process-Time"] = f"{process_time:.6f}"
        return response

    # Handle regular requests
    response = await call_next(request)

    # Add CORS header only for the allowed origin
    if origin == ALLOWED_ORIGIN:
        response.headers["Access-Control-Allow-Origin"] = ALLOWED_ORIGIN

    process_time = time.perf_counter() - start_time
    response.headers["X-Request-ID"] = request_id
    response.headers["X-Process-Time"] = f"{process_time:.6f}"
    return response


# --- The actual stats endpoint ---
@app.get("/stats")
async def get_stats(values: str):
    # Parse "1,2,3,4" into a Python list of integers
    nums = [int(v.strip()) for v in values.split(",")]

    count = len(nums)
    total = sum(nums)
    minimum = min(nums)
    maximum = max(nums)
    mean = total / count

    return {
        "email": MY_EMAIL,
        "count": count,
        "sum": total,
        "min": minimum,
        "max": maximum,
        "mean": round(mean, 6),
    }
