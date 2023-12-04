from typing import Any, List, Optional, Sequence

from sqlalchemy.sql import text, column, func, desc
import calendar

from app.common.singleton import Singleton

from .models import Beverage, Ingredient, Order, OrderDetail, Size, db
from .serializers import (BeverageSerializer, IngredientSerializer,
                          OrderSerializer, SizeSerializer, ma)

TOP_CUSTOMERS = 3

class BaseManager(metaclass=Singleton):
    model: Optional[db.Model] = None
    serializer: Optional[ma.SQLAlchemyAutoSchema] = None
    session = db.session

    @classmethod
    def get_all(cls):
        serializer = cls.serializer(many=True)
        _objects = cls.model.query.all()
        result = serializer.dump(_objects)
        return result

    @classmethod
    def get_by_id(cls, _id: Any):
        entry = cls.model.query.get(_id)
        return cls.serializer().dump(entry)

    @classmethod
    def create(cls, entry: dict):
        serializer = cls.serializer()
        new_entry = serializer.load(entry)
        cls.session.add(new_entry)
        cls.session.commit()
        return serializer.dump(new_entry)

    @classmethod
    def update(cls, _id: Any, new_values: dict):
        cls.session.query(cls.model).filter_by(_id=_id).update(new_values)
        cls.session.commit()
        return cls.get_by_id(_id)


class SizeManager(BaseManager, metaclass=Singleton):
    model = Size
    serializer = SizeSerializer


class IngredientManager(BaseManager, metaclass=Singleton):
    model = Ingredient
    serializer = IngredientSerializer

    @classmethod
    def get_by_id_list(cls, ids: Sequence):
        return cls.session.query(cls.model).filter(cls.model._id.in_(set(ids))).all() or []
    

class BeverageManager(BaseManager, metaclass=Singleton):
    model = Beverage
    serializer = BeverageSerializer

    @classmethod
    def get_by_id_list(cls, ids: Sequence):
        return cls.session.query(cls.model).filter(cls.model._id.in_(set(ids))).all() or []


class OrderManager(BaseManager, metaclass=Singleton):
    model = Order
    serializer = OrderSerializer

    @classmethod
    def create(cls, order_data: dict, ingredients: List[Ingredient], beverages: List[Beverage]):
        new_order = cls.model(**order_data)
        cls.session.add(new_order)
        cls.session.flush()
        cls.session.refresh(new_order)
        cls.session.add_all((OrderDetail(order_id=new_order._id, ingredient_id=ingredient._id, ingredient_price=ingredient.price)
                             for ingredient in ingredients))
        cls.session.add_all((OrderDetail(order_id=new_order._id, beverage_id=beverage._id, beverage_price=beverage.price)
                             for beverage in beverages))
        cls.session.commit()
        return cls.serializer().dump(new_order)

    @classmethod
    def update(cls):
        raise NotImplementedError(f'Method not suported for {cls.__name__}')


class IndexManager(BaseManager, metaclass=Singleton):

    @classmethod
    def test_connection(cls):
        cls.session.query(column('1')).from_statement(text('SELECT 1')).all()


class ReportManager(BaseManager, metaclass=Singleton):

    @classmethod
    def get_top_ingredient(cls):
        top_ingredient_response = (cls.session.query(Ingredient.name,
            func.count(OrderDetail.ingredient_id).label('qty')
            ).join(OrderDetail
            ).group_by(Ingredient.name
            ).order_by(desc('qty'))
        ).all()

        top_ingredient = {}

        if top_ingredient_response:
            top_ingredient = {
                'name': top_ingredient_response[0][0],
                'count': top_ingredient_response[0][1]
            }
        return top_ingredient

    @classmethod
    def get_top_month(cls):
        top_month_response = (
            cls.session.query(
                func.strftime("%m", Order.date).label("month"), func.sum(Order.total_price).label("revenue")
            ).group_by(func.strftime("%m", Order.date)
            ).order_by(func.sum(Order.total_price).desc())
        ).all()

        top_month = {}

        if top_month_response:
            top_month = {
                'name': calendar.month_name[int(top_month_response[0][0])],
                'total': top_month_response[0][1]
            }
        return top_month
    
    @classmethod
    def get_top_customers(cls):
        top_customers_response = (cls.session.query(Order.client_name,
            func.count(Order._id).label('qty')
            ).group_by(Order.client_name
            ).order_by(desc('qty')).limit(TOP_CUSTOMERS)
        ).all()

        top_customers = {}

        if top_customers_response:
            top_customers = [{
                'name': customer[0],
                'count': customer[1]
            } for customer in top_customers_response]

        return top_customers
