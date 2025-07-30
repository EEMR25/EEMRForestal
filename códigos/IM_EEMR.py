import numpy as np
import tkinter as tk
import pandas as pd
from PIL import Image, UnidentifiedImageError
from tkinter import filedialog, messagebox

# Autor: MC. EEMR---------06 octubre del 2024---------Además del índice de Moran te arrojará otros resultados, no les prestes atención. 

# Variables globales
matriz = None
Wij = None

def seleccionar_imagen():
    global matriz, Wij
    matriz, Wij = None, None  # Reinicia las variables globales al seleccionar una nueva imagen

    ruta_imagen = filedialog.askopenfilename(
        title="Selecciona una imagen TIFF",
        filetypes=[("Archivos TIFF", "*.tiff *.tif"), ("Todos los archivos", "*.*")]
    )
    if ruta_imagen:
        try:
            imagen = Image.open(ruta_imagen)
            # Procesa la imagen para extraer la matriz de valores
            matriz = procesar_imagen(imagen)
            matriz[:, 0] += 1  # Incrementa x en 1
            matriz[:, 1] += 1  # Incrementa y en 1

            # Mostrar los primeros valores de matriz para confirmar que es nueva
            print("Nueva matriz de valores de la imagen cargada:")
            print(matriz[:10])

            messagebox.showinfo("Imagen Cargada", "Imagen procesada correctamente.")
            crear_y_guardar_matriz_pesos(ruta_imagen, matriz)  # Genera una nueva matriz de pesos
            print("Matriz Wij generada con la nueva imagen:")
            print(Wij[:10, :10])  # Muestra los primeros valores para confirmar
        except UnidentifiedImageError:
            messagebox.showerror("Error", "No se puede identificar el archivo de imagen. Selecciona un archivo TIFF válido.")
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error inesperado: {e}")

def procesar_imagen(imagen):
    """Convierte la imagen en una matriz (x, y, valor)."""
    array_imagen = np.array(imagen)
    alto, ancho = array_imagen.shape
    matriz = []
    for y in range(alto):
        for x in range(ancho):
            valor = array_imagen[y, x]
            matriz.append([x, y, valor])
    return np.array(matriz)

def crear_y_guardar_matriz_pesos(ruta_imagen, matriz):
    """Crea y guarda la matriz de pesos espaciales de contigüidad."""
    global Wij
    dim = matriz.shape[0]
    Wij = np.zeros((dim, dim))
    for i in range(dim):
        for j in range(dim):
            if abs(i - j) == 1 or abs(i - j) == dim:
                Wij[i, j] = 1
    ruta_csv_wij = ruta_imagen.replace(".tif", "_Wij.csv")
    df_wij = pd.DataFrame(Wij)
    df_wij.to_csv(ruta_csv_wij, index=False, header=False)
    print(f"Matriz de pesos Wij guardada en: {ruta_csv_wij}")

def calcular_indice_moran():
    global matriz, Wij
    if matriz is None or Wij is None:
        messagebox.showerror("Error", "No se ha cargado ninguna imagen o la matriz de pesos no está disponible.")
        return
    valores = matriz[:, 2]
    x_media = np.mean(valores)
    num = np.sum(Wij * (valores - x_media)[:, None] * (valores - x_media))
    den = np.sum((valores - x_media) ** 2)
    I = (len(valores) / np.sum(Wij)) * (num / den)
    messagebox.showinfo("Índice de Moran", f"Índice de Moran: {I}")

def estimar_numero_de_condicion():
    global matriz, Wij
    if matriz is None or Wij is None:
        messagebox.showerror("Error", "No se ha cargado ninguna imagen o la matriz de pesos no está disponible.")
        return
    try:
        x_med = np.mean(matriz[:, 2])
        dim = Wij.shape[0]
        matriz_condicion = np.zeros((dim, dim))
        for i in range(dim):
            for j in range(dim):
                xi = matriz[i, 2] - x_med
                xj = matriz[j, 2] - x_med
                matriz_condicion[i, j] = Wij[i, j] * xi * xj
        numero_de_condicion = np.linalg.cond(matriz_condicion)
        messagebox.showinfo("Número de Condición", f"Número de condición de la matriz: {numero_de_condicion}")
    except Exception as e:
        messagebox.showerror("Error", f"Ocurrió un error al calcular el número de condición: {e}")

def calcular_determinante():
    global matriz, Wij
    if matriz is None or Wij is None:
        messagebox.showerror("Error", "No se ha cargado ninguna imagen o la matriz de pesos no está disponible.")
        return
    try:
        x_med = np.mean(matriz[:, 2])
        dim = Wij.shape[0]
        matriz_condicion = np.zeros((dim, dim))
        for i in range(dim):
            for j in range(dim):
                xi = matriz[i, 2] - x_med
                xj = matriz[j, 2] - x_med
                matriz_condicion[i, j] = Wij[i, j] * xi * xj
        _, eigenvectores = np.linalg.eig(matriz_condicion)
        matriz_producto = Wij @ eigenvectores
        determinante = np.linalg.det(matriz_producto)
        messagebox.showinfo("Determinante", f"Determinante del producto de Wij y los eigenvectores: {determinante}")
    except np.linalg.LinAlgError as e:
        messagebox.showerror("Error", f"No se pudo calcular el determinante: {e}")
    except Exception as e:
        messagebox.showerror("Error", f"Ocurrió un error inesperado: {e}")

# Crear la ventana principal con Tkinter
ventana = tk.Tk()
ventana.title("Cargar Imagen TIFF y Procesar")

btn_cargar = tk.Button(ventana, text="Seleccionar Imagen", command=seleccionar_imagen)
btn_cargar.pack(pady=10)

btn_moran = tk.Button(ventana, text="Calcular Índice de Moran", command=calcular_indice_moran)
btn_moran.pack(pady=10)

btn_condicion = tk.Button(ventana, text="Calcular Número de Condición", command=estimar_numero_de_condicion)
btn_condicion.pack(pady=10)

btn_determinante = tk.Button(ventana, text="Calcular Determinante", command=calcular_determinante)
btn_determinante.pack(pady=10)

ventana.mainloop()
