from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from datetime import datetime
from app.database import Base, engine
from app.routers import auth, jobs, applicants, applications, stats

Base.metadata.create_all(bind=engine)

app = FastAPI(title="HireSense API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(jobs.router, prefix="/jobs", tags=["jobs"])
app.include_router(applicants.router, prefix="/applicants", tags=["applicants"])
app.include_router(applications.router, prefix="/applications", tags=["applications"])
app.include_router(stats.router, prefix="/auth", tags=["stats"])


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=422,
        content={"detail": "Invalid input.", "errors": exc.errors()},
    )


@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"detail": "Something went wrong on our end. Please try again."},
    )


_rate_limit_store: dict[str, list[float]] = {}
RATE_LIMIT = 60
RATE_WINDOW = 60


@app.middleware("http")
async def rate_limit_middleware(request: Request, call_next):
    ip = request.client.host
    now = datetime.utcnow().timestamp()
    window_start = now - RATE_WINDOW
    hits = [t for t in _rate_limit_store.get(ip, []) if t > window_start]
    if len(hits) >= RATE_LIMIT:
        return JSONResponse(status_code=429, content={"detail": "Too many requests. Slow down."})
    hits.append(now)
    _rate_limit_store[ip] = hits
    return await call_next(request)