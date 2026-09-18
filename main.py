"""Script principal del Sistema de Gestión de Citas Médicas MediSENA."""

from src.cita import CitaMedica
from src.gestion_datos import cargar_citas, guardar_citas

RUTA_DATOS = "data/citas.json"


def mostrar_menu():
    print("\n=== SISTEMA DE GESTIÓN DE CITAS MÉDICAS MEDISENA ===")
    print("1. Listar citas")
    print("2. Registrar nueva cita")
    print("3. Consultar total de ingresos proyectados")
    print("4. Salir")


def registrar_cita(citas: list):
    print("\n--- REGISTRO DE NUEVA CITA MÉDICA ---")
    id_cita = input("Ingrese el ID de la cita (ej: CIT-2026-01): ").strip()

    for item in citas:
        if item["id_cita"].upper() == id_cita.upper():
            print("Error: Ya existe una cita registrada con este ID.")
            return

    paciente = input("Ingrese el nombre completo del paciente: ").strip()
    especialidad = input("Ingrese la especialidad médica: ").strip()
    medico_asignado = input("Ingrese el nombre del médico asignado: ").strip()

    try:
        costo_consulta = float(input("Ingrese el costo de la consulta (COP): "))
        if costo_consulta < 0:
            print("Error: El costo no puede ser negativo.")
            return
    except ValueError:
        print("Error: El costo debe ser un número válido.")
        return

    urgencia_input = input("¿Es una cita de urgencia? (S/N): ").strip().lower()
    es_urgencia = urgencia_input in ["s", "si", "sí", "true", "1"]

    nueva_cita = CitaMedica(
        id_cita, paciente, especialidad, medico_asignado, costo_consulta, es_urgencia
    )
    citas.append(nueva_cita.a_diccionario())

    if guardar_citas(RUTA_DATOS, citas):
        print("Cita médica registrada y guardada exitosamente.")


def listar_citas(citas: list):
    print("\n--- LISTADO DE CITAS MÉDICAS REGISTRADAS ---")
    if not citas:
        print("No hay citas médicas registradas.")
        return

    print(
        f"{'ID CITA':<12} | {'PACIENTE':<22} | {'ESPECIALIDAD':<16} | {'MÉDICO':<20} | {'TIPO':<10} | {'COSTO FIN.'}"
    )
    print("-" * 95)
    for c in citas:
        tipo = "Urgencia" if c["es_urgencia"] else "Programada"
        costo_final = c.get("costo_final", c["costo_consulta"])
        print(
            f"{c['id_cita']:<12} | {c['paciente']:<22} | {c['especialidad']:<16} | {c['medico_asignado']:<20} | {tipo:<10} | ${costo_final:,.2f}"
        )


def consultar_total_ingresos(citas: list):
    total = sum(c.get("costo_final", c["costo_consulta"]) for c in citas)
    print(f"\nEl total de ingresos proyectados es: ${total:,.2f} COP")


def main():
    citas = cargar_citas(RUTA_DATOS)

    while True:
        mostrar_menu()
        opcion = input("Seleccione una opción (1-4): ").strip()

        if opcion == "1":
            listar_citas(citas)
        elif opcion == "2":
            registrar_cita(citas)
        elif opcion == "3":
            consultar_total_ingresos(citas)
        elif opcion == "4":
            print("\nSaliendo del sistema MediSENA.")
            break
        else:
            print("Opción no válida. Intente de nuevo.")


if __name__ == "__main__":
    main()