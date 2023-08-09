from db.models.dish import Dish
from utils.dishes import SQLAlchemyRepository


class DishRepository(SQLAlchemyRepository):
    model = Dish
