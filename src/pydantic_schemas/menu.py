from pydantic import BaseModel


class MenuBase(BaseModel):
    title: str
    description: str | None = None

    class Config:
        orm_mode = True


class MenuCreate(MenuBase):
    pass


class Menu(MenuBase):
    id: int

    class Config:
        orm_mode = True
