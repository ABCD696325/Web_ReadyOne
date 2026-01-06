import streamlit as st
from capaLogica.nReservas import NReservas
from capaLogica.nClientes import NClientes

class PReservas:
    def __init__(self):
        self.negocio = NReservas()
        self.clientes = NClientes()
        self.interfaz()

    def interfaz(self):
        st.title("📅 Reservas - READY ONE")

        reservas = self.negocio.listar()
        st.subheader("📋 Reservas registradas")
        st.dataframe(reservas, use_container_width=True)

        st.divider()
        self.formulario()

    def formulario(self):
        st.subheader("📝 Registrar Reserva")

        clientes = {
            f"{c['nombres']} {c['apellidos']}": c["id_cliente"]
            for c in self.clientes.listar()
        }

        cliente = st.selectbox("Cliente", list(clientes.keys()))

        precio = st.number_input(
            "Precio (S/.)",
            min_value=1.0,
            step=10.0
        )

        estado = st.selectbox(
            "Estado",
            ["DISPONIBLE", "EN_PROCESO", "CANCELADO", "FINALIZADO"]
        )

        observaciones = st.text_area("Observaciones")

        if st.button("💾 Guardar"):
            try:
                self.negocio.registrar(
                    clientes[cliente],
                    precio,
                    estado,
                    observaciones
                )
                st.success("Reserva registrada correctamente")
                st.rerun()
            except Exception as e:
                st.error(str(e))
