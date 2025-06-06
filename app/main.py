from app.api.v1.endpoints import (
    address_controller,
    property_controller,
    property_manager_controller,
    tenant_controller,
    user_controller,
)
from app.models.base import Base
from fastapi import FastAPI
from app.core.database import engine
import uvicorn

app = FastAPI()

# Créer les tables
Base.metadata.create_all(bind=engine)

app.include_router(tenant_controller.router, prefix="/api/v1")
app.include_router(property_manager_controller.router, prefix="/api/v1")
app.include_router(property_controller.router, prefix="/api/v1")
app.include_router(address_controller.router, prefix="/api/v1")
app.include_router(user_controller.router, prefix="/api/v1")


@app.get("/api/healthchecker")
def read_root():
    return {"message": "Hello World"}


def start():
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
