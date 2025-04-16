
# SIMULACIÓN DE CÓDIGO PARA REALIZAR LA CONEXIÓN A BD CON WALLET
# IMPORTANTE CREAR VARIABLES DE ENTORNO PARA NO EXPONER INFORMACIÓN SENSIBLE

import os
import oracledb

def conectar_con_oracle():
    try:
        connection = oracledb.connect(
            user=os.getenv("ORACLE_USER"),
            password=os.getenv("ORACLE_PASSWORD"),
            dsn="",
            wallet_location=os.getenv("WALLET_PATH")
        )
        print("Conexión exitosa!")

        connection.close()

    except Exception as e:
        print("Error de conexión: ", e)

conectar_con_oracle()