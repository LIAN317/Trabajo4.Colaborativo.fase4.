# Módulo encargado de registrar eventos y errores en un archivo de texto plano (logs).
import os  # Importa el módulo os para gestionar rutas y creación de carpetas.
from datetime import datetime  # Importa datetime para estampar fecha y hora exacta en cada registro.


class GestorLogs:
    """Clase utilitaria para escribir eventos del sistema y trazas de errores en un archivo."""

    # Define la ruta por defecto donde se almacenará el archivo de registro.
    RUTA_ARCHIVO = os.path.join("logs", "sistema.log")

    @classmethod
    def _asegurar_directorio(cls) -> None:
        """Verifica si la carpeta 'logs' existe; si no, la crea automáticamente."""
        # Extrae el nombre del directorio a partir de la ruta configurada.
        directorio = os.path.dirname(cls.RUTA_ARCHIVO)
        # Comprueba si el directorio no existe en el sistema de archivos.
        if directorio and not os.path.exists(directorio):
            # Crea el directorio de forma segura.
            os.makedirs(directorio)

    @classmethod
    def registrar_evento(cls, tipo: str, origen: str, mensaje: str) -> None:
        """Escribe una línea formateada en el archivo de logs con manejo de errores de E/S."""
        # Garantiza que la carpeta de destino exista antes de abrir el archivo.
        cls._asegurar_directorio()
        # Obtiene la fecha y hora actual en formato legible (Año-Mes-Día Hora:Minuto:Segundo).
        marca_tiempo = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        # Formatea la línea de registro con nivel, módulo de origen y descripción.
        linea_log = f"[{marca_tiempo}] [{tipo.upper()}] [{origen}] -> {mensaje}\n"

        # Bloque try/except/finally para asegurar el cierre del archivo ante fallos de escritura.
        archivo = None  # Inicializa la variable del archivo en None.
        try:
            # Abre el archivo en modo 'a' (append/agregar al final) con codificación UTF-8.
            archivo = open(cls.RUTA_ARCHIVO, mode="a", encoding="utf-8")
            # Escribe la línea formateada dentro del archivo de logs.
            archivo.write(linea_log)
        except OSError as error_io:
            # Si falla el disco o los permisos, informa en consola sin detener el programa.
            print(f"CRÍTICO: No se pudo escribir en el archivo de logs: {error_io}")
        finally:
            # Verifica si el archivo fue abierto exitosamente antes de cerrarlo.
            if archivo is not None and not archivo.closed:
                # Cierra el flujo del archivo para liberar recursos del sistema.
                archivo.close()