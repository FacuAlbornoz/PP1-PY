from typing import Annotated

from fastapi import FastAPI, HTTPException, Path, Query
from pydantic import BaseModel, Field

app = FastAPI()

app.title = "Resintech - Gestión de Laboratorio"

not_found = {
    404: {
        "description": "Componente no encontrado",
        "content": {
            "application/json": {
                "example": {
                    "detail": "Componente no encontrado",
                }
            }
        },
    },
}


class ComponenteSchema(BaseModel):
    id: Annotated[int, Field(gt=0, description="ID del componente")]
    nombre: Annotated[str, Field(min_length=3, max_length=50, description="Nombre del componente")]
    categoria: Annotated[str, Field(min_length=2, max_length=30, description="Categoría del componente")]
    stock: Annotated[int, Field(ge=0, le=10000, description="Cantidad en stock")] = 1
    activo: Annotated[bool, Field(description="Disponible?")] = True


class ComponenteUpdateSchema(BaseModel):
    nombre: Annotated[str, Field(min_length=3, max_length=50, description="Nombre del componente")]
    categoria: Annotated[str, Field(min_length=2, max_length=30, description="Categoría del componente")]
    stock: Annotated[int, Field(ge=0, le=10000, description="Cantidad en stock")] = 1
    activo: Annotated[bool, Field(description="Disponible?")] = True


inventario = [
    {"id": 1, "nombre": "Placa Arduino Nano", "categoria": "Electronica", "stock": 10, "activo": True},
    {"id": 2, "nombre": "Sensor Ultrasonico HC-SR04", "categoria": "Electronica", "stock": 5, "activo": True},
    {"id": 3, "nombre": "Engranaje Extrusor Kobra 3", "categoria": "3D", "stock": 2, "activo": True},
]


@app.get("/items", response_model=list[ComponenteSchema])
async def obtener_todos(
    categoria: Annotated[
        str | None,
        Query(min_length=2, max_length=30, description="Filtrar por categoría"),
    ] = None,
):
    if categoria:
        resultado = []
        for item in inventario:
            if item["categoria"].lower() == categoria.lower():
                resultado.append(item)
        return resultado
    return inventario


@app.get(
    "/items/{id}",
    responses=not_found,
    response_model=ComponenteSchema,
)
async def obtener_por_id(
    id: Annotated[int, Path(gt=0, description="Id a buscar en el inventario. >0")],
):
    for item in inventario:
        if item["id"] == id:
            return item
    raise HTTPException(status_code=404, detail="Componente no encontrado")


@app.post("/items", response_model=list[ComponenteSchema])
async def agregar_componente(componente_nuevo: ComponenteSchema):
    inventario.append(componente_nuevo.model_dump())
    return inventario


@app.put(
    "/items/{id}",
    responses=not_found,
    response_model=ComponenteSchema,
)
async def editar_componente(
    id: Annotated[int, Path(gt=0, description="Id del componente. >0")],
    componente_editar: ComponenteUpdateSchema,
):
    for item in inventario:
        if item["id"] == id:
            item["nombre"] = componente_editar.nombre
            item["categoria"] = componente_editar.categoria
            item["stock"] = componente_editar.stock
            item["activo"] = componente_editar.activo
            return item
    raise HTTPException(status_code=404, detail="Componente no encontrado")


@app.delete(
    "/items/{id}",
    responses=not_found,
    response_model=ComponenteSchema,
)
async def borrar_componente(
    id: Annotated[int, Path(gt=0, description="Id del componente. >0")],
    logico: Annotated[bool, Query(description="Mantener registro?")] = False,
):
    for item in inventario:
        if item["id"] == id:
            if logico:
                item["activo"] = False
            else:
                inventario.remove(item)
            return item
    raise HTTPException(status_code=404, detail="Componente no encontrado")
