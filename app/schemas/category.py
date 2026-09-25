from pydantic import BaseModel
from app.schemas.expense import ExpenseOut

class CategoryCreate(BaseModel):
    name: str


class CategoryOut(BaseModel):
    id: int
    name: str
    user_id: int

    model_config = {"from_attributes": True}


class CategoryWithExpenses(BaseModel):
    id: int
    name: str
    expenses: list[ExpenseOut]

    model_config = {"from_attributes": True}