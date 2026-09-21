from pydantic import BaseModel


class CategoryCreate(BaseModel):
    name: str


class CategoryOut(BaseModel):
    id: int
    name: str
    user_id: int

    model_config = {"from_attributes": True}