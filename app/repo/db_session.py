from sqlalchemy.orm import Session

from config.config import DB_ENGINE


class DBSession:
    """
        Контекстный менеджер для соединения с БД.
        При успехе: совершает коммит.
        При неудаче: делает откат изменений и выдаёт ошибку
    """

    def __enter__(self):
        self.session = Session(bind=DB_ENGINE)
        return self.session

    def __exit__(self, *args, **kwargs):
        try:
            self.session.commit()
        except Exception as error:
            self.session.rollback()
            raise error
        finally:
            self.session.close()
