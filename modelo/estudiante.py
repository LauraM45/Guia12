# modelo/estudiante.py
"""
Funciones de acceso a datos para el Gestor de Estudiantes.
Responsabilidad única: todo lo relacionado con sqlite3 y persistencia.
"""

from pathlib import Path
import sqlite3
import csv
from typing import List, Tuple, Optional

DB_PATH = Path("gestor_estudiantes_mvc") / "estudiantes.db"

def conectar():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    con = sqlite3.connect(DB_PATH.as_posix())
    return con

def crear_base():
    """Crea la base y la tabla estudiantes si no existen."""
    con = conectar()
    cur = con.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS estudiantes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        edad INTEGER,
        nota REAL,
        id_curso INTEGER
    )
    """)
    con.commit()
    con.close()

def insertar_estudiante(nombre: str, edad: Optional[int], nota: float, id_curso: Optional[int]=None) -> int:
    """Inserta un estudiante y devuelve el id."""
    con = conectar()
    cur = con.cursor()
    cur.execute("INSERT INTO estudiantes (nombre, edad, nota, id_curso) VALUES (?, ?, ?, ?)",
                (nombre, edad, nota, id_curso))
    con.commit()
    lid = cur.lastrowid
    con.close()
    return lid

def listar_estudiantes() -> List[Tuple]:
    """Devuelve todos los estudiantes."""
    con = conectar()
    cur = con.cursor()
    cur.execute("SELECT id, nombre, edad, nota, id_curso FROM estudiantes")
    rows = cur.fetchall()
    con.close()
    return rows

def actualizar_nota_por_nombre(nombre: str, nueva_nota: float) -> int:
    """Actualiza la nota de estudiantes con el nombre dado. Devuelve número de filas afectadas."""
    con = conectar()
    cur = con.cursor()
    cur.execute("UPDATE estudiantes SET nota = ? WHERE nombre = ?", (nueva_nota, nombre))
    con.commit()
    affected = cur.rowcount
    con.close()
    return affected

def eliminar_por_nota_minima(umbral: float) -> int:
    """Elimina estudiantes con nota menor que umbral. Devuelve filas eliminadas."""
    con = conectar()
    cur = con.cursor()
    cur.execute("DELETE FROM estudiantes WHERE nota < ?", (umbral,))
    con.commit()
    affected = cur.rowcount
    con.close()
    return affected

def buscar_por_nombre_like(patron: str) -> List[Tuple]:
    """Busca nombres que contengan la cadena patron (case-insensitive)."""
    con = conectar()
    cur = con.cursor()
    like_pat = f"%{patron}%"
    cur.execute("SELECT id, nombre, edad, nota, id_curso FROM estudiantes WHERE nombre LIKE ? COLLATE NOCASE", (like_pat,))
    rows = cur.fetchall()
    con.close()
    return rows

def ordenar_por_nota_desc() -> List[Tuple]:
    """Devuelve estudiantes ordenados por nota descendente."""
    con = conectar()
    cur = con.cursor()
    cur.execute("SELECT id, nombre, edad, nota, id_curso FROM estudiantes ORDER BY nota DESC")
    rows = cur.fetchall()
    con.close()
    return rows

def importar_csv_a_db(csv_path: str):
    """Importa registros desde un CSV con columnas: nombre,edad,nota,id_curso."""
    con = conectar()
    cur = con.cursor()
    inserted = 0
    with open(csv_path, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for r in reader:
            nombre = r.get("nombre") or r.get("Nombre")
            edad = r.get("edad") or r.get("Edad") or None
            nota = r.get("nota") or r.get("Nota") or 0.0
            id_curso = r.get("id_curso") or r.get("idCurso") or None
            # Convertir tipos con manejo simple
            try:
                edad = int(edad) if edad not in (None, '') else None
            except:
                edad = None
            try:
                nota = float(nota)
            except:
                nota = 0.0
            try:
                id_curso = int(id_curso) if id_curso not in (None, '') else None
            except:
                id_curso = None
            cur.execute("INSERT INTO estudiantes (nombre, edad, nota, id_curso) VALUES (?, ?, ?, ?)",
                        (nombre, edad, nota, id_curso))
            inserted += 1
    con.commit()
    con.close()
    return inserted
