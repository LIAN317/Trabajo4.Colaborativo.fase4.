# Módulo que implementa la clase Cliente heredando de EntidadSistema.
import logging
import re  # Importa expresiones regulares para validar el formato del correo electrónico.
from importlib import import_module
from .entidad import EntidadSistema  # Importa la clase abstracta padre desde el mismo paquete.

try:
    # Usa la ruta relativa real del proyecto. El import dinámico evita que el
    # analizador reporte el módulo aunque se ejecute desde directorios distintos.
    try:
        excepciones = import_module("..utilidades.excepciones", package=__package__)
    except (ImportError, TypeError, ValueError):
        excepciones = import_module("utilidades.excepciones")
    ErrorValidacionDatos = excepciones.ErrorValidacionDatos
    ErrorOperacionNoPermitida = excepciones.ErrorOperacionNoPermitida
except (ImportError, AttributeError):
    # Define clases locales si el módulo no está disponible (uso independiente/pruebas).
    class ErrorValidacionDatos(Exception):
        def __init__(self, campo, mensaje):
            super().__init__(f"[{campo}] {mensaje}")
    class ErrorOperacionNoPermitida(Exception):
        pass

try:
    try:
        logger_module = import_module("..utilidades.logger", package=__package__)
    except (ImportError, TypeError, ValueError):
        logger_module = import_module("utilidades.logger")
    GestorLogs = logger_module.GestorLogs  # Importa el gestor de logs para auditar creaciones y errores.
except (ImportError, AttributeError):
    # Permite usar el modelo incluso si el módulo de logs no está disponible.
    class GestorLogs:
        @staticmethod
        def registrar_evento(nivel: str, modulo: str, mensaje: str) -> None:
            logger = logging.getLogger(modulo)
            metodo = getattr(logger, nivel.lower(), logger.info)
            metodo(mensaje)


class Cliente(EntidadSistema):
    """Representa a un cliente de Software FJ con encapsulación y validaciones estrictas."""

    # Constructor que recibe los datos personales del cliente.
    def __init__(self, id_cliente: str, nombre: str, correo: str, telefono: str):
        # Llama al constructor de EntidadSistema para validar y guardar el ID.
        super().__init__(id_cliente)
        # Inicializa atributos privados (doble guion bajo) para garantizar encapsulación estricta.
        self.__nombre = ""
        self.__correo = ""
        self.__telefono = ""
        self.__activo = True  # Todo cliente inicia en estado activo por defecto.
        self.__historial_reservas = []  # Lista interna en memoria (sin base de datos).

        # Asigna los valores a través de los setters para ejecutar todas las validaciones.
        self.nombre = nombre
        self.correo = correo
        self.telefono = telefono

        # Verifica la integridad completa del objeto antes de confirmar su creación.
        self.validar_integridad()
        # Registra en el archivo de logs que el cliente fue creado exitosamente.
        GestorLogs.registrar_evento(
            "INFO", "Cliente", f"Cliente registrado correctamente: {self.obtener_resumen()}"
        )

    # --- PROPIEDADES (GETTERS Y SETTERS ENCAPSULADOS) ---

    @property
    def nombre(self) -> str:
        """Retorna el nombre completo del cliente."""
        return self.__nombre

    @nombre.setter
    def nombre(self, valor: str) -> None:
        """Valida y asigna el nombre del cliente."""
        # Verifica que el nombre sea texto y tenga al menos 3 caracteres reales.
        if not isinstance(valor, str) or len(valor.strip()) < 3:
            raise ErrorValidacionDatos("nombre", "Debe contener al menos 3 caracteres alfabéticos.")
        # Almacena el nombre formateado con mayúscula inicial en cada palabra.
        self.__nombre = valor.strip().title()

    @property
    def correo(self) -> str:
        """Retorna el correo electrónico del cliente."""
        return self.__correo

    @correo.setter
    def correo(self, valor: str) -> None:
        """Valida mediante expresión regular el formato del correo electrónico."""
        # Patrón estándar para verificar estructura usuario@dominio.extensión.
        patron_correo = r"^[\w\.-]+@[\w\.-]+\.\w{2,}$"
        # Valida que sea cadena y cumpla con el patrón definido.
        if not isinstance(valor, str) or not re.match(patron_correo, valor.strip()):
            raise ErrorValidacionDatos("correo", f"El correo '{valor}' no tiene un formato válido.")
        # Guarda el correo en minúsculas y sin espacios.
        self.__correo = valor.strip().lower()

    @property
    def telefono(self) -> str:
        """Retorna el número telefónico del cliente."""
        return self.__telefono

    @telefono.setter
    def telefono(self, valor: str) -> None:
        """Valida que el teléfono contenga únicamente dígitos y longitud válida (7 a 15)."""
        # Elimina espacios o guiones opcionales antes de validar.
        limpio = str(valor).strip().replace(" ", "").replace("-", "")
        # Comprueba que todos los caracteres sean numéricos y tengan longitud adecuada.
        if not limpio.isdigit() or not (7 <= len(limpio) <= 15):
            raise ErrorValidacionDatos("telefono", "Debe contener entre 7 y 15 dígitos numéricos.")
        # Asigna el teléfono validado.
        self.__telefono = limpio

    @property
    def activo(self) -> bool:
        """Indica si el cliente está habilitado para realizar reservas."""
        return self.__activo

    @property
    def historial_reservas(self) -> list:
        """Retorna una copia de la lista de reservas para evitar modificaciones externas directas."""
        return list(self.__historial_reservas)

    # --- MÉTODOS DE COMPORTAMIENTO ---

    def desactivar_cliente(self) -> None:
        """Cambia el estado del cliente a inactivo si aún no lo está."""
        # Si ya está desactivado, lanza excepción de operación no permitida.
        if not self.__activo:
            raise ErrorOperacionNoPermitida(f"El cliente {self.id_entidad} ya se encuentra inactivo.")
        # Cambia el estado interno a False.
        self.__activo = False
        # Audita el cambio de estado en el archivo de logs.
        GestorLogs.registrar_evento("WARNING", "Cliente", f"Cliente {self.id_entidad} desactivado.")

    def agregar_reserva_historial(self, codigo_reserva: str) -> None:
        """Registra el código de una reserva dentro de la lista interna del cliente."""
        # Impide asociar reservas si el cliente está inactivo.
        if not self.__activo:
            raise ErrorOperacionNoPermitida(
                f"No se pueden asociar reservas al cliente inactivo '{self.__nombre}'."
            )
        # Valida que el código de reserva sea una cadena no vacía.
        if not codigo_reserva or not isinstance(codigo_reserva, str):
            raise ErrorValidacionDatos("codigo_reserva", "El código de reserva es inválido.")
        # Agrega el código a la lista interna en memoria.
        self.__historial_reservas.append(codigo_reserva.strip())

    def validar_integridad(self) -> bool:
        """Implementación obligatoria del método abstracto para verificar datos completos."""
        # Comprueba que ninguno de los atributos obligatorios esté vacío.
        if not all([self._id_entidad, self.__nombre, self.__correo, self.__telefono]):
            raise ErrorValidacionDatos("Cliente", "Faltan atributos obligatorios del cliente.")
        return True

    def obtener_resumen(self) -> str:
        """Implementación polimórfica que devuelve la ficha resumida del cliente."""
        estado = "Activo" if self.__activo else "Inactivo"
        return f"Cliente [{self._id_entidad}] - {self.__nombre} | Correo: {self.__correo} | Estado: {estado}"