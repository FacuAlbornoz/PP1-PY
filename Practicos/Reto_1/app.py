from fastapi import FastAPI

app = FastAPI()

# METODO: Crear un endpoint para cada método HTTP (GET, POST, PUT, DELETE) que devuelva un mensaje de saludo diferente para cada uno.

@app.get("/Saludo/get")
async def saludar():
    return {"Hola": "!Get¡"}

@app.post("/Saludo/post")
async def saludar():
    return {"Hola": "!Post¡"}

@app.put("/Saludo/put")
async def saludar():
    return {"Hola": "!Put¡"}

@app.delete("/Saludo/delete")
async def saludar():
    return {"Hola": "!Delete¡"}