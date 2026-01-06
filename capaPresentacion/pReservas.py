import streamlit as st
from capaLogica.nReservas import NReservas
from capaLogica.nClientes import NClientes
from capaLogica.nServicios import NServicios
from capaLogica.nVehiculos import NVehiculos
from capaLogica.nConductores import NConductores
from datetime import date


class PReservas:
    def __init__(self):
        self.logica = NReservas()
        self.clientes = NClientes()
        self.servicios = NServicios()
        self.vehiculos = NVehiculos()
        self.conductores = NConductores()
        self._init_state()
        self.interfaz()

    def _init_state(self):
        if "reserva_sel" not in st.session_state:
            st.session_state.reserva_sel = None

    def interfaz(self):
        st.title("📅 Gestión de Reservas - READY ONE")

        reservas = self.logica.listar()
        st.subheader("📋 Reservas registradas")

        seleccion = st.dataframe(
            reservas,
            use_container_width=True,
            selection_mode="single-row",
            on_select="rerun"
        )

        if seleccion.selection.rows:
            idx = seleccion.selection.rows[0]
            st.session_state.reserva_sel = reservas[idx]

        st.divider()
        self.formulario()

    def formulario(self):
        reserva = st.session_state.reserva_sel

        clientes = {
            f"{c['nombres']} {c['apellidos']}": c["id_cliente"]
            for c in self.clientes.listar()
        }

        servicios = {
            f"{s['tipo_servicio']} | {s['ciudad_origen']} → {s['ciudad_destino']}": s["id_servicio"]
            for s in self.servicios.listar()
        }

        vehiculos = {
            f"{v['placa']} | {v['capacidad']} pax | {v['estado']}": v["id_vehiculo"]
            for v in self.vehiculos.listar()
        }

        conductores = {
            f"{c['nombres']} {c['apellidos']}": c["id_conductor"]
            for c in self.conductores.listar()
        }

        st.subheader("📝 Registrar / Editar Reserva")

        cliente = st.selectbox("Cliente", list(clientes.keys()))
        servicio = st.selectbox("Servicio", list(servicios.keys()))
        vehiculo = st.selectbox("Vehículo", list(vehiculos.keys()))
        conductor = st.selectbox("Conductor", list(conductores.keys()))

        fecha_reserva = st.date_input(
            "Fecha de la reserva",
            min_value=date.today()
        )

        metodo_pago = st.selectbox(
            "Método de pago",
            ["EFECTIVO", "TRANSFERENCIA", "YAPE", "PLIN"]
        )

        monto = st.number_input(
            "Monto total (S/.)",
            min_value=0.0,
            step=10.0
        )

        estado = st.selectbox(
            "Estado de la reserva",
            [
                "PENDIENTE",
                "CONFIRMADA",
                "EN_PROCESO",
                "FINALIZADA",
                "CANCELADA"
            ]
        )

        observaciones = st.text_area("Observaciones")

        col1, col2, col3 = st.columns(3)

        with col1:
            if st.button("💾 Guardar"):
                try:
                    self.logica.registrar(
                        clientes[cliente],
                        servicios[servicio],
                        vehiculos[vehiculo],
                        conductores[conductor],
                        fecha_reserva,
                        metodo_pago,
                        monto,
                        estado,
                        observaciones
                    )
                    st.success("Reserva registrada correctamente")
                    self._limpiar()
                except Exception as e:
                    st.error(str(e))

        with col2:
            if st.button("🗑️ Eliminar") and reserva:
                self.logica.eliminar(reserva["id_reserva"])
                st.warning("Reserva eliminada")
                self._limpiar()

        with col3:
            if st.button("🧹 Limpiar"):
                self._limpiar()

    def _limpiar(self):
        st.session_state.reserva_sel = None
        st.rerun()
