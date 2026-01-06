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

    def _solo_numeros(self, valor, max_len):
        if valor is None:
            return ""
        return "".join(filter(str.isdigit, valor))[:max_len]

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

        cliente = st.session_state.cliente_sel

        tipo = st.selectbox(
            "Tipo de cliente",
            ["PERSONA_NATURAL", "PERSONA_JURIDICA"],
            index=0 if not cliente else
            (0 if cliente["tipo_cliente"] == "PERSONA_NATURAL" else 1)
        )

        if tipo == "PERSONA_NATURAL":
            nombres = st.text_input(
                "Nombres",
                value="" if not cliente else cliente.get("nombres", "")
            )
            apellidos = st.text_input(
                "Apellidos",
                value="" if not cliente else cliente.get("apellidos", "")
            )

            dni = st.text_input(
                "DNI (8 dígitos)",
                value="" if not cliente else cliente.get("dni", "")
            )
            dni = self._solo_numeros(dni, 8)

            razon_social = ruc = None
        else:
            razon_social = st.text_input(
                "Razón Social",
                value="" if not cliente else cliente.get("razon_social", "")
            )

            ruc = st.text_input(
                "RUC (11 dígitos)",
                value="" if not cliente else cliente.get("ruc", "")
            )
            ruc = self._solo_numeros(ruc, 11)

            nombres = apellidos = dni = None

        telefono = st.text_input(
            "Teléfono (9 dígitos)",
            value="" if not cliente else cliente.get("telefono", "")
        )
        telefono = self._solo_numeros(telefono, 9)

        correo = st.text_input(
            "Correo electrónico",
            value="" if not cliente else cliente.get("correo", ""),
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
            if st.button("✏️ Editar Cliente") and cliente:
                data = {
                    "telefono": telefono,
                    "correo": correo
                }

                if tipo == "PERSONA_NATURAL":
                    data.update({
                        "nombres": nombres,
                        "apellidos": apellidos,
                        "dni": dni
                    })
                else:
                    data.update({
                        "razon_social": razon_social,
                        "ruc": ruc
                    })

                self.logica.actualizar(cliente["id_cliente"], data)
                st.success("Cliente actualizado correctamente")
                self._limpiar()

        with col3:
            if st.button("🗑️ Eliminar") and cliente:
                self.logica.eliminar(cliente["id_cliente"])
                st.warning("Cliente eliminado")
                self._limpiar()

    def _limpiar(self):
        st.session_state.cliente_sel = None
        st.rerun()
