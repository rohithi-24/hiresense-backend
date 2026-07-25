from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from datetime import datetime
from app.database import Base, engine
from app.routers import auth, jobs, applicants, applications, stats, screening, reports

Base.metadata.create_all(bind=engine)

app = FastAPI(title="HireSense API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "https://hirsense.netlify.app",
        "https://hiresense.netlify.app",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(jobs.router, prefix="/jobs", tags=["jobs"])
app.include_router(applicants.router, prefix="/applicants", tags=["applicants"])
app.include_router(applications.router, prefix="/applications", tags=["applications"])
app.include_router(stats.router, prefix="/stats", tags=["stats"])
app.include_router(screening.router, prefix="/screening", tags=["screening"])
app.include_router(reports.router, prefix="/reports", tags=["reports"])
