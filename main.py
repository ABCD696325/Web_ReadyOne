import streamlit as st

from capaPresentacion.pClientes import PClientes
from capaPresentacion.pServicios import PServicios
from capaPresentacion.pVehiculos import PVehiculos
from capaPresentacion.pConductores import PConductores
from capaPresentacion.pReservas import PReservas


def main():
    st.set_page_config(
        page_title="READY ONE",
        page_icon="🚐",
        layout="wide"
    )

    st.sidebar.title("READY ONE 🚐")

    opcion = st.sidebar.selectbox(
        "Módulo",
        [
            "Clientes",
            "Servicios",
            "Vehículos",
            "Conductores",
            "Reservas"
        ]
    )

    if opcion == "Clientes":
        PClientes()
    elif opcion == "Servicios":
        PServicios()
    elif opcion == "Vehículos":
        PVehiculos()
    elif opcion == "Conductores":
        PConductores()
    elif opcion == "Reservas":
        PReservas()


if __name__ == "__main__":
    main()
