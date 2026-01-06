from capaDatos.dVehiculos import DVehiculos

class NVehiculos:
    def __init__(self):
        self.datos = DVehiculos()

    # ========= VALIDACIONES =========

    def _validar_placa(self, placa):
        return placa and len(placa) >= 6

    def _validar_capacidad(self, capacidad):
        return capacidad >= 4

    # ========= CRUD =========

    def listar(self):
        return self.datos.listar()

    def registrar(self, placa, marca, modelo, capacidad, estado):
        if not self._validar_placa(placa):
            raise ValueError("La placa debe tener al menos 6 caracteres")

        if not self._validar_capacidad(capacidad):
            raise ValueError("La capacidad mínima es 4 pasajeros")

        if not marca.strip() or not modelo.strip():
            raise ValueError("Marca y modelo son obligatorios")

        data = {
            "placa": placa.upper(),
            "marca": marca,
            "modelo": modelo,
            "capacidad": capacidad,
            "estado": estado
        }

        return self.datos.insertar(data)

    def actualizar(self, id_vehiculo, placa, marca, modelo, capacidad, estado):
        if not self._validar_capacidad(capacidad):
            raise ValueError("Capacidad mínima 4 pasajeros")

        data = {
            "placa": placa.upper(),
            "marca": marca,
            "modelo": modelo,
            "capacidad": capacidad,
            "estado": estado
        }

        return self.datos.actualizar(id_vehiculo, data)

    def eliminar(self, id_vehiculo):
        return self.datos.eliminar(id_vehiculo)
