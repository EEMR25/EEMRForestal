from osgeo import gdal
import numpy as np

# Rutas
raster_path = r'C:\Users\eredm\Desktop\Trabajo\ZMVM\entregables\mapas_130625b\01_Huella urbana\1985\comi80.tif'
salida = r'C:\Users\eredm\Desktop\Trabajo\ZMVM\entregables\mapas_130625b\01_Huella urbana\1985\comi80fill.tif'

# Abrir el raster
raster = gdal.Open(raster_path)
band = raster.GetRasterBand(1)
array = band.ReadAsArray()
nodata = band.GetNoDataValue()

# Mostrar info para depuración
print(f"Tipo de datos: {array.dtype}")
print(f"Valor NoData: {nodata}")
print(f"Valores únicos antes: {np.unique(array)}")

# Si hay NoData definido, reemplazarlo
if nodata is not None:
    array[array == nodata] = 1
else:
    # Caso sin NoData declarado: buscar píxeles distintos de 1 (asumimos que solo hay 1 y vacíos)
    array[~(array == 1)] = 1

print(f"Valores únicos después: {np.unique(array)}")

# Crear raster de salida
driver = gdal.GetDriverByName('GTiff')
out_raster = driver.Create(
    salida,
    raster.RasterXSize,
    raster.RasterYSize,
    1,
    band.DataType
)

out_raster.SetGeoTransform(raster.GetGeoTransform())
out_raster.SetProjection(raster.GetProjection())

# Escribir y quitar cualquier NoData
out_band = out_raster.GetRasterBand(1)
out_band.WriteArray(array)
out_band.DeleteNoDataValue()  # Elimina la marca de NoData, todos los píxeles ahora son válidos

out_raster.FlushCache()
out_raster = None

print("✅ ¡Listo! Se creó el raster con todos los valores sin dato reemplazados por 0.")
