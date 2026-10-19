from fastapi import APIRouter

main_router = APIRouter()
agent_router = APIRouter(prefix="/agent", tags=["Agent"])

@main_router.get("/health", response_model=dict[str, str])
def health():
    return {"status": "ok"}