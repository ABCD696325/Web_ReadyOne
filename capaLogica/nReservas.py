from capaDatos.dReservas import DReservas
from datetime import date

class NReservas:
    def __init__(self):
        self.datos = DReservas()

    def listar(self):
        return self.datos.listar()

    def registrar(
        self,
        id_cliente,
        tipo_servicio,
        fecha_servicio,
        hora_servicio,
        ciudad_origen,
        ciudad_destino,
        numero_pasajeros,
        observaciones=""
    ):
        if fecha_servicio < date.today():
            raise ValueError("La fecha no puede ser pasada")

        data = {
            "id_cliente": id_cliente,
            "tipo_servicio": tipo_servicio,
            "fecha_servicio": fecha_servicio.isoformat(),
            "hora_servicio": str(hora_servicio),
            "ciudad_origen": ciudad_origen,
            "ciudad_destino": ciudad_destino,
            "numero_pasajeros": int(numero_pasajeros),
            "observaciones": observaciones
        }

        return self.datos.insertar(data)

    def eliminar(self, id_reserva):
        return self.datos.eliminar(id_reserva)
