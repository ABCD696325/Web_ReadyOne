from conexion import ConexionDB

class DClientes:
    def __init__(self):
        self.db = ConexionDB().conectar()
        self.tabla = "clientes"

    def listar(self):
        return self.db.table(self.tabla).select("*").execute().data

    def insertar(self, data):
        return self.db.table(self.tabla).insert(data).execute()

    def actualizar(self, id_cliente, data):
        return (
            self.db.table(self.tabla)
            .update(data)
            .eq("id_cliente", id_cliente)
            .execute()
        )

    def eliminar(self, id_cliente):
        return (
            self.db.table(self.tabla)
            .delete()
            .eq("id_cliente", id_cliente)
            .execute()
        )
