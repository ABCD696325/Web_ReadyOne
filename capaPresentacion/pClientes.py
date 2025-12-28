import streamlit as st
from capaLogica.nClientes import NClientes

class PClientes:
    def __init__(self):
        self.logica = NClientes()
        self._init_state()
        self.interfaz()

    def _init_state(self):
        if "cliente_sel" not in st.session_state:
            st.session_state.cliente_sel = None

    def interfaz(self):
        st.title("👥 Gestión de Clientes - READY ONE")

        clientes = self.logica.listar()

        seleccion = st.dataframe(
            clientes,
            use_container_width=True,
            selection_mode="single-row",
            on_select="rerun"
        )

        if seleccion.selection.rows:
            idx = seleccion.selection.rows[0]
            st.session_state.cliente_sel = clientes[idx]

        st.divider()
        self.formulario()

    def formulario(self):
        st.subheader("📝 Registrar / Editar Cliente")

        tipo = st.selectbox(
            "Tipo de cliente",
            ["PERSONA_NATURAL", "PERSONA_JURIDICA"]
        )

        if tipo == "PERSONA_NATURAL":
            nombres = st.text_input("Nombres")
            apellidos = st.text_input("Apellidos")
            dni = st.text_input("DNI (8 dígitos)")
            razon_social = ruc = None
        else:
            razon_social = st.text_input("Razón Social")
            ruc = st.text_input("RUC (11 dígitos)")
            nombres = apellidos = dni = None

        telefono = st.text_input("Teléfono")
        correo = st.text_input(
            "Correo electrónico",
            help="Ejemplo: usuario@gmail.com"
        )

        col1, col2, col3 = st.columns(3)

        with col1:
            if st.button("💾 Guardar"):
                try:
                    if tipo == "PERSONA_NATURAL":
                        self.logica.registrar_persona_natural(
                            nombres, apellidos, dni,
                            telefono, correo
                        )
                    else:
                        self.logica.registrar_persona_juridica(
                            razon_social, ruc,
                            telefono, correo
                        )

                    st.success("Cliente registrado correctamente")
                    self._limpiar()
                except Exception as e:
                    st.error(str(e))

        with col2:
            if st.button("🗑️ Eliminar") and st.session_state.cliente_sel:
                self.logica.eliminar(
                    st.session_state.cliente_sel["id_cliente"]
                )
                st.warning("Cliente eliminado")
                self._limpiar()

        with col3:
            if st.button("🧹 Limpiar"):
                self._limpiar()

    def _limpiar(self):
        st.session_state.cliente_sel = None
        st.rerun()
