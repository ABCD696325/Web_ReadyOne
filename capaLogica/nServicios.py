from capaDatos.dServicios import DServicios
from datetime import date

class NServicios:
    def __init__(self):
        self.datos = DServicios()

    # ========= VALIDACIONES =========

    def _validar_fecha(self, fecha):
        return fecha >= date.today()

    def _validar_pasajeros(self, numero):
        return numero > 0

    # ========= CRUD =========

    def listar(self):
        return self.datos.listar()

    def registrar(
        self,
        id_cliente,
        tipo_servicio,
        origen,
        destino,
        fecha_servicio,
        hora_servicio,
        pasajeros,
        tipo_viaje,
        ida_vuelta,
        observaciones
    ):
        if not self._validar_fecha(fecha_servicio):
            raise ValueError("No se permiten fechas pasadas")

        if not self._validar_pasajeros(pasajeros):
            raise ValueError("Número de pasajeros inválido")

        data = {
            "id_cliente": id_cliente,
            "tipo_servicio": tipo_servicio,
            "ciudad_origen": origen,
            "ciudad_destino": destino,
            "fecha_servicio": fecha_servicio.isoformat(),
            "hora_servicio": hora_servicio.strftime("%H:%M:%S"),
            "numero_pasajeros": pasajeros,
            "tipo_viaje": tipo_viaje,
            "ida_vuelta": ida_vuelta,
            "observaciones_cliente": observaciones,
            "estado_servicio": "SOLICITADO"
        }

        return self.datos.insertar(data)

    def actualizar(
        self,
        id_servicio,
        data
    ):
        return self.datos.actualizar(id_servicio, data)

    def eliminar(self, id_servicio):
        return self.datos.eliminar(id_servicio)
