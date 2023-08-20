from fastapi import FastAPI, BackgroundTasks
from fastapi.staticfiles import StaticFiles
from src.routes import contacts,auth
import uvicorn

app= FastAPI()

app.mount("/static", StaticFiles(directory="src/static"), name="static")

app.include_router(contacts.router)
app.include_router(auth.router)

if __name__ == '__main__':
    uvicorn.run("main:app", host="127.0.0.1", reload=True, log_level="info")