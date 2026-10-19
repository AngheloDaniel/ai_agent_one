from fastapi import FastAPI

from app.routes.agent_router import main_router

app = FastAPI()

app.include_router(main_router)

if __name__ == '__main__':
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=False)
