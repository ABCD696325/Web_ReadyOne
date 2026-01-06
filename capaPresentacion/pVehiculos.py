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

        marca = st.text_input(
            "Marca",
            value=vehiculo["marca"] if vehiculo else ""
        )

        modelo = st.text_input(
            "Modelo",
            value=vehiculo["modelo"] if vehiculo else ""
        )

        capacidad = st.number_input(
            "Capacidad",
            min_value=4,
            step=1,
            value=vehiculo["capacidad"] if vehiculo else 4
        )

        estado = st.selectbox(
            "Estado",
            ["DISPONIBLE", "MANTENIMIENTO", "FUERA_SERVICIO"],
            index=0 if not vehiculo else
            ["DISPONIBLE", "MANTENIMIENTO", "FUERA_SERVICIO"].index(
                vehiculo["estado"]
            )
        )

        if st.button("💾 Guardar"):
            try:
                if vehiculo:
                    self.logica.actualizar(
                        vehiculo["id_vehiculo"],
                        placa,
                        marca,
                        modelo,
                        capacidad,
                        estado
                    )
                    st.success("Vehículo actualizado")
                else:
                    self.logica.registrar(
                        placa,
                        marca,
                        modelo,
                        capacidad,
                        estado
                    )
                    st.success("Vehículo registrado")

                self._limpiar()
            except Exception as e:
                st.error(str(e))

    def _limpiar(self):
        st.session_state.vehiculo_sel = None
        st.rerun()
