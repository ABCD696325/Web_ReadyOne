from capaDatos.dVehiculos import DVehiculos

class NVehiculos:
    def __init__(self):
        self.datos = DVehiculos()

    def listar(self):
        return self.datos.listar()

    def registrar(self, placa, capacidad, estado):
        if not placa or len(placa) < 6:
            raise ValueError("La placa debe tener al menos 6 caracteres")

        if int(capacidad) < 4:
            raise ValueError("La capacidad mínima es 4 pasajeros")

        data = {
            "placa": placa.upper(),
            "capacidad": int(capacidad),
            "estado": estado
        }

        return self.datos.insertar(data)

    def actualizar(self, id_vehiculo, placa, capacidad, estado):
        data = {
            "placa": placa.upper(),
            "capacidad": int(capacidad),
            "estado": estado
        }

        return self.datos.actualizar(id_vehiculo, data)

    def eliminar(self, id_vehiculo):
        return self.datos.eliminar(id_vehiculo)
