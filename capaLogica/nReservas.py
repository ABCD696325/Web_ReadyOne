from capaDatos.dReservas import DReservas


class NReservas:
    def __init__(self):
        self.datos = DReservas()

    # ========= VALIDACIONES =========

    def _validar_estado(self, estado):
        return estado in [
            "PENDIENTE",
            "CONFIRMADA",
            "EN_PROCESO",
            "FINALIZADA",
            "CANCELADA"
        ]

    # ========= CRUD =========

    def listar(self):
        return self.datos.listar()

    def registrar(
        self,
        id_cliente,
        id_servicio,
        id_vehiculo,
        id_conductor,
        metodo_pago,
        monto,
        estado,
        observaciones
    ):
        if not self._validar_estado(estado):
            raise ValueError("Estado inválido")

        data = {
            "id_cliente": id_cliente,
            "id_servicio": id_servicio,
            "id_vehiculo": id_vehiculo,
            "id_conductor": id_conductor,
            "metodo_pago": metodo_pago,
            "monto_total": float(monto),
            "estado": estado,
            "observaciones": observaciones
        }

        return self.datos.insertar(data)

    def eliminar(self, id_reserva):
        return self.datos.eliminar(id_reserva)
