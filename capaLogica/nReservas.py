from capaDatos.dReservas import DReservas

class NReservas:
    def __init__(self):
        self.datos = DReservas()

    def listar(self):
        return self.datos.listar()

    def registrar(self, id_cliente, estado, precio):
        if precio <= 0:
            raise ValueError("El precio debe ser mayor a 0")

        data = {
            "id_cliente": id_cliente,
            "estado": estado,
            "precio": float(precio)
        }

        return self.datos.insertar(data)

    def eliminar(self, id_reserva):
        return self.datos.eliminar(id_reserva)
