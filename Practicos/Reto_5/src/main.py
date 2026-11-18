from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routers.marca import marcas_routers
from routers.producto import productos_routers

app = FastAPI()

app.title = "tiendaZapatillas"

app.include_router(productos_routers, tags=["Productos"], prefix="/productos")
app.include_router(marcas_routers, tags=["Marcas"], prefix="/marcas")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:5500",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
