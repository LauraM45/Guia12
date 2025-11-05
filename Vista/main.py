# vista/main.py
"""
Interfaz por consola (vista). No debe tocar la base directamente; usa controlador.
"""

import sys
from Controlador import gestor

CSV_PRUEBA = "estudiantes.csv"

def generar_csv_prueba():
    import csv, os
    if os.path.exists(CSV_PRUEBA):
        return
    filas = [
        {"nombre":"Ana", "edad":"20", "nota":"4.7", "id_curso":"1"},
        {"nombre":"Juan", "edad":"22", "nota":"3.9", "id_curso":"1"},
        {"nombre":"Lucia", "edad":"19", "nota":"4.2", "id_curso":"2"},
        {"nombre":"Pedro", "edad":"21", "nota":"2.8", "id_curso":"2"},
    ]
    with open(CSV_PRUEBA, "w", newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=["nombre","edad","nota","id_curso"])
        writer.writeheader()
        writer.writerows(filas)

def imprimir_lista(lista):
    if not lista:
        print(" -> No hay registros.")
        return
    print(f"{'id':>3}  {'nombre':20} {'edad':>4} {'nota':>5} {'curso':>6}")
    print("-"*45)
    for r in lista:
        print(f"{r[0]:3}  {r[1]:20} {str(r[2]):>4} {r[3]:5.2f} {str(r[4]):>6}")

def menu():
    gestor.inicializar()
    generar_csv_prueba()
    print("Gestor de Estudiantes (MVC) - Menú")
    while True:
        print("\nOpciones:")
        print("1. Agregar estudiante")
        print("2. Listar estudiantes")
        print("3. Actualizar nota por nombre")
        print("4. Eliminar registros con nota menor que ...")
        print("5. Buscar por nombre (LIKE)")
        print("6. Mostrar ordenados por nota (desc)")
        print("7. Importar desde CSV")
        print("8. Salir")
        opt = input("Seleccione opción (1-8): ").strip()
        if opt == "1":
            nombre = input("Nombre: ")
            edad = input("Edad (enter para n/d): ")
            nota = input("Nota (ej. 4.0): ")
            idc = input("id_curso (opcional): ")
            ok, msg = gestor.agregar_estudiante(nombre, edad, nota, idc)
            print(msg)
        elif opt == "2":
            rows = gestor.listar()
            imprimir_lista(rows)
        elif opt == "3":
            nombre = input("Nombre del estudiante a actualizar: ")
            nota = input("Nueva nota: ")
            ok, msg = gestor.actualizar_nota(nombre, nota)
            print(msg)
        elif opt == "4":
            umbral = input("Eliminar si nota < (ej. 3.0): ")
            ok, msg = gestor.eliminar_por_nota(umbral)
            print(msg)
        elif opt == "5":
            patron = input("Cadena a buscar en nombre: ")
            rows = gestor.buscar(patron)
            imprimir_lista(rows)
        elif opt == "6":
            rows = gestor.ordenar_desc()
            imprimir_lista(rows)
        elif opt == "7":
            path = input(f"Ruta CSV (enter para usar {CSV_PRUEBA}): ").strip() or CSV_PRUEBA
            ok, msg = gestor.importar_csv(path)
            print(msg)
        elif opt == "8":
            print("Saliendo...")
            sys.exit(0)
        else:
            print("Opción inválida. Intente de nuevo.")

if __name__ == "__main__":
    menu()
