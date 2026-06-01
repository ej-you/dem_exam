from typing import List

from app.entity.good import Good
from app.repo.db_session import DBSession


class GoodRepo:
    def __init__(self, session: DBSession):
        self.session = session

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
            return {
                "id": good.id,
                "article": good.article,
                "title": good.title,
                "measurement_unit": good.measurement_unit,
                "price": good.price,
                "supplier": good.supplier,
                "producer": good.producer,
                "good_category": good.good_category,
                "discount": good.discount,
                "amount": good.amount,
                "description": good.description,
                "photo": good.photo,
            }
