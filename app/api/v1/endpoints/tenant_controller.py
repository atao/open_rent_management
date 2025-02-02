from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ...models.tenant import Tenant
from ...core.dependencies import get_db

router = APIRouter()

@router.post("/tenants/", response_model=Tenant)
def create_tenant(tenant: Tenant, db: Session = Depends(get_db)):
    db.add(tenant)
    db.commit()
    db.refresh(tenant)
    return tenant