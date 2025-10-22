from pydantic import BaseModel, constr, field_validator

class PropertyBase(BaseModel):
    title: constr(strip_whitespace=True, min_length=1)
    address: constr(strip_whitespace=True, min_length=1)
    status: str = "active"

    @field_validator("status")
    @classmethod
    def check_status(cls, v: str) -> str:
        if v not in {"active", "inactive"}:
            raise ValueError("status must be 'active' or 'inactive'")
        return v

class PropertyCreate(PropertyBase):
    pass

class PropertyUpdate(PropertyBase):
    pass

class PropertyRead(PropertyBase):
    id: int
