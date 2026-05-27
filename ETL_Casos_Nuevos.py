import pandas as pd
from sqlalchemy import create_engine
import time

import os 
from dotenv import load_dotenv


inicio = time.time()
#Importar archivo excel
df = pd.read_excel("Casos_Nuevos.xlsx",
                   sheet_name="Base",
                   skiprows=1,
                   #Columnas que se usaran 
                   usecols=["Expediente","Sexo","Fecha_Nacimiento","Fecha_Apertura_Exp","Diagnostico","Descripcion", "Diagnostico_2", "Descripcion_2","Vivo","T","M","N","EC","Fecha_defuncion"]

)

#Cantidad de registros extraidos
print (f"Extraidos:{len(df)} registros")

# Imprimir 5 primero y 5 ultimos
print(df.head(10))
#Informacion del tipo de datos de columnas
print(df.info())

#Transformacion de datos  de objeto a Fecha
df["Fecha_Nacimiento"] = pd.to_datetime(df["Fecha_Nacimiento"], errors="coerce")
df["Fecha_Apertura_Exp"] = pd.to_datetime(df["Fecha_Apertura_Exp"], errors="coerce")
#Poner en etapa clinica cuando se encuentre vacio o tenga el numero 99 No definido
df["EC"] = df["EC"].replace(
    [99, "99", ""],
    "No definido"
)
df["EC"] = df["EC"].fillna("No definido")

# Convertir NaN/NaT a NULL espacios vacios de forma correcta
df = df.where(pd.notnull(df), None)

print(f"Transformados: {len(df)} registros válidos")
#Volver a imprimir la info con el tipo de dato cambiado
print(df.info())
#Mostrar los primeros 5 registros para validar
print(df.head(10))


#Carga a MYSQL

print("-------Comienza la Carga-------")

load_dotenv()
usuario = os.getenv("MYSQL_USER")
password = os.getenv("MYSQL_PASS")
host = os.getenv("MYSQL_HOST")
puerto = os.getenv("MYSQL_PORT")
database = os.getenv("MYSQL_DB_NAME")

#Conexion a la base de datos con su driver y carga de tabla
engine = create_engine(f"mysql+pymysql://{usuario}:{password}@{host}:{puerto}/{database}")

#Try catch para hacer rollback en caso de error
try:
    with engine.begin() as conexion:
        if len(df) == 0 :
            raise ValueError("El DataFrame está vacío")
        
        df.to_sql("casos_nuevos", engine, if_exists="append", index=False)

        #tiempo de finalizacion del proceso
        fin = time.time()
        print(f"Se ha completado el ETL: {len(df)} registros cargados en {round(fin-inicio,2)} segundos")
        print(f"Tabla lista en MySQL en la base de datos: {database} y tabla casos nuevos")

        

except Exception as e:

    print(f"Error en ETL: {e} se realizo rollback")
   



