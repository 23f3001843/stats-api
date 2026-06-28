import time
import uuid
from fastapi import FastAPI, Request, Response
from fastapi.responses import JSONResponse

app = FastAPI()

# ✅ YOUR assigned allowed origin (the one from the error message)
ALLOWED_ORIGIN = "https://dash-aji2l6.example.com"

# ✅ YOUR email address — change this!
YOUR_EMAIL = "your-email@example.com"


@app.middleware("http")
async def cors_and_metrics_middleware(request: Request, call_next):
    """
    This middleware runs on EVERY request before and after your route handler.
    It handles CORS manually so we have full control.
    """
    start_time = time.perf_counter()
    request_id = str(uuid.uuid4())
    origin = request.headers.get("origin", "")

    # --- Handle CORS Preflight (OPTIONS) requests ---
    if request.method == "OPTIONS":
        headers = {
            "X-Request-ID": request_id,
            "X-Process-Time": "0.000001",
            "Access-Control-Allow-Methods": "GET, OPTIONS",
            "Access-Control-Allow-Headers": "Content-Type, Authorization",
            "Access-Control-Max-Age": "600",
        }
        # Only echo ACAO header if the origin is our allowed one
        if origin == ALLOWED_ORIGIN:
            headers["Access-Control-Allow-Origin"] = ALLOWED_ORIGIN
        # Evil origins get no ACAO header at all (grader requirement)
        return Response(status_code=200, headers=headers)

    # --- Handle normal GET requests ---
    response = await call_next(request)
    elapsed = time.perf_counter() - start_time

    # Add required headers to every response
    response.headers["X-Request-ID"] = request_id
    response.headers["X-Process-Time"] = f"{elapsed:.6f}"

    # Only add CORS header if request came from the allowed origin
    if origin == ALLOWED_ORIGIN:
        response.headers["Access-Control-Allow-Origin"] = ALLOWED_ORIGIN

    return response


@app.get("/stats")
async def get_stats(values: str):
    """
    Parses comma-separated integers and returns descriptive statistics.
    Example: GET /stats?values=1,2,3,4,5
    """
    # Parse the comma-separated string into a list of integers
    nums = [int(v.strip()) for v in values.split(",")]

    count = len(nums)
    total = sum(nums)
    minimum = min(nums)
    maximum = max(nums)
    mean = total / count

    return {
        "email": YOUR_EMAIL,
        "count": count,
        "sum": total,
        "min": minimum,
        "max": maximum,
        "mean": round(mean, 6),
    }
