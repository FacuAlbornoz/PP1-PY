from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Path
from sqlmodel import Session, select

from database import get_db
from models.anidados import MarcaNested
from models.marca import Marca, MarcaBase, MarcaPublic

marcas_routers = APIRouter()

NO_ENCONTRADO = {
    404: {
        "description": "Marca no encontrada",
        "content": {
            "application/json": {
                "example": {
                    "detail": "Marca no encontrada",
                }
            }
        },
    },
}


@marcas_routers.get("/", response_model=list[MarcaNested])
async def getMarcas(db: Session = Depends(get_db)):
    marcas = db.exec(select(Marca)).all()
    return marcas


@marcas_routers.get(
    "/{id}",
    response_model=MarcaNested,
    responses=NO_ENCONTRADO,
)
async def obtenerMarcaId(
    id: Annotated[int, Path(gt=0)],
    db: Session = Depends(get_db),
):
    marca_obtenida = db.get(Marca, id)
    if marca_obtenida is not None:
        return marca_obtenida
    raise HTTPException(status_code=404, detail="Marca no encontrada")


@marcas_routers.post("/", response_model=MarcaPublic)
async def crearMarca(marca: MarcaBase, db: Session = Depends(get_db)):
    nueva_marca = Marca.model_validate(marca)
    db.add(nueva_marca)
    db.commit()
    db.refresh(nueva_marca)
    return nueva_marca
