from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.dependencies import get_db
from app.models.property import Property
from app.models.property_manager import PropertyManager
from app.schemas.property_create import PropertyCreate
from app.schemas.property_update import PropertyUpdate

router = APIRouter()


@router.post("/property/")
def create_property(property_create: PropertyCreate, db: Session = Depends(get_db)):
    property = Property(**property_create.model_dump())
    property_manager = (
        db.query(PropertyManager).filter(PropertyManager.id == property_create.property_manager_id).first()
    )
    if property_manager is None:
        raise HTTPException(status_code=404, detail="Property Manager not found")
    db.add(property)
    db.commit()
    db.refresh(property)
    return property


@router.put("/property/{property_id}")
def update_property(property_id: int, property_update: PropertyUpdate, db: Session = Depends(get_db)):
    property = db.query(Property).filter(Property.id == property_id).first()
    if property is None:
        raise HTTPException(status_code=404, detail="Property not found")
    property_manager = (
        db.query(PropertyManager).filter(PropertyManager.id == property_update.property_manager_id).first()
    )
    if property_manager is None:
        raise HTTPException(status_code=404, detail="Property Manager not found")
    for field, value in property_update.model_dump(exclude_unset=True).items():
        setattr(property, field, value)
    db.add(property)
    db.commit()
    db.refresh(property)
    return property


@router.delete("/property/{property_id}")
def delete_property(property_id: int, db: Session = Depends(get_db)):
    property = db.query(Property).filter(Property.id == property_id).first()
    if property is None:
        raise HTTPException(status_code=404, detail="Property not found")
    db.delete(property)
    db.commit()
    return property


@router.get("/properties/")
def get_propertys(db: Session = Depends(get_db)):
    propertys = db.query(Property).all()
    if propertys is None or len(propertys) == 0:
        raise HTTPException(status_code=404, detail="Propertys not found")
    return propertys


@router.get("/property/{property_id}")
def get_property_by_id(property_id: int, db: Session = Depends(get_db)):
    property = db.query(Property).filter(Property.id == property_id).first()
    if property is None:
        raise HTTPException(status_code=404, detail="Property not found")
    return property
