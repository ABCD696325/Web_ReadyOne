from conexion import ConexionDB

class DConductores:
    def __init__(self):
        self.db = ConexionDB().conectar()
        self.tabla = "conductores"

    def listar(self):
        response = self.db.table(self.tabla).select("*").execute()
        return response.data

    def insertar(self, data):
        return self.db.table(self.tabla).insert(data).execute()

    def actualizar(self, id_conductor, data):
        return (
            self.db.table(self.tabla)
            .update(data)
            .eq("id_conductor", id_conductor)
            .execute()
        )

    def eliminar(self, id_conductor):
        return (
            self.db.table(self.tabla)
            .delete()
            .eq("id_conductor", id_conductor)
            .execute()
        )
