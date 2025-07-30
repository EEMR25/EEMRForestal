from qgis.core import QgsRasterLayer, QgsProject
import numpy as np
import scipy.ndimage as ndi
from osgeo import gdal

# Ruta del raster binario
raster_path = r"C:\Users\eredm\Desktop\Trabajo\ZMVM\raster\1980\zvmv80\mrkv80h.tif"

# Abrimos el raster con GDAL
raster_ds = gdal.Open(raster_path)
band = raster_ds.GetRasterBand(1)
array = band.ReadAsArray()

# Definir estructura vecindad tipo reina (8 vecinos)
structure = ndi.generate_binary_structure(2, 2)  # 3x3 con centro

# Contar vecinos valor 1 para cada píxel que es 1
# Primero creamos una máscara de píxeles 1
mask = (array == 1)

# Contar vecinos sumando convolución con estructura vecindad
neighbor_count = ndi.convolve(mask.astype(int), structure, mode='constant', cval=0) - 1  
# -1 para no contar el pixel central

# Condición: solo conservar píxeles con más de 2 vecinos
final_mask = np.where((mask) & (neighbor_count > 1), 1, 0)

# Guardamos el nuevo raster
driver = gdal.GetDriverByName('GTiff')
out_path = r"C:\Users\eredm\Desktop\Trabajo\ZMVM\raster\1975\zmvm75\mrkv75g.tif"
out_ds = driver.Create(out_path, raster_ds.RasterXSize, raster_ds.RasterYSize, 1, gdal.GDT_Byte)
out_ds.SetGeoTransform(raster_ds.GetGeoTransform())
out_ds.SetProjection(raster_ds.GetProjection())
out_band = out_ds.GetRasterBand(1)
out_band.WriteArray(final_mask)
out_band.FlushCache()
out_ds = None  # Cerrar dataset para guardar bien

print("Listo. Raster filtrado guardado en:", out_path)
