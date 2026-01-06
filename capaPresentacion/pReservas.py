import streamlit as st
from capaLogica.nReservas import NReservas
from capaLogica.nClientes import NClientes
from capaLogica.nServicios import NServicios
from capaLogica.nVehiculos import NVehiculos
from capaLogica.nConductores import NConductores


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
        st.dataframe(reservas, use_container_width=True)

        st.divider()
        self.formulario()

    def formulario(self):
        clientes = {
            f"{c['nombres']} {c['apellidos']}": c["id_cliente"]
            for c in self.clientes.listar()
        }

        servicios = {
            f"{s['tipo_servicio']} | {s['ciudad_origen']} → {s['ciudad_destino']}": s["id_servicio"]
            for s in self.servicios.listar()
        }

        vehiculos = {
            f"{v['placa']} | {v['capacidad']} pax": v["id_vehiculo"]
            for v in self.vehiculos.listar()
        }

        conductores = {
            f"{c['nombres']} {c['apellidos']}": c["id_conductor"]
            for c in self.conductores.listar()
        }

        st.subheader("📝 Registrar Reserva")

        cliente = st.selectbox("Cliente", clientes.keys())
        servicio = st.selectbox("Servicio", servicios.keys())
        vehiculo = st.selectbox("Vehículo", vehiculos.keys())
        conductor = st.selectbox("Conductor", conductores.keys())

        metodo_pago = st.selectbox(
            "Método de pago",
            ["EFECTIVO", "TRANSFERENCIA", "YAPE", "PLIN"]
        )

        monto = st.number_input("Monto total", min_value=0.0, step=10.0)

        estado = st.selectbox(
            "Estado",
            ["PENDIENTE", "CONFIRMADA", "EN_PROCESO", "FINALIZADA", "CANCELADA"]
        )

        observaciones = st.text_area("Observaciones")

        if st.button("💾 Guardar Reserva"):
            try:
                self.logica.registrar(
                    clientes[cliente],
                    servicios[servicio],
                    vehiculos[vehiculo],
                    conductores[conductor],
                    metodo_pago,
                    monto,
                    estado,
                    observaciones
                )
                st.success("Reserva registrada correctamente")
                st.rerun()
            except Exception as e:
                st.error(str(e))
