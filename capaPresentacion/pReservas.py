import streamlit as st
from capaLogica.nReservas import NReservas
from capaLogica.nClientes import NClientes

class PReservas:
    def __init__(self):
        self.logica = NReservas()
        self.clientes = NClientes()
        self._init_state()
        self.interfaz()

    def _init_state(self):
        if "reserva_sel" not in st.session_state:
            st.session_state.reserva_sel = None

    def interfaz(self):
        st.title("📅 Gestión de Reservas - READY ONE")

        reservas = self.logica.listar()
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
        reserva = st.session_state.reserva_sel

        clientes = {
            f"{c['nombre']}": c["id_cliente"]
            for c in self.clientes.listar()
        }

        st.subheader("📝 Registrar / Editar Reserva")

        cliente = st.selectbox(
            "Cliente",
            clientes.keys(),
            index=0 if not reserva else
            list(clientes.values()).index(reserva["id_cliente"])
        )

        precio = st.number_input(
            "Precio (S/.)",
            min_value=0.0,
            step=10.0,
            value=float(reserva["precio"]) if reserva else 0.0
        )

        estado = st.selectbox(
            "Estado",
            [
                "SOLICITADO",
                "DISPONIBLE",
                "EN_PROCESO",
                "CANCELADO",
                "FINALIZADO"
            ],
            index=0 if not reserva else
            [
                "SOLICITADO",
                "DISPONIBLE",
                "EN_PROCESO",
                "CANCELADO",
                "FINALIZADO"
            ].index(reserva["estado"])
        )

        observaciones = st.text_area(
            "Observaciones",
            value=reserva["observaciones"] if reserva else ""
        )

        col1, col2 = st.columns(2)

        with col1:
            if st.button("💾 Guardar"):
                try:
                    if reserva:
                        self.logica.actualizar(
                            reserva["id_reserva"],
                            precio,
                            estado,
                            observaciones
                        )
                        st.success("Reserva actualizada")
                    else:
                        self.logica.registrar(
                            clientes[cliente],
                            precio,
                            estado,
                            observaciones
                        )
                        st.success("Reserva registrada")

                    self._limpiar()
                except Exception as e:
                    st.error(str(e))

        with col2:
            if st.button("🗑️ Eliminar") and reserva:
                self.logica.eliminar(reserva["id_reserva"])
                st.warning("Reserva eliminada")
                self._limpiar()

    def _limpiar(self):
        st.session_state.reserva_sel = None
        st.rerun()
