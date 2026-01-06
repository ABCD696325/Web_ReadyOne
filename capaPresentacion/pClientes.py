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
        if "dni" not in st.session_state:
            st.session_state.dni = ""
        if "telefono" not in st.session_state:
            st.session_state.telefono = ""
        if "ruc" not in st.session_state:
            st.session_state.ruc = ""

    def _solo_numeros(self, valor, max_len):
        return "".join(c for c in valor if c.isdigit())[:max_len]

    def interfaz(self):
        st.title("👤 Gestión de Clientes - READY ONE")

        clientes = self.logica.listar()
        st.subheader("📋 Clientes Registrados")

        seleccion = st.dataframe(
            clientes,
            use_container_width=True,
            selection_mode="single-row",
            on_select="rerun"
        )

        if seleccion.selection.rows:
            st.session_state.cliente_sel = clientes[
                seleccion.selection.rows[0]
            ]

        st.divider()
        self.formulario()

    def formulario(self):
        cliente = st.session_state.cliente_sel

        st.subheader("📝 Registrar / Editar Cliente")

        nombres = st.text_input(
            "Nombres",
            value=cliente["nombres"] if cliente else ""
        )

        apellidos = st.text_input(
            "Apellidos",
            value=cliente["apellidos"] if cliente else ""
        )

        # ---------- DNI ----------
        dni_raw = st.text_input(
            "DNI (8 dígitos)",
            max_chars=8,
            value=cliente["dni"] if cliente else ""
        )
        st.session_state.dni = self._solo_numeros(dni_raw, 8)
        st.caption(f"{len(st.session_state.dni)}/8")

        # ---------- TELÉFONO ----------
        tel_raw = st.text_input(
            "Teléfono (9 dígitos)",
            max_chars=9,
            value=cliente["telefono"] if cliente else ""
        )
        st.session_state.telefono = self._solo_numeros(tel_raw, 9)
        st.caption(f"{len(st.session_state.telefono)}/9")

        correo = st.text_input(
            "Correo electrónico",
            value=cliente["correo"] if cliente else "",
            help="Ejemplo: usuario@gmail.com"
        )

        col1, col2 = st.columns(2)

        with col1:
            if st.button("💾 Guardar"):
                try:
                    if cliente:
                        self.logica.actualizar(
                            cliente["id_cliente"],
                            nombres,
                            apellidos,
                            st.session_state.telefono,
                            correo
                        )
                        st.success("Cliente actualizado correctamente")
                    else:
                        self.logica.registrar(
                            nombres,
                            apellidos,
                            st.session_state.telefono,
                            correo
                        )
                        st.success("Cliente registrado correctamente")

                    self._limpiar()
                except Exception as e:
                    st.error(str(e))

        with col2:
            if st.button("🗑️ Eliminar") and cliente:
                self.logica.eliminar(cliente["id_cliente"])
                st.warning("Cliente eliminado")
                self._limpiar()

    def _limpiar(self):
        st.session_state.cliente_sel = None
        st.session_state.dni = ""
        st.session_state.telefono = ""
        st.rerun()
