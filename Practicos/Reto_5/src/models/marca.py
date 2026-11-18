from sqlmodel import Field, Relationship, SQLModel


class MarcaBase(SQLModel):
    nombre: str = Field(max_length=50)
    pais: str = Field(max_length=50)


class Marca(MarcaBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    productos: list["Producto"] | None = Relationship(back_populates="marca")


class MarcaPublic(MarcaBase):
    id: int
