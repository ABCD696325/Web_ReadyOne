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

    # ---------- FILTRO REAL ----------
    def _filtrar(self, campo, max_len):
        valor = st.session_state[campo]
        valor = "".join(c for c in valor if c.isdigit())
        st.session_state[campo] = valor[:max_len]

    def interfaz(self):
        st.title("👥 Gestión de Clientes - READY ONE")

        clientes = self.logica.listar()

        sel = st.dataframe(
            clientes,
            selection_mode="single-row",
            use_container_width=True,
            on_select="rerun"
        )

        if sel.selection.rows:
            st.session_state.cliente_sel = clientes[sel.selection.rows[0]]

        st.divider()
        self.formulario()

    def formulario(self):
        cliente = st.session_state.cliente_sel

        tipo = st.selectbox(
            "Tipo de cliente",
            ["PERSONA_NATURAL", "PERSONA_JURIDICA"]
        )

        if tipo == "PERSONA_NATURAL":
            st.text_input("Nombres")
            st.text_input("Apellidos")

            st.text_input(
                "DNI",
                key="dni",
                on_change=self._filtrar,
                args=("dni", 8)
            )
            st.caption(f"{len(st.session_state.dni)}/8 dígitos")

        else:
            st.text_input("Razón Social")

            st.text_input(
                "RUC",
                key="ruc",
                on_change=self._filtrar,
                args=("ruc", 11)
            )
            st.caption(f"{len(st.session_state.ruc)}/11 dígitos")

        st.text_input(
            "Teléfono",
            key="telefono",
            on_change=self._filtrar,
            args=("telefono", 9)
        )
        st.caption(f"{len(st.session_state.telefono)}/9 dígitos")
