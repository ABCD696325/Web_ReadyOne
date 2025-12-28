from capaDatos.dReservas import DReservas
from datetime import date

class NReservas:
    def __init__(self):
        self.datos = DReservas()

    # ===== VALIDACIONES =====

    def _validar_fecha(self, fecha):
        return fecha >= date.today()

    def _validar_estado(self, estado):
        return estado in [
            "PENDIENTE",
            "CONFIRMADA",
            "EN_PROCESO",
            "FINALIZADA",
            "CANCELADA"
        ]

    # ===== CRUD =====

    def listar(self):
        return self.datos.listar()

    def registrar(
        self,
        id_cliente,
        id_servicio,
        id_vehiculo,
        id_conductor,
        fecha_reserva,
        metodo_pago,
        monto,
        estado,
        observaciones
    ):
        if not self._validar_fecha(fecha_reserva):
            raise ValueError("La fecha de reserva no puede ser pasada")

        if not self._validar_estado(estado):
            raise ValueError("Estado de reserva inválido")

        data = {
            "id_cliente": id_cliente,
            "id_servicio": id_servicio,
            "id_vehiculo": id_vehiculo,
            "id_conductor": id_conductor,
            "fecha_reserva": fecha_reserva.isoformat(),
            "metodo_pago": metodo_pago,
            "monto_total": float(monto),
            "estado_reserva": estado,
            "observaciones": observaciones
        }

        return self.datos.insertar(data)

    def actualizar(self, id_reserva, data):
        return self.datos.actualizar(id_reserva, data)

    def eliminar(self, id_reserva):
        return self.datos.eliminar(id_reserva)
