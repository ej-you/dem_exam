from typing import List

from app.entity.good import Good
from app.repo.db_session import DBSession
from config.config import DEFAULT_PHOTO_PATH


class GoodNotFoundError(Exception):
    pass


class GoodRepo:
    def __init__(self, session: DBSession):
        self.session = session

    @staticmethod
    def get_default() -> dict:
        return {
            "id": 0,
            "article": "000000",
            "title": "",
            "measurement_unit": "",
            "price": 0,
            "supplier": "",
            "producer": "",
            "category": "",
            "discount": 0,
            "amount": 0,
            "description": "",
            "photo": DEFAULT_PHOTO_PATH,
        }

    def get_all(self) -> List[dict]:
        with self.session as session:
            good_list = session.query(Good).all()
            return [
                {
                    "id": good.id,
                    "article": good.article,
                    "title": good.title,
                    "price": f"{good.price:.2f} ₽",
                } for good in good_list
            ]

    def get_by_id(self, pk: int):
        with self.session as session:
            good = session.query(Good).filter(Good.id == pk).first()
            if not good:
                raise GoodNotFoundError("товар не найден")
            return {
                "id": good.id,
                "article": good.article,
                "title": good.title,
                "measurement_unit": good.measurement_unit.name,
                "price": good.price,
                "supplier": good.supplier.title,
                "producer": good.producer.title,
                "category": good.good_category.name,
                "discount": good.discount,
                "amount": good.amount,
                "description": good.description,
                "photo": good.photo,
            }
