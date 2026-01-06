import streamlit as st
from capaLogica.nReservas import NReservas
from capaLogica.nClientes import NClientes
from datetime import date

class PReservas:
    def __init__(self):
        self.logica = NReservas()
        self.clientes = NClientes()
        self.interfaz()

    def interfaz(self):
        st.title("📅 Gestión de Reservas - READY ONE")

        reservas = self.logica.listar()
        st.subheader("📋 Reservas registradas")
        st.dataframe(reservas, use_container_width=True)

        st.divider()
        self.formulario()

    def formulario(self):
        clientes = {
            f"{c['nombres']} {c['apellidos']}": c["id_cliente"]
            for c in self.clientes.listar()
        }

        st.subheader("📝 Registrar Reserva")

        cliente = st.selectbox("Cliente", list(clientes.keys()))

        tipo_servicio = st.selectbox(
            "Tipo de servicio",
            [
                "tour",
                "viaje personalizado",
                "aeropuerto de jauja"
            ]
        )

        fecha_servicio = st.date_input(
            "Fecha del servicio",
            min_value=date.today()
        )

        hora_servicio = st.time_input("Hora del servicio")

        ciudad_origen = st.text_input("Ciudad origen")
        ciudad_destino = st.text_input("Ciudad destino")

        numero_pasajeros = st.number_input(
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
                    fecha_servicio,
                    hora_servicio,
                    ciudad_origen,
                    ciudad_destino,
                    numero_pasajeros,
                    observaciones
                )
                st.success("Reserva registrada correctamente")
                st.rerun()
            except Exception as e:
                st.error(str(e))
