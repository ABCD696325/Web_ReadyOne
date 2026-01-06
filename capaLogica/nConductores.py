from capaDatos.dConductores import DConductores

class NConductores:
    def __init__(self):
        self.datos = DConductores()

    def listar(self):
        return self.datos.listar()

    def registrar(self, nombres, apellidos, telefono, estado="ACTIVO"):
        if not telefono.isdigit() or len(telefono) != 9:
            raise ValueError("El teléfono debe tener 9 dígitos numéricos")

        if estado not in ["ACTIVO", "INACTIVO"]:
            raise ValueError("Estado debe ser ACTIVO o INACTIVO")

        return self.datos.insertar(
            nombres,
            apellidos,
            telefono,
            estado
        )

    def actualizar(self, id_conductor, nombres, apellidos, telefono, estado):
        if not telefono.isdigit() or len(telefono) != 9:
            raise ValueError("El teléfono debe tener 9 dígitos numéricos")

        return self.datos.actualizar(
            id_conductor,
            nombres,
            apellidos,
            telefono,
            estado
        )

    def eliminar(self, id_conductor):
        return self.datos.eliminar(id_conductor)
