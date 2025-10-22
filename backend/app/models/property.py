from typing import Optional
from sqlmodel import Field, SQLModel

class Property(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    address: str
    status: str = "active"  # 'active' | 'inactive'
