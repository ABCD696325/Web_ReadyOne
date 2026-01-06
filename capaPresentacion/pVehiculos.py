import streamlit as st
from capaLogica.nVehiculos import NVehiculos

class PVehiculos:
    def __init__(self):
        self.logica = NVehiculos()
        if "vehiculo_sel" not in st.session_state:
            st.session_state.vehiculo_sel = None
        self.interfaz()

    def interfaz(self):
        st.title("🚗 Gestión de Vehículos - READY ONE")

        vehiculos = self.logica.listar()
        st.subheader("📋 Vehículos registrados")

        seleccion = st.dataframe(
            vehiculos,
            use_container_width=True,
            selection_mode="single-row",
            on_select="rerun"
        )

        if seleccion.selection.rows:
            st.session_state.vehiculo_sel = vehiculos[
                seleccion.selection.rows[0]
            ]

        st.divider()
        self.formulario()

    def formulario(self):
        v = st.session_state.vehiculo_sel

        st.subheader("📝 Registrar / Editar Vehículo")

        placa = st.text_input(
            "Placa",
            value=v["placa"] if v else "",
            help="Placa del vehículo. Ejemplo: ABC-123"
        )

        capacidad = st.number_input(
            "Capacidad",
            min_value=4,
            value=v["capacidad"] if v else 4,
            help="Número máximo de pasajeros"
        )

        estado = st.selectbox(
            "Estado",
            ["DISPONIBLE", "MANTENIMIENTO", "FUERA_SERVICIO"],
            index=0 if not v else
            ["DISPONIBLE", "MANTENIMIENTO", "FUERA_SERVICIO"].index(v["estado"]),
            help="Estado actual del vehículo"
        )

        col1, col2 = st.columns(2)

        with col1:
            if st.button("💾 Guardar"):
                try:
                    if v:
                        self.logica.actualizar(
                            v["id_vehiculo"],
                            placa,
                            capacidad,
                            estado
                        )
                        st.success("Vehículo actualizado")
                    else:
                        self.logica.registrar(
                            placa,
                            capacidad,
                            estado
                        )
                        st.success("Vehículo registrado")

                    self._limpiar()
                except Exception as e:
                    st.error(str(e))

        with col2:
            if st.button("🧹 Limpiar"):
                self._limpiar()

    def _limpiar(self):
        st.session_state.vehiculo_sel = None
        st.rerun()
