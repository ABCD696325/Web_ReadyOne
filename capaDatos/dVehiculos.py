from conexion import ConexionDB

class DVehiculos:
    def __init__(self):
        self.db = ConexionDB().conectar()
        self.tabla = "vehiculos"

    def listar(self):
        return self.db.table(self.tabla).select("*").execute().data

    def insertar(self, data):
        return self.db.table(self.tabla).insert(data).execute()

    def actualizar(self, id_vehiculo, data):
        return (
            self.db.table(self.tabla)
            .update(data)
            .eq("id_vehiculo", id_vehiculo)
            .execute()
        )

    def eliminar(self, id_vehiculo):
        return (
            self.db.table(self.tabla)
            .delete()
            .eq("id_vehiculo", id_vehiculo)
            .execute()
        )
