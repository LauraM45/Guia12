# controlador/gestor.py
"""
Controlador: orquesta llamadas entre la vista y el modelo.
Valida datos y prepara mensajes de retorno.
"""

from modelo import estudiante as mod
from typing import List, Tuple

def inicializar():
    mod.crear_base()

def agregar_estudiante(nombre: str, edad: str, nota: str, id_curso: str = None) -> Tuple[bool, str]:
    # Validaciones simples
    if not nombre.strip():
        return False, "El nombre no puede estar vacío."
    try:
        nota_f = float(nota)
    except ValueError:
        return False, "Nota inválida. Use un número (ej. 4.5)."
    try:
        edad_i = int(edad) if edad != "" else None
    except ValueError:
        return False, "Edad inválida."
    try:
        idc = int(id_curso) if id_curso not in (None, "", "None") else None
    except ValueError:
        idc = None
    new_id = mod.insertar_estudiante(nombre.strip(), edad_i, nota_f, idc)
    return True, f"Estudiante agregado con id {new_id}."

def listar() -> List[Tuple]:
    return mod.listar_estudiantes()

def actualizar_nota(nombre: str, nueva_nota: str) -> Tuple[bool, str]:
    try:
        n = float(nueva_nota)
    except ValueError:
        return False, "Nota inválida."
    filas = mod.actualizar_nota_por_nombre(nombre, n)
    if filas == 0:
        return False, "No se encontró estudiante con ese nombre."
    return True, f"Se actualizaron {filas} registro(s)."

def eliminar_por_nota(umbral: str) -> Tuple[bool, str]:
    try:
        u = float(umbral)
    except ValueError:
        return False, "Valor inválido."
    filas = mod.eliminar_por_nota_minima(u)
    return True, f"Se eliminaron {filas} registro(s) con nota < {u}."

def buscar(patron: str):
    return mod.buscar_por_nombre_like(patron)

def ordenar_desc():
    return mod.ordenar_por_nota_desc()

def importar_csv(path: str) -> Tuple[bool, str]:
    try:
        inserted = mod.importar_csv_a_db(path)
        return True, f"{inserted} registros importados desde {path}."
    except FileNotFoundError:
        return False, f"Archivo no encontrado: {path}"
    except Exception as e:
        return False, f"Error al importar: {e}"
