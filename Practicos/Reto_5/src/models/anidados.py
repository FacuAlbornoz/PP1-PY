from .marca import Marca, MarcaPublic
from .zapatillas import Producto, ProductoPublic


class ProductoNested(ProductoPublic):
    marca: Marca | None = None


class MarcaNested(MarcaPublic):
    productos: list[Producto] = []
