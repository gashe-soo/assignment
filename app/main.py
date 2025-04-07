from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def get() -> dict[str, str]:
    return {"Hello": "World"}
