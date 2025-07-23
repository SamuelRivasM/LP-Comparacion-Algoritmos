import tkinter as tk
from tkinter import messagebox, ttk
import random
import time
import csv
import os

# ----------------- VARIABLES GLOBALES -----------------
historial_busquedas = []
archivo_csv = "historial_busquedas.csv"

# ----------------- FUNCIONES DE BUSQUEDA -----------------

def busqueda_lineal(lista, objetivo):
    for i in range(len(lista)):
        if lista[i] == objetivo:
            return i + 1
    return -1

def busqueda_binaria(lista, objetivo):
    inicio = 0
    fin = len(lista) - 1
    while inicio <= fin:
        medio = (inicio + fin) // 2
        if lista[medio] == objetivo:
            return medio + 1
        elif objetivo < lista[medio]:
            fin = medio - 1
        else:
            inicio = medio + 1
    return -1

# ----------------- FUNCIONES DE HISTORIAL -----------------

def guardar_historial_en_csv():
    with open(archivo_csv, mode='w', newline='') as archivo:
        writer = csv.writer(archivo)
        writer.writerow(["Método", "Objetivo", "Tiempo (ms)", "Resultado"])
        for h in historial_busquedas:
            writer.writerow([
                h["metodo"],
                h["objetivo"],
                f"{h['tiempo']:.3f}",
                h["resultado"] if h["resultado"] != -1 else "No encontrado"
            ])
    messagebox.showinfo("Guardado", "Historial guardado en historial_busquedas.csv")

def cargar_historial():
    if not os.path.exists(archivo_csv):
        return
    with open(archivo_csv, mode='r', newline='') as archivo:
        reader = csv.DictReader(archivo)
        for fila in reader:
            historial_busquedas.append({
                "metodo": fila["Método"],
                "objetivo": int(fila["Objetivo"]),
                "tiempo": float(fila["Tiempo (ms)"]),
                "resultado": int(fila["Resultado"]) if fila["Resultado"].isdigit() else -1
            })

# ----------------- FUNCIONES DE INTERFAZ -----------------

def ejecutar_busqueda():
    try:
        lista = list(map(int, entrada_lista.get().split(',')))
        objetivo = int(entrada_objetivo.get())
        tipo = metodo.get()

        inicio_tiempo = time.time()

        if tipo == "lineal":
            posicion = busqueda_lineal(lista, objetivo)
            duracion = (time.time() - inicio_tiempo) * 1000
            mensaje = f"Elemento {'encontrado en la posición: ' + str(posicion) if posicion != -1 else 'no encontrado.'}\nTiempo: {duracion:.3f} ms"
        else:
            lista_ordenada = sorted(lista)
            posicion = busqueda_binaria(lista_ordenada, objetivo)
            duracion = (time.time() - inicio_tiempo) * 1000
            mensaje = f"Lista ordenada: {lista_ordenada}\nElemento {'encontrado en la posición: ' + str(posicion) if posicion != -1 else 'no encontrado.'}\nTiempo: {duracion:.3f} ms"

        historial_busquedas.append({
            "metodo": tipo,
            "lista": lista,
            "objetivo": objetivo,
            "tiempo": duracion,
            "resultado": posicion
        })

        messagebox.showinfo("Resultado", mensaje)

    except ValueError:
        messagebox.showerror("Error", "Formato incorrecto. Ingresa números separados por comas.")

def generar_lista_aleatoria():
    datos = [random.randint(1, 10000) for _ in range(10000)]
    entrada_lista.delete(0, tk.END)
    entrada_lista.insert(0, ",".join(map(str, datos)))

def mostrar_historial():
    ventana_historial = tk.Toplevel()
    ventana_historial.title("Historial de Búsquedas")
    ventana_historial.geometry("700x400")

    filtro = tk.StringVar(value="todos")

    def actualizar_tabla():
        for item in tabla.get_children():
            tabla.delete(item)
        for i, h in enumerate(historial_busquedas):
            if filtro.get() == "todos" or h["metodo"] == filtro.get():
                tabla.insert("", "end", values=(
                    i + 1,
                    h["metodo"].capitalize(),
                    h["objetivo"],
                    f"{h['tiempo']:.3f} ms",
                    "Pos: " + str(h["resultado"]) if h["resultado"] != -1 else "No encontrado"
                ))

    # Filtro
    opciones = ["todos", "lineal", "binaria"]
    ttk.Label(ventana_historial, text="Filtrar por método:").pack(pady=5)
    ttk.OptionMenu(ventana_historial, filtro, *opciones, command=lambda _: actualizar_tabla()).pack()

    # Tabla
    columnas = ("#", "Método", "Objetivo", "Tiempo", "Resultado")
    tabla = ttk.Treeview(ventana_historial, columns=columnas, show="headings")
    for col in columnas:
        tabla.heading(col, text=col)
        tabla.column(col, width=120, anchor="center")
    tabla.pack(expand=True, fill="both", padx=10, pady=10)

    actualizar_tabla()

# ----------------- VENTANA PRINCIPAL -----------------

ventana = tk.Tk()
ventana.title("Búsquedas Lineal y Binaria - GUI Persistente")
ventana.geometry("520x450")

tk.Label(ventana, text="Lista de números (ej: 3,5,8,7):").pack(pady=5)
entrada_lista = tk.Entry(ventana, width=60)
entrada_lista.pack()

tk.Button(ventana, text="Generar lista grande", command=generar_lista_aleatoria, bg="#007ACC", fg="white").pack(pady=5)

tk.Label(ventana, text="Elemento a buscar:").pack(pady=5)
entrada_objetivo = tk.Entry(ventana, width=30)
entrada_objetivo.pack()

metodo = tk.StringVar(value="lineal")
tk.Label(ventana, text="Método de búsqueda:").pack(pady=10)
tk.Radiobutton(ventana, text="Lineal", variable=metodo, value="lineal").pack()
tk.Radiobutton(ventana, text="Binaria", variable=metodo, value="binaria").pack()

tk.Button(ventana, text="Buscar", command=ejecutar_busqueda, bg="#4CAF50", fg="white", width=20).pack(pady=15)
tk.Button(ventana, text="Ver Historial", command=mostrar_historial, bg="#FF9800", fg="white", width=20).pack(pady=5)
tk.Button(ventana, text="Guardar Historial", command=guardar_historial_en_csv, bg="#6A1B9A", fg="white", width=20).pack(pady=5)

# Cargar historial al iniciar
cargar_historial()

ventana.mainloop()
