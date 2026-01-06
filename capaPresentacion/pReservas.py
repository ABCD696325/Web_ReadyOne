import streamlit as st
from capaLogica.nReservas import NReservas
from capaLogica.nClientes import NClientes


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

        cliente = st.selectbox("Cliente", clientes.keys())

        monto = st.number_input(
            "Monto total (S/.)",
            min_value=0.0,
            step=10.0
        )

        estado = st.text_input(
            "Estado",
            value="PENDIENTE",
            help="Ejemplo: PENDIENTE, CONFIRMADA, CANCELADA"
        )

        observaciones = st.text_area("Observaciones")

        if st.button("💾 Guardar Reserva"):
            try:
                self.logica.registrar(
                    clientes[cliente],
                    monto,
                    estado,
                    observaciones
                )
                st.success("Reserva registrada correctamente")
                st.rerun()
            except Exception as e:
                st.error(str(e))
