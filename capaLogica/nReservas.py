from capaDatos.dReservas import DReservas


class NReservas:
    def __init__(self):
        self.datos = DReservas()

    def listar(self):
        return self.datos.listar()

    def registrar(
        self,
        id_cliente,
        id_vehiculo,
        metodo_pago,
        monto,
        estado,
        observaciones
    ):
        data = {
            "id_cliente": id_cliente,
            "id_vehiculo": id_vehiculo,
            "metodo_pago": metodo_pago,
            "monto_total": float(monto),
            "estado": estado,
            "observaciones": observaciones
        }

        return self.datos.insertar(data)

    def eliminar(self, id_reserva):
        return self.datos.eliminar(id_reserva)
