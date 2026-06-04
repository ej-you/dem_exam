from typing import List

from app.entity.good import Good, MeasurementUnit, Supplier, Producer, GoodCategory
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
                    "id": elem.id,
                    "article": elem.article,
                    "title": elem.title,
                    "price": f"{elem.price:.2f} ₽",
                } for elem in good_list
            ]

    def get_by_id(self, pk: int):
        with self.session as session:
            good = session.query(Good).filter(Good.id == pk).first()
            if not good:
                raise GoodNotFoundError("товар не найден")
            return self._to_dict(good)

    def create(self, data: dict):
        with self.session as session:
            good = Good(
                article=data["article"],
                title=data["title"],
                measurement_unit_id=data["measurement_unit_id"],
                price=data["price"],
                supplier_id=data["supplier_id"],
                producer_id=data["producer_id"],
                good_category_id=data["good_category_id"],
                discount=data.get("discount", 0),
                amount=data.get("amount", 0),
                description=data.get("description"),
                photo=data.get("photo", DEFAULT_PHOTO_PATH),
            )

            session.add(good)
            session.commit()
            # get ID and other default fields
            session.refresh(good)
            return self._to_dict(good)

    def update(self, pk: int, data: dict):
        with self.session as session:
            # find good
            good = session.query(Good).filter(Good.id == pk).first()
            if not good:
                raise GoodNotFoundError(f"Товар {pk} не найден")

            # update only given fields
            for key, value in data.items():
                if hasattr(good, key) and value is not None:
                    setattr(good, key, value)

            session.commit()
            session.refresh(good)
            return self._to_dict(good)

    def get_all_measurement_units(self):
        with self.session as session:
            unit_list = session.query(MeasurementUnit).all()
            return [
                {
                    "id": elem.id,
                    "name": elem.name,
                } for elem in unit_list
            ]

    def get_all_suppliers(self):
        with self.session as session:
            sup_list = session.query(Supplier).all()
            return [
                {
                    "id": elem.id,
                    "title": elem.title,
                } for elem in sup_list
            ]
    def get_all_producers(self):
        with self.session as session:
            prod_list = session.query(Producer).all()
            return [
                {
                    "id": elem.id,
                    "title": elem.title,
                } for elem in prod_list
            ]

    def get_all_good_categories(self):
        with self.session as session:
            cat_list = session.query(GoodCategory).all()
            return [
                {
                    "id": elem.id,
                    "name": elem.name,
                } for elem in cat_list
            ]

    @staticmethod
    def _to_dict(good: Good) -> dict:
        """Преобразует объект Good в словарь"""
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
