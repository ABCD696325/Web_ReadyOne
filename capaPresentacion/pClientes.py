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
        if "ruc" not in st.session_state:
            st.session_state.ruc = ""
        if "telefono" not in st.session_state:
            st.session_state.telefono = ""

    # 🔒 SOLO NÚMEROS + LÍMITE
    def _solo_numeros(self, valor, limite):
        return "".join(c for c in valor if c.isdigit())[:limite]

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

            # CARGAR DATOS PARA EDITAR
            st.session_state.telefono = clientes[idx].get("telefono", "")
            st.session_state.dni = clientes[idx].get("dni", "")
            st.session_state.ruc = clientes[idx].get("ruc", "")

        st.divider()
        self.formulario()

    def formulario(self):
        st.subheader("📝 Registrar / Editar Cliente")

        cliente = st.session_state.cliente_sel

        tipo = st.selectbox(
            "Tipo de cliente",
            ["PERSONA_NATURAL", "PERSONA_JURIDICA"],
            index=0 if not cliente or cliente["tipo_cliente"] == "PERSONA_NATURAL" else 1
        )

        # ========= PERSONA NATURAL =========
        if tipo == "PERSONA_NATURAL":
            nombres = st.text_input(
                "Nombres",
                value=cliente["nombres"] if cliente else ""
            )
            apellidos = st.text_input(
                "Apellidos",
                value=cliente["apellidos"] if cliente else ""
            )

            dni_input = st.text_input(
                "DNI (8 dígitos)",
                max_chars=8,
                value=st.session_state.dni
            )
            st.session_state.dni = self._solo_numeros(dni_input, 8)
            st.caption(f"{len(st.session_state.dni)}/8 dígitos")

            razon_social = None
            ruc = None

        # ========= PERSONA JURÍDICA =========
        else:
            razon_social = st.text_input(
                "Razón Social",
                value=cliente["razon_social"] if cliente else ""
            )

            ruc_input = st.text_input(
                "RUC (11 dígitos)",
                max_chars=11,
                value=st.session_state.ruc
            )
            st.session_state.ruc = self._solo_numeros(ruc_input, 11)
            st.caption(f"{len(st.session_state.ruc)}/11 dígitos")

            nombres = None
            apellidos = None

        # ========= TELÉFONO =========
        telefono_input = st.text_input(
            "Teléfono (9 dígitos)",
            max_chars=9,
            value=st.session_state.telefono
        )
        st.session_state.telefono = self._solo_numeros(telefono_input, 9)
        st.caption(f"{len(st.session_state.telefono)}/9 dígitos")

        correo = st.text_input(
            "Correo electrónico",
            value=cliente["correo"] if cliente else "",
            help="Ejemplo: usuario@gmail.com"
        )

        col1, col2 = st.columns(2)

        with col1:
            if st.button("💾 Guardar"):
                try:
                    if cliente:  # 👉 EDITAR
                        if tipo == "PERSONA_NATURAL":
                            data = {
                                "nombres": nombres,
                                "apellidos": apellidos,
                                "dni": st.session_state.dni,
                                "telefono": st.session_state.telefono,
                                "correo": correo
                            }
                        else:
                            data = {
                                "razon_social": razon_social,
                                "ruc": st.session_state.ruc,
                                "telefono": st.session_state.telefono,
                                "correo": correo
                            }

                        self.logica.actualizar(
                            cliente["id_cliente"],
                            data
                        )
                        st.success("Cliente actualizado correctamente")

                    else:  # 👉 REGISTRAR
                        if tipo == "PERSONA_NATURAL":
                            self.logica.registrar_persona_natural(
                                nombres,
                                apellidos,
                                st.session_state.dni,
                                st.session_state.telefono,
                                correo
                            )
                        else:
                            self.logica.registrar_persona_juridica(
                                razon_social,
                                st.session_state.ruc,
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
        st.session_state.ruc = ""
        st.session_state.telefono = ""
        st.rerun()
