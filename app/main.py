from app.api.v1.endpoints import tenant_controller
from app.models.base import Base
from fastapi import FastAPI
from app.core.database import engine

app = FastAPI()

# Créer les tables
Base.metadata.create_all(bind=engine)

app.include_router(tenant_controller.router, prefix="/api/v1")

@app.get("/")
def read_root():
    return {"Hello": "World"}