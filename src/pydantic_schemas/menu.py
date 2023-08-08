from pydantic import BaseModel
from sqlalchemy.dialects.postgresql import UUID


class MenuBase(BaseModel):
    title: str
    description: str | None = None


class MenuCreate(MenuBase):
    pass


class Menu(MenuBase):
    id: int
    

    class Config:
        orm_mode = True