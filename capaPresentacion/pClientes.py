import streamlit as st
from capaLogica.nClientes import NClientes


class PClientes:
    def __init__(self):
        self.logica = NClientes()
        self._init_state()
        self.interfaz()

    # ================== ESTADO ==================

    def _init_state(self):
        if "cliente_sel" not in st.session_state:
            st.session_state.cliente_sel = None

    # ================== UTIL ==================

    def _solo_numeros(self, valor, limite):
        if valor is None:
            return ""
        return "".join(c for c in str(valor) if c.isdigit())[:limite]

    # ================== UI ==================

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
        cliente = st.session_state.cliente_sel

        st.subheader("📝 Registrar / Editar Cliente")

        tipo = st.selectbox(
            "Tipo de cliente",
            ["PERSONA_NATURAL", "PERSONA_JURIDICA"],
            index=0 if not cliente else (
                0 if cliente.get("tipo_cliente") == "PERSONA_NATURAL" else 1
            )
        )

        # ================== PERSONA NATURAL ==================
        if tipo == "PERSONA_NATURAL":
            nombres = st.text_input(
                "Nombres",
                value=cliente.get("nombres", "") if cliente else ""
            )
            apellidos = st.text_input(
                "Apellidos",
                value=cliente.get("apellidos", "") if cliente else ""
            )

            dni_input = st.text_input(
                "DNI (8 dígitos)",
                value=cliente.get("dni", "") if cliente else ""
            )
            dni = self._solo_numeros(dni_input, 8)
            st.caption(f"{len(dni)}/8")

            razon_social = None
            ruc = None

        # ================== PERSONA JURÍDICA ==================
        else:
            razon_social = st.text_input(
                "Razón Social",
                value=cliente.get("razon_social", "") if cliente else ""
            )

            ruc_input = st.text_input(
                "RUC (11 dígitos)",
                value=cliente.get("ruc", "") if cliente else ""
            )
            ruc = self._solo_numeros(ruc_input, 11)
            st.caption(f"{len(ruc)}/11")

            nombres = None
            apellidos = None
            dni = None

        # ================== COMUNES ==================
        telefono_input = st.text_input(
            "Teléfono (9 dígitos)",
            value=cliente.get("telefono", "") if cliente else ""
        )
        telefono = self._solo_numeros(telefono_input, 9)
        st.caption(f"{len(telefono)}/9")

        correo = st.text_input(
            "Correo electrónico",
            value=cliente.get("correo", "") if cliente else "",
            help="Ejemplo: usuario@gmail.com"
        )

        col1, col2 = st.columns(2)

        # ================== GUARDAR / ACTUALIZAR ==================
        with col1:
            if st.button("💾 Guardar"):
                try:
                    if cliente:
                        # EDITAR
                        if tipo == "PERSONA_NATURAL":
                            data = {
                                "tipo_cliente": tipo,
                                "nombres": nombres,
                                "apellidos": apellidos,
                                "dni": dni,
                                "telefono": telefono,
                                "correo": correo,
                                "razon_social": None,
                                "ruc": None
                            }
                        else:
                            data = {
                                "tipo_cliente": tipo,
                                "razon_social": razon_social,
                                "ruc": ruc,
                                "telefono": telefono,
                                "correo": correo,
                                "nombres": None,
                                "apellidos": None,
                                "dni": None
                            }

                        self.logica.actualizar(cliente["id_cliente"], data)
                        st.success("Cliente actualizado correctamente")

                    else:
                        # NUEVO
                        if tipo == "PERSONA_NATURAL":
                            self.logica.registrar_persona_natural(
                                nombres, apellidos, dni, telefono, correo
                            )
                        else:
                            self.logica.registrar_persona_juridica(
                                razon_social, ruc, telefono, correo
                            )

                        st.success("Cliente registrado correctamente")

                    self._limpiar()

                except Exception as e:
                    st.error(str(e))

        # ================== ELIMINAR ==================
        with col2:
            if st.button("🗑️ Eliminar") and cliente:
                self.logica.eliminar(cliente["id_cliente"])
                st.warning("Cliente eliminado")
                self._limpiar()

    # ================== LIMPIAR ==================

    def _limpiar(self):
        st.session_state.cliente_sel = None
        st.rerun()
