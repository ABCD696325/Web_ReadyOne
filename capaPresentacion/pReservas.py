import streamlit as st
from capaLogica.nReservas import NReservas
from capaLogica.nClientes import NClientes
from datetime import date, time

class PReservas:
    def __init__(self):
        self.logica = NReservas()
        self.clientes = NClientes()
        self.interfaz()

    def interfaz(self):
        st.title("📅 Gestión de Reservas - READY ONE")

        st.subheader("📝 Registrar Reserva")

        clientes = {
            f"{c['nombres']} {c['apellidos']}": c["id_cliente"]
            for c in self.clientes.listar()
        }

        cliente = st.selectbox("Cliente", list(clientes.keys()))

        tipo_servicio = st.selectbox(
            "Tipo de servicio",
            ["TAXI", "DELIVERY", "TOUR", "TRASLADO"]
        )

        fecha = st.date_input("Fecha del servicio", min_value=date.today())
        hora = st.time_input("Hora del servicio", value=time(8, 0))

        ciudad_origen = st.text_input("Ciudad de origen")
        ciudad_destino = st.text_input("Ciudad de destino")

        pasajeros = st.number_input(
            "Número de pasajeros",
            min_value=1,
            step=1
        )

        observaciones = st.text_area("Observaciones")

        if st.button("💾 Guardar"):
            try:
                self.logica.registrar(
                    clientes[cliente],
                    tipo_servicio,
                    fecha,
                    hora,
                    ciudad_origen,
                    ciudad_destino,
                    pasajeros,
                    observaciones
                )
                st.success("✅ Reserva registrada correctamente")
                st.rerun()
            except Exception as e:
                st.error(str(e))
