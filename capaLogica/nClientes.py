import re
from capaDatos.dClientes import DClientes

class NClientes:
    def __init__(self):
        self.datos = DClientes()

    # ========= VALIDACIONES =========

    def _validar_dni(self, dni):
        return dni.isdigit() and len(dni) == 8

    def _validar_ruc(self, ruc):
        return (
            ruc.isdigit()
            and len(ruc) == 11
            and (ruc.startswith("10") or ruc.startswith("20"))
        )

    def _validar_correo(self, correo):
        patron = r"^[\w\.-]+@[\w\.-]+\.\w+$"
        return re.match(patron, correo)

    def _validar_telefono(self, telefono):
        return telefono.isdigit() and len(telefono) == 9

    # ========= CRUD =========

    def listar(self):
        return self.datos.listar()

    def registrar_persona_natural(
        self, nombres, apellidos, dni, telefono, correo
    ):
        if not self._validar_dni(dni):
            raise ValueError("DNI inválido")

        if not self._validar_telefono(telefono):
            raise ValueError("Teléfono inválido")

        if not self._validar_correo(correo):
            raise ValueError("Correo inválido")

        data = {
            "tipo_cliente": "PERSONA_NATURAL",
            "nombres": nombres,
            "apellidos": apellidos,
            "dni": dni,
            "telefono": telefono,
            "correo": correo
        }

        return self.datos.insertar(data)

    def registrar_persona_juridica(
        self, razon_social, ruc, telefono, correo
    ):
        if not self._validar_ruc(ruc):
            raise ValueError("RUC inválido")

        if not self._validar_telefono(telefono):
            raise ValueError("Teléfono inválido")

        if not self._validar_correo(correo):
            raise ValueError("Correo inválido")

        data = {
            "tipo_cliente": "PERSONA_JURIDICA",
            "razon_social": razon_social,
            "ruc": ruc,
            "telefono": telefono,
            "correo": correo
        }

        return self.datos.insertar(data)

    def actualizar(self, id_cliente, data):
        return self.datos.actualizar(id_cliente, data)

    def eliminar(self, id_cliente):
        return self.datos.eliminar(id_cliente)
