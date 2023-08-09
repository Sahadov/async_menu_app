from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from ..db_setup import Base


class Menu(Base):
    __tablename__ = 'Menus'
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(), unique=True, nullable=False)
    description = Column(String())
    # Отношение один-ко-многим с таблицей SubMenu
    submenus = relationship('SubMenu', back_populates='menu', cascade='all, delete-orphan')


'''
class Menu(Base):
    __tablename__ = "Menus"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    title: Mapped[str] = mapped_column(unique=True, nullable=False)
    description: Mapped[str]
    # Отношение один-ко-многим с таблицей SubMenu
    submenus = relationship("SubMenu", back_populates="menu", cascade="all, delete-orphan")
'''
