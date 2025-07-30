import pandas as pd
import os

# Ruta a la carpeta que contiene los archivos .csv
ruta_carpeta = r'C:\Users\eredm\Desktop\CentroGeo\II\SIG\Proyecto\Datos\violencia\homicidios\amlo'

# Lista para almacenar los dataframes
dfs = []

# Itera sobre todos los archivos en la carpeta
for archivo in os.listdir(ruta_carpeta):
    if archivo.endswith('.csv'):
        # Lee cada archivo .csv y lo agrega a la lista de dataframes
        df = pd.read_csv(os.path.join(ruta_carpeta, archivo))
        dfs.append(df)

# Une todos los dataframes en uno solo
df_combinado = pd.concat(dfs, ignore_index=True)

# Guarda el dataframe combinado en un nuevo archivo CSV
df_combinado.to_csv('archivo_combinado.csv', index=False)

print("Las tablas se han combinado exitosamente.")
