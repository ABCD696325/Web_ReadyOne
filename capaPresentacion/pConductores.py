import streamlit as st
from capaLogica.nConductores import NConductores

class PConductores:
    def __init__(self):
        self.logica = NConductores()
        self._init_state()
        self.interfaz()

    def _init_state(self):
        if "conductor_sel" not in st.session_state:
            st.session_state.conductor_sel = None

    def interfaz(self):
        st.title("👨‍✈️ Gestión de Conductores - READY ONE")

        conductores = self.logica.listar()

        seleccion = st.dataframe(
            conductores,
            use_container_width=True,
            selection_mode="single-row",
            on_select="rerun"
        )

        if seleccion.selection.rows:
            idx = seleccion.selection.rows[0]
            st.session_state.conductor_sel = conductores[idx]

        st.divider()
        self.formulario()

    def formulario(self):
        conductor = st.session_state.conductor_sel

        st.subheader("📝 Registrar / Editar Conductor")

        nombres = st.text_input(
            "Nombres",
            value=conductor["nombres"] if conductor else ""
        )

        apellidos = st.text_input(
            "Apellidos",
            value=conductor["apellidos"] if conductor else ""
        )

        telefono = st.text_input(
            "Teléfono (9 dígitos)",
            max_chars=9,
            value=conductor["telefono"] if conductor else ""
        )

        estado = st.text_input(
            "Estado",
            value=conductor["estado"] if conductor else "ACTIVO",
            help="Escriba ACTIVO o INACTIVO"
        )

        col1, col2 = st.columns(2)

        with col1:
            if st.button("💾 Guardar"):
                try:
                    if conductor:
                        self.logica.actualizar(
                            conductor["id_conductor"],
                            nombres,
                            apellidos,
                            telefono,
                            estado
                        )
                        st.success("Conductor actualizado correctamente")
                    else:
                        self.logica.registrar(
                            nombres,
                            apellidos,
                            telefono,
                            estado
                        )
                        st.success("Conductor registrado correctamente")

                    self._limpiar()
                except Exception as e:
                    st.error(str(e))

        with col2:
            if st.button("🗑️ Eliminar") and conductor:
                self.logica.eliminar(conductor["id_conductor"])
                st.warning("Conductor eliminado")
                self._limpiar()

    def _limpiar(self):
        st.session_state.conductor_sel = None
        st.rerun()
