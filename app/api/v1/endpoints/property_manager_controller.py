from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.dependencies import get_db
from app.models.property_manager import PropertyManager
from app.schemas.property_manager_create import PropertyManagerCreate
from app.schemas.property_manager_update import PropertyManagerUpdate

router = APIRouter()


@router.post("/property_manager/")
def create_property_manager(property_manager_create: PropertyManagerCreate, db: Session = Depends(get_db)):
    property_manager = PropertyManager(**property_manager_create.model_dump())
    existing_property_manager = (
        db.query(PropertyManager).filter(PropertyManager.email == property_manager.email).first()
    )
    if existing_property_manager is not None:
        raise HTTPException(status_code=400, detail="PropertyManager email already exists")
    db.add(property_manager)
    db.commit()
    db.refresh(property_manager)
    return property_manager


@router.put("/property_manager/{property_manager_id}")
def update_property_manager(
    property_manager_id: int,
    property_manager_update: PropertyManagerUpdate,
    db: Session = Depends(get_db),
):
    property_manager = db.query(PropertyManager).filter(PropertyManager.id == property_manager_id).first()
    if property_manager is None:
        raise HTTPException(status_code=404, detail="PropertyManager not found")
    for field, value in property_manager_update.model_dump(exclude_unset=True).items():
        setattr(property_manager, field, value)
    db.add(property_manager)
    db.commit()
    db.refresh(property_manager)
    return property_manager


@router.delete("/property_manager/{property_manager_id}")
def delete_property_manager(property_manager_id: int, db: Session = Depends(get_db)):
    property_manager = db.query(PropertyManager).filter(PropertyManager.id == property_manager_id).first()
    if property_manager is None:
        raise HTTPException(status_code=404, detail="PropertyManager not found")
    db.delete(property_manager)
    db.commit()
    return property_manager


@router.get("/property_managers/")
def get_property_managers(db: Session = Depends(get_db)):
    property_managers = db.query(PropertyManager).all()
    if property_managers is None or len(property_managers) == 0:
        raise HTTPException(status_code=404, detail="PropertyManagers not found")
    return property_managers


@router.get("/property_manager/{property_manager_id}")
def get_property_manager_by_id(property_manager_id: int, db: Session = Depends(get_db)):
    property_manager = db.query(PropertyManager).filter(PropertyManager.id == property_manager_id).first()
    if property_manager is None:
        raise HTTPException(status_code=404, detail="PropertyManager not found")
    return property_manager
