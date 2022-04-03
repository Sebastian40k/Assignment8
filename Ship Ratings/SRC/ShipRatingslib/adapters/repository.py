import abc
from ShipRatingslib.Domain import ReviewFramework


class AbstractRepository(abc.ABC):
    @abc.abstractmethod
    def add(self, product: ReviewFramework.Product):
        raise NotImplementedError

    @abc.abstractmethod
    def get(self, sku) -> ReviewFramework.Product:
        raise NotImplementedError


class SqlAlchemyRepository(AbstractRepository):
    def __init__(self, session):
        self.session = session

    def add(self, product):
        self.session.add(product)

    def get(self, sku):
        return self.session.query(ReviewFramework.Product).filter_by(sku=sku).first()
