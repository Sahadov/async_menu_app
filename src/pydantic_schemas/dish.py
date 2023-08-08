from pydantic import BaseModel
from sqlalchemy.dialects.postgresql import UUID


class DishBase(BaseModel):
    title: str
    description: str | None = None
    price: float | None = None | str
    

class DishCreate(DishBase):
    pass


class Dish(DishBase):
    id: int | str
    parent_id: int | str
    main_menu_id: int

    class Config:
        orm_mode = True