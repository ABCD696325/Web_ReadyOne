from capaDatos.dConductores import DConductores

class NConductores:
    def __init__(self):
        self.datos = DConductores()

    # ========= VALIDACIONES =========

    def _validar_telefono(self, telefono):
        return telefono.isdigit() and len(telefono) == 9

    def _validar_licencia(self, licencia):
        return len(licencia) >= 8

    # ========= CRUD =========

    def listar(self):
        return self.datos.listar()

    def registrar(
        self,
        nombres,
        apellidos,
        licencia,
        telefono,
        tiene_papeletas,
        estado
    ):
        if not nombres or not apellidos:
            raise ValueError("Nombres y apellidos son obligatorios")

        if not self._validar_licencia(licencia):
            raise ValueError("Licencia inválida")

        if not self._validar_telefono(telefono):
            raise ValueError("Teléfono inválido")

        data = {
            "nombres": nombres,
            "apellidos": apellidos,
            "licencia": licencia,
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
        licencia,
        telefono,
        tiene_papeletas,
        estado
    ):
        data = {
            "nombres": nombres,
            "apellidos": apellidos,
            "licencia": licencia,
            "telefono": telefono,
            "tiene_papeletas": tiene_papeletas,
            "estado": estado
        }

        return self.datos.actualizar(id_conductor, data)

    def eliminar(self, id_conductor):
        return self.datos.eliminar(id_conductor)
