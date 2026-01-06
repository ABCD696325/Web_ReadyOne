from capaDatos.dReservas import DReservas

class NReservas:
    def __init__(self):
        self.datos = DReservas()

    def listar(self):
        return self.datos.listar()

    def registrar(self, id_cliente, precio, estado, observaciones):
        data = {
            "id_cliente": id_cliente,
            "precio": float(precio),
            "estado": estado,
            "observaciones": observaciones
        }
        return self.datos.insertar(data)

    def eliminar(self, id_reserva):
        return self.datos.eliminar(id_reserva)
