from fastapi import FastAPI, HTTPException, Path, Query, Body
from pydantic import BaseModel
from typing import Annotated, Optional

app = FastAPI()
app.title = "Resintech - Gestión de Laboratorio"

# Modelo de datos para validación
class Componente(BaseModel):
    id: int
    nombre: str
    categoria: str
    stock: int

# Simulación de Base de Datos
inventario = [
    {"id": 1, "nombre": "Placa Arduino Nano", "categoria": "Electronica", "stock": 10},
    {"id": 2, "nombre": "Sensor Ultrasonico HC-SR04", "categoria": "Electronica", "stock": 5},
    {"id": 3, "nombre": "Engranaje Extrusor Kobra 3", "categoria": "3D", "stock": 2},
]

# PATH OPERATIONS: GET

# 1. Obtener todos con filtro por categoría
@app.get("/items", tags=["Lectura"])
async def obtener_todos(
    cat: Annotated[Optional[str], Query(min_length=2, max_length=15, description="Filtrar por categoría")] = None
):
    """Filtra los componentes del laboratorio por su categoría."""
    if cat:
        return [item for item in inventario if item["categoria"].lower() == cat.lower()]
    return inventario

# 2. Obtener un item por ID
@app.get("/items/{item_id}", tags=["Lectura"])
async def obtener_por_id(
    item_id: Annotated[int, Path(gt=0, description="El ID debe ser mayor a 0")]
):
    for item in inventario:
        if item["id"] == item_id:
            return item
    raise HTTPException(status_code=404, detail="Componente no encontrado")

# PATH OPERATION: POST

# 3. Crear un nuevo componente
@app.post("/items", tags=["Escritura"])
async def agregar_componente(nuevo: Componente):
    if any(item["id"] == nuevo.id for item in inventario):
        raise HTTPException(status_code=400, detail="Ese ID ya existe en el inventario")
    
    inventario.append(nuevo.model_dump())
    return {"mensaje": "Registrado con éxito", "item": nuevo}

# PATH OPERATION: PUT8

# 4. Actualizar stock
@app.put("/items/{item_id}", tags=["Escritura"])
async def actualizar_stock(
    item_id: Annotated[int, Path(gt=0)],
    nuevo_stock: Annotated[int, Body(ge=0, embed=True)]
):
    for item in inventario:
        if item["id"] == item_id:
            item["stock"] = nuevo_stock
            return {"mensaje": "Stock actualizado", "datos": item}
    raise HTTPException(status_code=404, detail="No se encontró el item")

# PATH OPERATION: DELETE

# 5. Eliminar componente
@app.delete("/items/{item_id}", tags=["Escritura"])
async def borrar_item(
    item_id: Annotated[int, Path(gt=0)]
):
    for i, item in enumerate(inventario):
        if item["id"] == item_id:
            eliminado = inventario.pop(i)
            return {"mensaje": "Eliminado", "item": eliminado}
    raise HTTPException(status_code=404, detail="ID no encontrado para eliminar")