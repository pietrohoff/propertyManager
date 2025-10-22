from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from ...db.session import get_session
from ...schemas.property import PropertyCreate, PropertyUpdate, PropertyRead
from ...services.property_service import PropertyService

router = APIRouter(prefix="/properties", tags=["properties"])

@router.get("", response_model=list[PropertyRead])
def list_properties(session: Session = Depends(get_session)):
    return PropertyService(session).list()

@router.post("", response_model=PropertyRead, status_code=201)
def create_property(payload: PropertyCreate, session: Session = Depends(get_session)):
    return PropertyService(session).create(payload)

@router.put("/{prop_id}", response_model=PropertyRead)
def update_property(prop_id: int, payload: PropertyUpdate, session: Session = Depends(get_session)):
    try:
        return PropertyService(session).update(prop_id, payload)
    except ValueError:
        raise HTTPException(status_code=404, detail="Property not found")

@router.delete("/{prop_id}")
def delete_property(prop_id: int, session: Session = Depends(get_session)):
    ok = PropertyService(session).delete(prop_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Property not found")
    return {"ok": True}
