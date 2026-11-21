# Módulo de excepciones personalizadas para el sistema de Software FJ.

class ErrorSistemaFJ(Exception):
    """Clase base para todas las excepciones controladas del sistema Software FJ."""
    # Constructor que recibe el mensaje descriptivo del error ocurrido.
    def __init__(self, mensaje: str):
        # Llama al constructor de la clase padre Exception con el mensaje.
        super().__init__(mensaje)
        # Almacena el mensaje como atributo de instancia para consultas posteriores.
        self.mensaje = mensaje


class ErrorValidacionDatos(ErrorSistemaFJ):
    """Excepción lanzada cuando los datos ingresados por el usuario son inválidos o faltantes."""
    # Constructor que recibe el campo afectado y el detalle del error.
    def __init__(self, campo: str, detalle: str):
        # Construye un mensaje formateado indicando exactamente qué campo falló.
        mensaje_completo = f"Error de validación en el campo '{campo}': {detalle}"
        # Inicializa la excepción base con el mensaje construido.
        super().__init__(mensaje_completo)


class ErrorOperacionNoPermitida(ErrorSistemaFJ):
    """Excepción lanzada cuando se intenta ejecutar una acción inválida sobre una entidad."""
    pass


class ErrorServicioNoDisponible(ErrorSistemaFJ):
    """Excepción lanzada cuando un servicio no existe o no tiene disponibilidad."""
    pass


class ErrorReservaInvalida(ErrorSistemaFJ):
    """Excepción lanzada ante inconsistencias en el proceso o estado de una reserva."""
    pass