#? API REST: Interfaz de Programación de Aplicaiones para compartir recursos
from pydantic import BaseModel
from typing import List, Optional
from fastapi import FastAPI
import uuid
from fastapi import HTTPException

# Inicializamos una variable donde tendrá todas las características de una  API REST 
app = FastAPI()

#? Aca se define el modelo
class Curso(BaseModel):
    id: Optional[str] = None
    nombre: str
    descripcion: Optional[str] = None
    nivel: str
    duracion:int


#? Simularemos una Base de Datos
curso_db = []

#? CRUD: Read (lectura) GET ALL: Leeremos todos cursos que haya en la db

@app.get('/cursos', response_model=list[Curso])
def obtener_cursos():
    return curso_db


#? CRUD: Create (crear) POST: Crearemos un nuevo curso

@app.post('/cursos', response_model=Curso)
def crear_curso(curso: Curso):
    curso.id = str(uuid.uuid4())
    curso_db.append(curso)
    return curso

#? CRUD: Read (lectura) GET (individualo): Leeremos el cursos que coincida con el ID que pidamos en la db

@app.get('/cursos/{curso_id}', response_model=Curso)
def obtener_curso(curso_id: str):
    curso = next((curso for curso in curso_db if curso.id == curso_id), None)  #? Con next tomamos la primera coincidencia del array devuelto
    if curso is None:
        raise HTTPException(status_code=404, detail='Curso no encontrado')
    return curso


#? CRUD: Update (Actualizar/Modoficar) PUT: Modificar un Registro

@app.put('/cursos/{curso_id}', response_model=Curso)
def actualizar_curso(curso_id: str, curso_actualizado: Curso):
    curso = next((curso for curso in curso_db if curso.id == curso_id))
    if curso is None:
        raise HTTPException(status_code=404, detail='Curso no encontrado')
    curso_actualizado.id = curso_id
    index = curso_db.index(curso)
    curso_db[index] = curso_actualizado
    return curso_actualizado

    
# @app.put('/cursos/{curso_id}', response_model=Curso)
# def actualizar_curso(curso_id: str, curso: Curso):
#     curso_actualizado = next((curso for curso in curso_db if curso.id == curso_id))
#     if curso_actualizado is None:
#         raise HTTPException(status_code=404, detail='Curso no encontrado')
#         curso_actualizado.id = curso_id
#         curso_actualizado.nombre = curso.nombre
#         curso_actualizado.descripcion = curso.descripcion
#         curso_actualizado.nivel = curso.nivel
#         curso_actualizado.duracion = curso.duracion
#         return curso_actualizado


#? CRUD: Delete (Eliminar) DELETE: Eliminar un Registro

@app.delete('/cursos/{curso_id}', response_model=Curso)
def eliminar_curso(curso_id: str):
    curso = next((curso for curso in curso_db if curso.id == curso_id))
    if curso is None:
        raise HTTPException(status_code=404, detail='Curso no encontrado')
    curso_db.remove(curso)
    return curso









