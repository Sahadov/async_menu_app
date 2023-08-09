from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from ..db_setup import Base


class SubMenu(Base):
    __tablename__ = 'Submenus'
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(), unique=True, nullable=False)
    description = Column(String())
    parent_id = Column(Integer, ForeignKey('Menus.id'))

    # Отношение один-ко-многим с таблицей Dish
    dishes = relationship('Dish', back_populates='submenu', cascade='all, delete', passive_deletes=True,)

    # Отношение многие-к-одному с таблицей Menu
    menu = relationship('Menu', back_populates='submenus')


'''
class SubMenu(Base):
    __tablename__ = "Submenus"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    title: Mapped[str] = mapped_column(unique=True, nullable=False)
    description: Mapped[str]
    parent_id: Mapped[int] = mapped_column(ForeignKey("Menus.id"))

     # Отношение один-ко-многим с таблицей Dish
    dishes = relationship("Dish", back_populates="submenu", cascade="all, delete", passive_deletes=True,)

    # Отношение многие-к-одному с таблицей Menu
    menu = relationship("Menu", back_populates="submenus")
'''
