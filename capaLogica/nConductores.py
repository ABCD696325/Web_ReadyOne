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
        estado="ACTIVO"   # valor por defecto
    ):
        if not estado:
            estado = "ACTIVO"

        return self.datos.registrar(
            nombres,
            apellidos,
            telefono,
            tiene_papeletas,
            estado
        )

    def actualizar(
        self,
        id_conductor,
        nombres,
        apellidos,
        telefono,
        tiene_papeletas=False,
        estado="ACTIVO"
    ):
        if not estado:
            estado = "ACTIVO"

        return self.datos.actualizar(
            id_conductor,
            nombres,
            apellidos,
            telefono,
            tiene_papeletas,
            estado
        )

    def eliminar(self, id_conductor):
        return self.datos.eliminar(id_conductor)
