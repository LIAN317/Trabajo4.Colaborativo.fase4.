# Script de prueba inicial para validar la arquitectura base y la clase Cliente.
import sys
from pathlib import Path

# Permite ejecutar main.py desde cualquier directorio sin perder la carpeta del proyecto.
sys.path.insert(0, str(Path(__file__).resolve().parent))

import modelos.cliente  # type: ignore[import-not-found]  # Importa la clase Cliente.
from utilidades.excepciones import ErrorSistemaFJ  # type: ignore[import-not-found]  # Importa la excepción base del sistema.
from utilidades.logger import GestorLogs  # type: ignore[import-not-found]  # Importa el registrador de logs.


def probar_modulo_base():
    """Ejecuta casos válidos e inválidos de clientes para comprobar estabilidad y logs."""
    print("=== INICIANDO PRUEBAS DE ARQUITECTURA BASE (ESTUDIANTE 1) ===\n")

    # Caso 1: Registro válido de un cliente.
    try:
        cliente1 = modelos.cliente.Cliente("CLI-001", "camila selena gomez", "camila.gomez@correo.com", "3501931167")
        print("[OK] Cliente creado:", cliente1.obtener_resumen())
    except ErrorSistemaFJ as error:
        GestorLogs.registrar_evento("ERROR", "MainPrueba", str(error))
        print("[ERROR CONTROLADO]:", error)

    # Caso 2: Registro inválido por correo mal formado (debe capturar error y seguir ejecutando).
    try:
        cliente_invalido = modelos.cliente.Cliente("CLI-002", "Camilo Ruiz", "correo-sin-arroba.com", "3239876993")
    except ErrorSistemaFJ as error:
        GestorLogs.registrar_evento("ERROR", "MainPrueba", str(error))
        print("[ERROR CONTROLADO]:", error)

    # Caso 3: Registro inválido por teléfono corto.
    try:
        cliente_tel_malo = modelos.cliente.Cliente("CLI-003", "Lucas Paez", "lucas@empresa.co", "1234")
    except ErrorSistemaFJ as error:
        GestorLogs.registrar_evento("ERROR", "MainPrueba", str(error))
        print("[ERROR CONTROLADO]:", error)

    print("\n=== PRUEBAS FINALIZADAS SIN INTERRUPCIONES (Revisa logs/sistema.log) ===")


if __name__ == "__main__":
    probar_modulo_base()