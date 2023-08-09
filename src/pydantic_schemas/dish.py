from pydantic import BaseModel


class DishBase(BaseModel):
    title: str
    description: str | None = None
    price: float | str | None = None


class DishCreate(DishBase):
    pass


class Dish(DishBase):
    id: int | str
    parent_id: int | str
    main_menu_id: int

    class Config:
        orm_mode = True
