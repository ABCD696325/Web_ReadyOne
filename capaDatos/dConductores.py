from capaDatos.dConductores import DConductores

class NConductores:
    def __init__(self):
        self.datos = DConductores()

    def listar(self):
        return self.datos.listar()

    def registrar(
        self,
        nombres,
        apellidos,
        telefono,
        tiene_papeletas=False,
        estado="ACTIVO"
    ):
        if not estado:
            estado = "ACTIVO"

        data = {
            "nombres": nombres,
            "apellidos": apellidos,
            "telefono": telefono,
            "tiene_papeletas": tiene_papeletas,
            "estado": estado
        }

        return self.datos.insertar(data)

    def actualizar(
        self,
        id_conductor,
        nombres,
        apellidos,
        telefono,
        tiene_papeletas,
        estado
    ):
        data = {
            "nombres": nombres,
            "apellidos": apellidos,
            "telefono": telefono,
            "tiene_papeletas": tiene_papeletas,
            "estado": estado
        }

        return self.datos.actualizar(id_conductor, data)

    def eliminar(self, id_conductor):
        return self.datos.eliminar(id_conductor)
