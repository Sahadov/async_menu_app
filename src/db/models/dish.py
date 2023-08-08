from sqlalchemy import Column, ForeignKey, Integer, String, Numeric
from sqlalchemy.orm import relationship
from .submenu import SubMenu
from ..db_setup import Base
from sqlalchemy.orm import Mapped, mapped_column


class Dish(Base):
    __tablename__ = "Dishes"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(), unique=True, nullable=False)
    description = Column(String())
    price = Column(Numeric(10, 2), nullable=False)
    parent_id = Column(Integer, ForeignKey("Submenus.id", ondelete="CASCADE"))
    
    # Отношение многие-к-одному с таблицей SubMenu
    submenu = relationship("SubMenu", back_populates="dishes")
    
    main_menu_id = Column(Integer)
