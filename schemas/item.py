from ma import ma
from models.item import ItemModel
from models.store import StoreModel


class ItemSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = ItemModel
        load_instance = True
        load_only = ("store",)
        dump_only = ("id",)
        include_fk = True


# from pydantic.dataclasses import dataclass

# @dataclass
# class ItemSchema:
#     name: str
#     price: float
#     store_id: int
