import streamlit as st
from capaLogica.nReservas import NReservas
from capaLogica.nClientes import NClientes

class PReservas:
    def __init__(self):
        self.logica = NReservas()
        self.clientes = NClientes()
        self.interfaz()

    def interfaz(self):
        st.title("📅 Reservas - READY ONE")

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

        estado = st.selectbox(
            "Estado",
            ["DISPONIBLE", "EN_PROCESO", "CANCELADO"]
        )

        precio = st.number_input(
            "Precio (S/.)",
            min_value=1.0,
            step=10.0
        )

        if st.button("💾 Guardar"):
            try:
                self.logica.registrar(
                    clientes[cliente],
                    estado,
                    precio
                )
                st.success("Reserva registrada correctamente")
                st.rerun()
            except Exception as e:
                st.error(str(e))
