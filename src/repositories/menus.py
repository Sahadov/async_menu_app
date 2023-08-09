from db.models.menu import Menu
from utils.menus import SQLAlchemyRepository


class MenuRepository(SQLAlchemyRepository):
    model = Menu
