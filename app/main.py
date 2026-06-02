from fastapi import FastAPI

app = FastAPI(title="Sports Events API", description="A small REST API for managing sports events and their results.")


@app.get("/health")
def health_check():
    return {"status": "ok"}
