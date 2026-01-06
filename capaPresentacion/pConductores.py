import streamlit as st
from capaLogica.nConductores import NConductores


class PConductores:
    def __init__(self):
        self.logica = NConductores()
        self._init_state()
        self.interfaz()

    # ================== ESTADO ==================

    def _init_state(self):
        if "conductor_sel" not in st.session_state:
            st.session_state.conductor_sel = None

    # ================== UTIL ==================

    def _solo_numeros(self, valor, limite):
        if valor is None:
            return ""
        return "".join(c for c in str(valor) if c.isdigit())[:limite]

    # ================== UI ==================

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
            value=conductor.get("nombres", "") if conductor else ""
        )

        apellidos = st.text_input(
            "Apellidos",
            value=conductor.get("apellidos", "") if conductor else ""
        )

        telefono_input = st.text_input(
            "Teléfono (9 dígitos)",
            value=conductor.get("telefono", "") if conductor else ""
        )
        telefono = self._solo_numeros(telefono_input, 9)
        st.caption(f"{len(telefono)}/9")

        tiene_papeletas = st.selectbox(
            "¿Tiene papeletas?",
            ["NO", "SÍ"],
            index=1 if conductor and conductor.get("tiene_papeletas") else 0
        )

        estado = st.selectbox(
            "Estado del conductor",
            ["ACTIVO", "INACTIVO"],
            index=0 if not conductor or conductor.get("estado") == "ACTIVO" else 1
        )

        col1, col2 = st.columns(2)

        # ================== GUARDAR ==================
        with col1:
            if st.button("💾 Guardar"):
                try:
                    self._guardar(
                        conductor,
                        nombres,
                        apellidos,
                        telefono,
                        tiene_papeletas,
                        estado
                    )
                except Exception as e:
                    st.error(str(e))

        # ================== ELIMINAR ==================
        with col2:
            if st.button("🗑️ Eliminar") and conductor:
                self.logica.eliminar(conductor["id_conductor"])
                st.warning("Conductor eliminado")
                self._limpiar()

    # ================== LOGICA ==================

    def _guardar(
        self,
        conductor,
        nombres,
        apellidos,
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
                telefono,
                papeletas,
                estado
            )
            st.success("Conductor actualizado correctamente")
        else:
            # 👉 AQUÍ ESTABA EL ERROR: faltaba `estado`
            self.logica.registrar(
                nombres,
                apellidos,
                telefono,
                papeletas,
                estado
            )
            st.success("Conductor registrado correctamente")

        self._limpiar()

    # ================== LIMPIAR ==================

    def _limpiar(self):
        st.session_state.conductor_sel = None
        st.rerun()
