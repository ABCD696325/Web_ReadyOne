import streamlit as st
from capaLogica.nVehiculos import NVehiculos

class PVehiculos:
    def __init__(self):
        self.logica = NVehiculos()
        self._init_state()
        self.interfaz()

    def _init_state(self):
        if "vehiculo_sel" not in st.session_state:
            st.session_state.vehiculo_sel = None

    def interfaz(self):
        st.title("🚗 Gestión de Vehículos - READY ONE")

        vehiculos = self.logica.listar()

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
        vehiculo = st.session_state.vehiculo_sel

        placa = st.text_input(
            "Placa",
            value=vehiculo["placa"] if vehiculo else "",
            help="Mínimo 6 caracteres"
        )

        modelo = st.text_input(
            "Modelo",
            value=vehiculo["modelo"] if vehiculo else ""
        )

        capacidad = st.number_input(
            "Capacidad de pasajeros",
            min_value=4,
            step=1,
            value=vehiculo["capacidad"] if vehiculo else 4
        )

        estado = st.selectbox(
            "Estado del vehículo",
            ["DISPONIBLE", "MANTENIMIENTO", "FUERA_SERVICIO"],
            index=0 if not vehiculo else
            ["DISPONIBLE", "MANTENIMIENTO", "FUERA_SERVICIO"]
            .index(vehiculo["estado"])
        )

        col1, col2 = st.columns(2)

        with col1:
            if st.button("💾 Guardar"):
                try:
                    if vehiculo:
                        self.logica.actualizar(
                            vehiculo["id_vehiculo"],
                            placa,
                            modelo,
                            capacidad,
                            estado
                        )
                        st.success("Vehículo actualizado correctamente")
                    else:
                        self.logica.registrar(
                            placa,
                            modelo,
                            capacidad,
                            estado
                        )
                        st.success("Vehículo registrado correctamente")

                    self._limpiar()
                except Exception as e:
                    st.error(str(e))

        with col2:
            if st.button("🗑️ Eliminar") and vehiculo:
                self.logica.eliminar(vehiculo["id_vehiculo"])
                st.warning("Vehículo eliminado")
                self._limpiar()

    def _limpiar(self):
        st.session_state.vehiculo_sel = None
        st.rerun()
