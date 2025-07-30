import numpy as np
import scipy.ndimage as ndi
from osgeo import gdal

# Ruta del raster binario (ajusta esto)
raster_path = r"C:\Users\eredm\Desktop\Trabajo\ZMVM\raster\2030\zmvm30\mrkv2030flimpio.tif"

# Abrimos el raster con GDAL
ds = gdal.Open(raster_path)
array = ds.GetRasterBand(1).ReadAsArray()

# Cerradura morfológica (dilatación + erosión)
estructura = ndi.generate_binary_structure(2, 1)  # Tipo reina (8 vecinos)
cerrado = ndi.binary_closing(array == 1, structure=estructura).astype(np.uint8)

# Guardamos el resultado
driver = gdal.GetDriverByName('GTiff')
out_path = r"C:\Users\eredm\Desktop\Trabajo\ZMVM\raster\2040\markv40a.tif"
out_ds = driver.Create(out_path, ds.RasterXSize, ds.RasterYSize, 1, gdal.GDT_Byte)
out_ds.SetGeoTransform(ds.GetGeoTransform())
out_ds.SetProjection(ds.GetProjection())
out_ds.GetRasterBand(1).WriteArray(cerrado)
out_ds.FlushCache()
out_ds = None

print("Listo: raster con cerradura morfológica guardado en:", out_path)

