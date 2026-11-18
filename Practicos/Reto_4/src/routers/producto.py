from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Path, Query
from sqlalchemy.orm import Session

from database import get_db
from models.zapatillas import Producto
from schemas.zapatillas import ProductoSchema, ProductoUpdateSchema

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
    response_model=list[ProductoSchema],
)
async def getProductos(db: Session = Depends(get_db)):
    productos = db.query(Producto).all()
    return productos


@productos_routers.get(
    "/{id}",
    response_model=ProductoSchema,
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
    response_model=ProductoSchema,
)
async def postProducto(
    producto_nuevo: ProductoSchema,
    db: Session = Depends(get_db),
):
    producto_db = Producto(
        nombre=producto_nuevo.nombre,
        marca=producto_nuevo.marca,
        precio=producto_nuevo.precio,
        activo=producto_nuevo.activo,
    )
    db.add(producto_db)
    db.commit()
    db.refresh(producto_db)
    return producto_db


@productos_routers.put(
    "/{id}",
    responses=noEncontrado,
    response_model=ProductoSchema,
)
async def modificarProducto(
    id: Annotated[int, Path(gt=0)],
    producto_editado: ProductoUpdateSchema,
    db: Session = Depends(get_db),
):
    producto_obtenido = db.get(Producto, id)
    if producto_obtenido is not None:
        producto_obtenido.nombre = producto_editado.nombre
        producto_obtenido.marca = producto_editado.marca
        producto_obtenido.precio = producto_editado.precio
        producto_obtenido.activo = producto_editado.activo
        db.commit()
        db.refresh(producto_obtenido)
        return producto_obtenido

    raise HTTPException(status_code=404, detail="Producto no encontrado")


@productos_routers.delete(
    "/{id}",
    responses=noEncontrado,
    response_model=list[ProductoSchema],
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
        return db.query(Producto).all()

    raise HTTPException(status_code=404, detail="Producto no encontrado")
