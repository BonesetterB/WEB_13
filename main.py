from fastapi import FastAPI,Request,status
from ipaddress import ip_address
from fastapi.staticfiles import StaticFiles
from src.routes import contacts,auth
import uvicorn
from fastapi.responses import JSONResponse
from typing import Callable
import re

app= FastAPI()


ALLOWED_IPS = [ip_address('192.168.1.0'), ip_address('172.16.0.0'), ip_address("127.0.0.1")]


@app.middleware("http")
async def limit_access_by_ip(request: Request, call_next: Callable):
    ip = ip_address(request.client.host)
    if ip not in ALLOWED_IPS:
        return JSONResponse(status_code=status.HTTP_403_FORBIDDEN, content={"detail": "Not allowed IP address"})
    response = await call_next(request)
    return response


user_agent_ban_list = [r"Python-urllib"]


@app.middleware("http")
async def user_agent_ban_middleware(request: Request, call_next: Callable):
    user_agent = request.headers.get("user-agent")
    for ban_pattern in user_agent_ban_list:
        if re.search(ban_pattern, user_agent):
            return JSONResponse(status_code=status.HTTP_403_FORBIDDEN, content={"detail": "You are banned"})
    response = await call_next(request)
    return response

app.mount("/static", StaticFiles(directory="src/static"), name="static")

app.include_router(contacts.router)
app.include_router(auth.router)

if __name__ == '__main__':
    uvicorn.run("main:app", host="127.0.0.1", reload=True, log_level="info")