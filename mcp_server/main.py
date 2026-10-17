from fastapi import FastAPI

from app.routers.tools_route import tools_router

app = FastAPI()

app.include_router(tools_router)




if __name__ == '__main__':
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=False)
