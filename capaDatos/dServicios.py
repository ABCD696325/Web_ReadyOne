from conexion import ConexionDB

class DServicios:
    def __init__(self):
        self.db = ConexionDB().conectar()
        self.tabla = "servicios"

    def listar(self):
        response = self.db.table(self.tabla).select("*").execute()
        return response.data

    def insertar(self, data):
        return self.db.table(self.tabla).insert(data).execute()

    def actualizar(self, id_servicio, data):
        return (
            self.db.table(self.tabla)
            .update(data)
            .eq("id_servicio", id_servicio)
            .execute()
        )

    def eliminar(self, id_servicio):
        return (
            self.db.table(self.tabla)
            .delete()
            .eq("id_servicio", id_servicio)
            .execute()
        )
