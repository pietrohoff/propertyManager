from sqlmodel import Session, select
from ..models.property import Property
from ..schemas.property import PropertyCreate, PropertyUpdate
from typing import List, Optional

class PropertyRepository:
    def __init__(self, session: Session):
        self.session = session

    def list(self) -> list[Property]:
        return self.session.exec(select(Property)).all()

    def get(self, prop_id: int) -> Optional[Property]:
        return self.session.get(Property, prop_id)

    def create(self, data: PropertyCreate) -> Property:
        item = Property(**data.model_dump())
        self.session.add(item)
        self.session.commit()
        self.session.refresh(item)
        return item

    def update(self, prop_id: int, data: PropertyUpdate) -> Property:
        item = self.get(prop_id)
        if not item:
            raise ValueError("not found")
        for k, v in data.model_dump().items():
            setattr(item, k, v)
        self.session.add(item)
        self.session.commit()
        self.session.refresh(item)
        return item

    def delete(self, prop_id: int) -> bool:
        item = self.get(prop_id)
        if not item:
            return False
        self.session.delete(item)
        self.session.commit()
        return True
