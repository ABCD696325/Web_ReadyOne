import streamlit as st
from capaLogica.nClientes import NClientes

class PClientes:
    def __init__(self):
        self.logica = NClientes()
        self._init_state()
        self.interfaz()

    def _init_state(self):
        for k in ["cliente_sel", "dni", "ruc", "telefono"]:
            if k not in st.session_state:
                st.session_state[k] = ""

    def _solo_numeros(self, valor, max_len):
        valor = "".join(c for c in valor if c.isdigit())
        return valor[:max_len]

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
            st.session_state.cliente_sel = clientes[
                seleccion.selection.rows[0]
            ]

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

            st.session_state.dni = st.text_input(
                "DNI",
                value=cliente.get("dni", "") if cliente else "",
                key="dni_input"
            )
            st.session_state.dni = self._solo_numeros(
                st.session_state.dni, 8
            )
            st.caption(f"{len(st.session_state.dni)}/8 dígitos")

            razon_social = ruc = None

        else:
            razon_social = st.text_input(
                "Razón Social",
                value="" if not cliente else cliente.get("razon_social", "")
            )

            st.session_state.ruc = st.text_input(
                "RUC",
                value=cliente.get("ruc", "") if cliente else "",
                key="ruc_input"
            )
            st.session_state.ruc = self._solo_numeros(
                st.session_state.ruc, 11
            )
            st.caption(f"{len(st.session_state.ruc)}/11 dígitos")

            nombres = apellidos = dni = None

        st.session_state.telefono = st.text_input(
            "Teléfono",
            value=cliente.get("telefono", "") if cliente else "",
            key="telefono_input"
        )
        st.session_state.telefono = self._solo_numeros(
            st.session_state.telefono, 9
        )
        st.caption(f"{len(st.session_state.telefono)}/9 dígitos")

        correo = st.text_input(
            "Correo electrónico",
            value="" if not cliente else cliente.get("correo", "")
        )

        col1, col2, col3 = st.columns(3)

        with col1:
            if st.button("💾 Guardar"):
                try:
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
            if st.button("✏️ Editar Cliente") and cliente:
                data = {
                    "telefono": st.session_state.telefono,
                    "correo": correo
                }

                if tipo == "PERSONA_NATURAL":
                    data.update({
                        "nombres": nombres,
                        "apellidos": apellidos,
                        "dni": st.session_state.dni
                    })
                else:
                    data.update({
                        "razon_social": razon_social,
                        "ruc": st.session_state.ruc
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
        for k in ["cliente_sel", "dni", "ruc", "telefono"]:
            st.session_state[k] = ""
        st.rerun()
