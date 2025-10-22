from sqlmodel import Session
from ..repositories.property_repository import PropertyRepository
from ..schemas.property import PropertyCreate, PropertyUpdate

class PropertyService:
    def __init__(self, session: Session):
        self.repo = PropertyRepository(session)

    def list(self):
        return self.repo.list()

    def get(self, prop_id: int):
        return self.repo.get(prop_id)

    def create(self, data: PropertyCreate):
        return self.repo.create(data)

    def update(self, prop_id: int, data: PropertyUpdate):
        return self.repo.update(prop_id, data)

    def delete(self, prop_id: int):
        return self.repo.delete(prop_id)
