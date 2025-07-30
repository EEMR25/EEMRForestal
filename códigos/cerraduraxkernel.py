import numpy as np
from osgeo import gdal
import scipy.ndimage as ndi

# Ruta del raster binario
raster_path = r"C:\Users\eredm\Desktop\Trabajo\ZMVM\raster\2040\mrkv2030flimpio.tif"

# Abrir raster
ds = gdal.Open(raster_path)
array = ds.GetRasterBand(1).ReadAsArray()

# Estructura tipo torre (cruz de 4 vecinos)
estructura = np.array([[0, 1, 0],
                       [1, 0, 1],
                       [0, 1, 0]])

# Contar vecinos tipo torre con valor 1
vecinos = ndi.convolve((array == 1).astype(int), estructura, mode='constant', cval=0)

# Crear una copia del array
resultado = array.copy()

# Cambiar a 1 donde el valor original era 0 y tiene al menos 3 vecinos tipo torre con 1
resultado[(array == 0) & (vecinos >= 4)] = 1

# Guardar resultado
driver = gdal.GetDriverByName('GTiff')
out_path = r"C:\Users\eredm\Desktop\Trabajo\ZMVM\raster\2040\markv40v.tif"
out_ds = driver.Create(out_path, ds.RasterXSize, ds.RasterYSize, 1, gdal.GDT_Byte)
out_ds.SetGeoTransform(ds.GetGeoTransform())
out_ds.SetProjection(ds.GetProjection())
out_ds.GetRasterBand(1).WriteArray(resultado)
out_ds.FlushCache()
out_ds = None

print("Listo: píxeles 0 con ≥3 vecinos tipo torre cambiados a 1 guardados en:", out_path)
