import streamlit as st
from capaLogica.nReservas import NReservas
from capaLogica.nClientes import NClientes

class PReservas:
    def __init__(self):
        self.negocio = NReservas()
        self.clientes = NClientes()
        self.interfaz()

    def interfaz(self):
        st.title("📅 Gestión de Reservas - READY ONE")

        reservas = self.negocio.listar()
        st.subheader("Reservas registradas")
        st.dataframe(reservas, use_container_width=True)

        st.divider()
        self.formulario()

    def formulario(self):
        clientes = {
            f"{c['nombres']} {c.get('apellidos', '')}": c["id_cliente"]
            for c in self.clientes.listar()
        }

        with st.form("form_reserva"):
            cliente = st.selectbox("Cliente", list(clientes.keys()))

            precio = st.number_input(
                "Precio",
                min_value=0.0,
                step=1.0
            )

            estado = st.selectbox(
                "Estado",
                [
                    "SOLICITADO",
                    "EN_PROCESO",
                    "CANCELADO",
                    "FINALIZADO"
                ]
            )


            observaciones = st.text_area("Observaciones")

            if st.form_submit_button("Registrar"):
                self.negocio.registrar(
                    clientes[cliente],
                    precio,
                    estado,
                    observaciones
                )
                st.success("Reserva registrada correctamente")
                st.rerun()
