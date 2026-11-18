from sqlalchemy import Boolean, Column, Float, Integer, String
from database import Base


class Producto(Base):
    __tablename__ = "productos"

    id = Column(Integer, primary_key=True)
    nombre = Column(String)
    marca = Column(String)
    precio = Column(Float)
    activo = Column(Boolean)
