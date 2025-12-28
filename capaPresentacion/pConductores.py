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
        st.subheader("📋 Conductores registrados")

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
        licencia = st.text_input(
            "Licencia de conducir",
            value=conductor["licencia"] if conductor else ""
        )
        telefono = st.text_input(
            "Teléfono",
            max_chars=9,
            value=conductor["telefono"] if conductor else ""
        )

        tiene_papeletas = st.selectbox(
            "¿Tiene papeletas?",
            ["NO", "SÍ"],
            index=1 if conductor and conductor["tiene_papeletas"] else 0
        )

        estado = st.selectbox(
            "Estado del conductor",
            ["ACTIVO", "INACTIVO"],
            index=0 if not conductor or conductor["estado"] == "ACTIVO" else 1
        )

        col1, col2, col3 = st.columns(3)

        with col1:
            if st.button("💾 Guardar"):
                try:
                    self._guardar(
                        conductor,
                        nombres,
                        apellidos,
                        licencia,
                        telefono,
                        tiene_papeletas,
                        estado
                    )
                except Exception as e:
                    st.error(str(e))

        with col2:
            if st.button("🗑️ Eliminar") and conductor:
                self.logica.eliminar(conductor["id_conductor"])
                st.warning("Conductor eliminado")
                self._limpiar()

        with col3:
            if st.button("🧹 Limpiar"):
                self._limpiar()

    def _guardar(
        self,
        conductor,
        nombres,
        apellidos,
        licencia,
        telefono,
        tiene_papeletas,
        estado
    ):
        papeletas = True if tiene_papeletas == "SÍ" else False

        if conductor:
            self.logica.actualizar(
                conductor["id_conductor"],
                nombres,
                apellidos,
                licencia,
                telefono,
                papeletas,
                estado
            )
            st.success("Conductor actualizado correctamente")
        else:
            self.logica.registrar(
                nombres,
                apellidos,
                licencia,
                telefono,
                papeletas,
                estado
            )
            st.success("Conductor registrado correctamente")

        self._limpiar()

    def _limpiar(self):
        st.session_state.conductor_sel = None
        st.rerun()
