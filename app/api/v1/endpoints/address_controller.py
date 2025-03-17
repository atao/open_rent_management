from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.dependencies import get_db
from app.models.address import Address
from app.schemas.address_create import AddressCreate
from app.schemas.address_update import AddressUpdate

router = APIRouter()


@router.post("/address/")
def create_address(address_create: AddressCreate, db: Session = Depends(get_db)):
    address = Address(**address_create.model_dump())
    db.add(address)
    db.commit()
    db.refresh(address)
    return address


@router.put("/address/{address_id}")
def update_address(address_id: int, address_update: AddressUpdate, db: Session = Depends(get_db)):
    address = db.query(Address).filter(Address.id == address_id).first()
    if address is None:
        raise HTTPException(status_code=404, detail="Address not found")
    for field, value in address_update.model_dump(exclude_unset=True).items():
        setattr(address, field, value)
    db.add(address)
    db.commit()
    db.refresh(address)
    return address


@router.delete("/address/{address_id}")
def delete_address(address_id: int, db: Session = Depends(get_db)):
    address = db.query(Address).filter(Address.id == address_id).first()
    if address is None:
        raise HTTPException(status_code=404, detail="Address not found")
    db.delete(address)
    db.commit()
    return address


@router.get("/addresses/")
def get_addresss(db: Session = Depends(get_db)):
    addresss = db.query(Address).all()
    if addresss is None or len(addresss) == 0:
        raise HTTPException(status_code=404, detail="Addresss not found")
    return addresss


@router.get("/address/{address_id}")
def get_address_by_id(address_id: int, db: Session = Depends(get_db)):
    address = db.query(Address).filter(Address.id == address_id).first()
    if address is None:
        raise HTTPException(status_code=404, detail="Address not found")
    return address
