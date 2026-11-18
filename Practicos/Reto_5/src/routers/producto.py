from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Path, Query
from sqlmodel import Session, select

from database import get_db
from models.anidados import ProductoNested
from models.zapatillas import Producto, ProductoBase, ProductoPublic

productos_routers = APIRouter()

NO_ENCONTRADO = noEncontrado = {
    404: {
        "description": "Producto no encontrado",
        "content": {
            "application/json": {
                "example": {
                    "detail": "Producto no encontrado",
                }
            }
        },
    },
}


@productos_routers.get(
    "/",
    response_model=list[ProductoPublic],
)
async def getProductos(db: Session = Depends(get_db)):
    productos = db.exec(select(Producto)).all()
    return productos


@productos_routers.get(
    "/{id}",
    response_model=ProductoNested,
    responses=noEncontrado,
)
async def obtenerProductoId(
    id: Annotated[int, Path(gt=0)],
    db: Session = Depends(get_db),
):
    producto_obtenido = db.get(Producto, id)
    if producto_obtenido is not None:
        return producto_obtenido
    raise HTTPException(status_code=404, detail="Producto no encontrado")


@productos_routers.post(
    "/",
    response_model=ProductoNested,
)
async def postProducto(
    producto_nuevo: ProductoBase,
    db: Session = Depends(get_db),
):
    producto_db = Producto.model_validate(producto_nuevo)
    db.add(producto_db)
    db.commit()
    db.refresh(producto_db)
    return producto_db


@productos_routers.put(
    "/{id}",
    responses=noEncontrado,
    response_model=ProductoPublic,
)
async def modificarProducto(
    id: Annotated[int, Path(gt=0)],
    producto_editado: ProductoBase,
    db: Session = Depends(get_db),
):
    producto_obtenido = db.get(Producto, id)
    if producto_obtenido is not None:
        producto_obtenido.nombre = producto_editado.nombre
        producto_obtenido.precio = producto_editado.precio
        producto_obtenido.activo = producto_editado.activo
        producto_obtenido.marca_id = producto_editado.marca_id
        db.commit()
        db.refresh(producto_obtenido)
        return producto_obtenido

    raise HTTPException(status_code=404, detail="Producto no encontrado")


@productos_routers.delete(
    "/{id}",
    responses=noEncontrado,
    response_model=list[ProductoPublic],
)
async def borrarProducto(
    id: Annotated[int, Path(gt=0)],
    db: Session = Depends(get_db),
    logico: Annotated[
        bool,
        Query(description="Mantener registro?"),
    ] = False,
):
    producto_obtenido = db.get(Producto, id)
    if producto_obtenido is not None:
        if logico:
            producto_obtenido.activo = False
            db.commit()
        else:
            db.delete(producto_obtenido)
            db.commit()
        return db.exec(select(Producto)).all()

    raise HTTPException(status_code=404, detail="Producto no encontrado")
