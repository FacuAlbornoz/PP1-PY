from sqlmodel import Field, Relationship, SQLModel

from .marca import Marca


class ProductoBase(SQLModel):
    nombre: str = Field(min_length=1, max_length=30)
    precio: float = Field(gt=0, lt=999999999)
    activo: bool = True
    marca_id: int | None = Field(default=None, foreign_key="marca.id")


class Producto(ProductoBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    marca: Marca | None = Relationship(back_populates="productos")


class ProductoPublic(ProductoBase):
    id: int
