from fastapi import FastAPI

app = FastAPI(
    title="Enterprise AI Platform",
    version="1.0.0",
    description="Enterprise AI Platform Backend"
)


@app.get("/")
def root():
    return {
        "status": "running"
    }


@app.get("/health")
def health():
    return {
        "database": "connected",
        "vector_db": "connected",
        "llm": "connected"
    }