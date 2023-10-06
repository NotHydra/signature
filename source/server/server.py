from fastapi import FastAPI

app = FastAPI()


@app.get("/api/user")
def hello():
    return {"test": "Hello"}


@app.get("/api/user/{currentDate}")
def hello(currentDate):
    return {"test": currentDate}
