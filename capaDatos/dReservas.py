from conexion import ConexionDB


class DReservas:
    def __init__(self):
        self.db = ConexionDB().conectar()
        self.tabla = "reservas"

    def listar(self):
        return self.db.table(self.tabla).select("*").execute().data

    def insertar(self, data):
        return self.db.table(self.tabla).insert(data).execute()

    def eliminar(self, id_reserva):
        return (
            self.db.table(self.tabla)
            .delete()
            .eq("id_reserva", id_reserva)
            .execute()
        )
