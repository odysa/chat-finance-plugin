from fastapi import FastAPI
from equities import equities_app
import uvicorn

app = FastAPI()
app.mount("/equities", equities_app)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)