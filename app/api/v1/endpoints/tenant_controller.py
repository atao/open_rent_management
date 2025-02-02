from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.dependencies import get_db
from app.models.tenant import Tenant
from app.schemas.tenant_create import TenantCreate
from app.schemas.tenant_update import TenantUpdate

router = APIRouter()

@router.post("/tenant/")
def create_tenant(tenant_create: TenantCreate, db: Session = Depends(get_db)):
    tenant = Tenant(**tenant_create.model_dump())
    db.add(tenant)
    db.commit()
    db.refresh(tenant)
    return tenant

@router.put("/tenant/{tenant_id}")
def update_tenant(tenant_id: int, tenant_update: TenantUpdate, db: Session = Depends(get_db)):
    tenant = db.query(Tenant).filter(Tenant.id == tenant_id).first()
    if(tenant is None):
        raise HTTPException(status_code=404, detail="Tenant not found")
    for field, value in tenant_update.model_dump(exclude_unset=True).items():
        setattr(tenant, field, value)
    db.add(tenant)
    db.commit()
    db.refresh(tenant)
    return tenant

@router.delete("/tenant/{tenant_id}")
def delete_tenant(tenant_id: int, db: Session = Depends(get_db)):
    tenant = db.query(Tenant).filter(Tenant.id == tenant_id).first()
    if(tenant is None):
        raise HTTPException(status_code=404, detail="Tenant not found")
    db.delete(tenant)
    db.commit()
    return tenant

@router.get("/tenants/")
def get_tenants(db: Session = Depends(get_db)):
    tenants = db.query(Tenant).all()
    if(tenants is None or len(tenants) == 0):
        raise HTTPException(status_code=404, detail="Tenants not found")
    return tenants

@router.get("/tenant/{tenant_id}")
def get_tenant_by_id(tenant_id: int, db: Session = Depends(get_db)):
    tenant = db.query(Tenant).filter(Tenant.id == tenant_id).first()
    if(tenant is None):
        raise HTTPException(status_code=404, detail="Tenant not found")
    return tenant