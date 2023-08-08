from db.models.submenu import SubMenu
from utils.submenus import SQLAlchemyRepository

class SubMenuRepository(SQLAlchemyRepository):
    model = SubMenu