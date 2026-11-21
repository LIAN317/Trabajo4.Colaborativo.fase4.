# Módulo que define la clase abstracta base para todas las entidades de Software FJ.

from abc import ABC, abstractmethod
from datetime import datetime

try:
    # Importación relativa cuando el proyecto se ejecuta como paquete.
    from ..utilidades.excepciones import ErrorValidacionDatos  # type: ignore[import-not-found]
except (ImportError, ValueError):
    # Importación absoluta cuando la raíz del proyecto está en sys.path.
    from utilidades.excepciones import ErrorValidacionDatos  # type: ignore[import-not-found]


class EntidadSistema(ABC):
    """Clase abstracta que representa cualquier entidad general del sistema."""

    def __init__(self, id_entidad: str):

        # Validar que el identificador sea un texto válido.
        if not isinstance(id_entidad, str) or not id_entidad.strip():
            raise ErrorValidacionDatos(
                "id_entidad",
                "El identificador no puede estar vacío y debe ser texto."
            )

        # Guardar el identificador sin espacios innecesarios.
        self._id_entidad = id_entidad.strip()

        # Registrar fecha y hora de creación.
        self._fecha_creacion = datetime.now()

    @property
    def id_entidad(self) -> str:
        """Permite consultar el identificador."""
        return self._id_entidad

    @property
    def fecha_creacion(self) -> datetime:
        """Permite consultar la fecha de creación."""
        return self._fecha_creacion

    @abstractmethod
    def validar_integridad(self) -> bool:
        """Obliga a las clases hijas a validar sus propios datos."""
        pass

    @abstractmethod
    def obtener_resumen(self) -> str:
        """Permite representar cada entidad mediante un resumen."""
        pass