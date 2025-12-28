import streamlit as st
from capaLogica.nServicios import NServicios
from capaLogica.nClientes import NClientes
from datetime import date, time

class PServicios:
    def __init__(self):
        self.logica = NServicios()
        self.clientes = NClientes()
        self._init_state()
        self.interfaz()

    def _init_state(self):
        if "servicio_sel" not in st.session_state:
            st.session_state.servicio_sel = None

    def interfaz(self):
        st.title("🧾 Gestión de Servicios - READY ONE")

        servicios = self.logica.listar()
        st.subheader("📋 Servicios registrados")

        seleccion = st.dataframe(
            servicios,
            use_container_width=True,
            selection_mode="single-row",
            on_select="rerun"
        )

        if seleccion.selection.rows:
            idx = seleccion.selection.rows[0]
            st.session_state.servicio_sel = servicios[idx]

        st.divider()
        self.formulario()

    def formulario(self):
        servicio = st.session_state.servicio_sel

        clientes = self.clientes.listar()
        clientes_dict = {
            f"{c['nombres']} {c['apellidos']}": c["id_cliente"]
            for c in clientes
        }

        st.subheader("📝 Registrar / Editar Servicio")

        cliente_nombre = st.selectbox(
            "Cliente",
            list(clientes_dict.keys())
        )

        tipo_servicio = st.selectbox(
            "Tipo de servicio",
            [
                "TAXI_AEROPUERTO_JAUJA",
                "TRASLADOS_REGIONALES_NACIONALES",
                "TOURS_PRIVADOS"
            ]
        )

        origen = st.text_input("Ciudad de origen")
        destino = st.text_input("Ciudad de destino")

        fecha_servicio = st.date_input(
            "Fecha del servicio",
            min_value=date.today()
        )

        hora_servicio = st.time_input(
            "Hora del servicio",
            value=time(8, 0)
        )

        pasajeros = st.number_input(
            "Número de pasajeros",
            min_value=1,
            step=1
        )

        tipo_viaje = st.selectbox(
            "Tipo de viaje",
            ["CORTO", "LARGO"]
        )

        ida_vuelta = st.selectbox(
            "Modalidad",
            ["IDA", "IDA_VUELTA"]
        )

        observaciones = st.text_area("Observaciones")

        col1, col2, col3 = st.columns(3)

        with col1:
            if st.button("💾 Guardar"):
                try:
                    self.logica.registrar(
                        clientes_dict[cliente_nombre],
                        tipo_servicio,
                        origen,
                        destino,
                        fecha_servicio,
                        hora_servicio,
                        pasajeros,
                        tipo_viaje,
                        ida_vuelta,
                        observaciones
                    )
                    st.success("Servicio registrado correctamente")
                    self._limpiar()
                except Exception as e:
                    st.error(str(e))

        with col2:
            if st.button("🗑️ Eliminar") and servicio:
                self.logica.eliminar(servicio["id_servicio"])
                st.warning("Servicio eliminado")
                self._limpiar()

        with col3:
            if st.button("🧹 Limpiar"):
                self._limpiar()

    def _limpiar(self):
        st.session_state.servicio_sel = None
        st.rerun()
