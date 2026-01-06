import streamlit as st
from capaLogica.nReservas import NReservas
from capaLogica.nClientes import NClientes

class PReservas:
    def __init__(self):
        self.negocio = NReservas()
        self.clientes = NClientes()
        self._init_state()
        self.interfaz()

    def _init_state(self):
        if "reserva_sel" not in st.session_state:
            st.session_state.reserva_sel = None

    def interfaz(self):
        st.title("📅 Reservas - READY ONE")

        reservas = self.negocio.listar()
        st.subheader("📋 Reservas registradas")

        seleccion = st.dataframe(
            reservas,
            use_container_width=True,
            selection_mode="single-row",
            on_select="rerun"
        )

        if seleccion.selection.rows:
            st.session_state.reserva_sel = reservas[
                seleccion.selection.rows[0]
            ]

        st.divider()
        self.formulario()

    def formulario(self):
        clientes_db = self.clientes.listar()

        # 🔥 CONSTRUCCIÓN SEGURA DEL SELECTBOX
        clientes = {}
        for c in clientes_db:
            etiqueta = (
                c.get("nombre")
                or c.get("nombres")
                or c.get("razon_social")
                or c.get("cliente")
                or f"Cliente {c['id_cliente']}"
            )
            clientes[etiqueta] = c["id_cliente"]

        st.subheader("📝 Registrar Reserva")

        cliente = st.selectbox(
            "Cliente",
            clientes.keys()
        )

        precio = st.number_input(
            "Precio (S/.)",
            min_value=1.0,
            step=10.0
        )

        estado = st.selectbox(
            "Estado",
            ["SOLICITADO", "EN_PROCESO", "FINALIZADO", "CANCELADO"]
        )

        observaciones = st.text_area("Observaciones")

        col1, col2 = st.columns(2)

        with col1:
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

        with col2:
            if st.button("🗑️ Eliminar") and st.session_state.reserva_sel:
                self.negocio.eliminar(
                    st.session_state.reserva_sel["id_reserva"]
                )
                st.warning("Reserva eliminada")
                st.rerun()
