from osgeo import gdal

# Cambia estas rutas por las tuyas
input_file = r"C:\Users\eredm\Desktop\Trabajo\ZMVM\raster\2030\ufc20b_ajustado.rst"
output_file = r"C:\Users\eredm\Desktop\Trabajo\ZMVM\raster\2030\ufc20c.rst"

# Ejecutar la conversión con tipo de dato entero
gdal.Translate(
    output_file,
    input_file,
    format="RST",
    outputType=gdal.GDT_Int16
)

print("Conversión completada con éxito.")
