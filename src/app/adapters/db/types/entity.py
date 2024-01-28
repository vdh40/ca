from pydantic import BaseModel
from sqlalchemy.orm import mapped_column


class Entity(BaseModel):
    id: int = mapped_column(primary_key=True)

