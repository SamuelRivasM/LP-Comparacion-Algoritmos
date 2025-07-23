import tkinter as tk
from tkinter import messagebox, ttk
import random
import time
import csv
from datetime import datetime

# Algoritmos funcionales
# Primer algoritmo: b. lineal
def busqueda_lineal_funcional(lista, objetivo):
    return next((i for i, val in enumerate(lista) if val == objetivo), -1)

# Segundo algoritmo: b. binaria
def busqueda_binaria_funcional(lista, objetivo):
    #                             índice inicial  - i. final
    def binaria_rec(lista, objetivo, izquierda, derecha):
        # si el limite izq es mayor, no hay mas que buscar
        if izquierda > derecha:
            return -1
        medio = (izquierda + derecha) // 2
        if lista[medio] == objetivo:
            return medio
        elif lista[medio] < objetivo:
            return binaria_rec(lista, objetivo, medio + 1, derecha)
        else:
            return binaria_rec(lista, objetivo, izquierda, medio - 1)
    ## llama a la fun. recursiva para buscar en la lista entera.
    return binaria_rec(lista, objetivo, 0, len(lista) - 1)

# Historial de búsquedas xd
historial = []

# Config del interfaz uwu
class BusquedaApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Comparador de Búsqueda Funcional")
        self.root.geometry("800x600")
        self.root.configure(bg="#f0f4f8")
        self.lista = []

        fuente = ("Segoe UI", 11)

        tk.Label(root, text="Ingrese la lista separada por comas:", font=fuente, bg="#f0f4f8").pack(pady=5)
        self.entry_lista = tk.Entry(root, width=100, font=fuente)
        self.entry_lista.pack(pady=5)

        self.btn_generar = tk.Button(
            root, text="Generar lista grande", command=self.generar_lista_grande,
            bg="#007acc", fg="white", font=fuente, width=25
        )
        self.btn_generar.pack(pady=10)

        tk.Label(root, text="Elemento a buscar:", font=fuente, bg="#f0f4f8").pack()
        self.entry_objetivo = tk.Entry(root, font=fuente)
        self.entry_objetivo.pack(pady=5)

        tk.Label(root, text="Método de búsqueda:", font=fuente, bg="#f0f4f8").pack()
        self.metodo = tk.StringVar()
        self.metodo.set("lineal")
        tk.Radiobutton(root, text="Lineal", variable=self.metodo, value="lineal", font=fuente, bg="#f0f4f8").pack()
        tk.Radiobutton(root, text="Binaria", variable=self.metodo, value="binaria", font=fuente, bg="#f0f4f8").pack()

        self.btn_buscar = tk.Button(
            root, text="Buscar", command=self.buscar,
            bg="#28a745", fg="white", font=fuente, width=20
        )
        self.btn_buscar.pack(pady=10)

        self.btn_ver_historial = tk.Button(
            root, text="Ver historial", command=self.ver_historial,
            bg="#17a2b8", fg="white", font=fuente, width=20
        )
        self.btn_ver_historial.pack(pady=5)

        self.btn_guardar_csv = tk.Button(
            root, text="Guardar historial en CSV", command=self.guardar_historial_csv,
            bg="#ffc107", fg="black", font=fuente, width=25
        )
        self.btn_guardar_csv.pack(pady=5)

    def generar_lista_grande(self):
        self.lista = sorted(random.sample(range(1, 1000000), 100000))
        vista_resumida = ",".join(map(str, self.lista[:200])) + ",..."
        self.entry_lista.delete(0, tk.END)
        self.entry_lista.insert(0, vista_resumida)
        messagebox.showinfo("Lista generada", "Se ha generado una lista grande de 100 000 elementos.")

    def buscar(self):
        if "..." not in self.entry_lista.get():
            try:
                self.lista = list(map(int, self.entry_lista.get().split(",")))
            except ValueError:
                messagebox.showerror("Error", "Por favor ingresa una lista válida de números.")
                return

        objetivo_str = self.entry_objetivo.get()
        if not objetivo_str.isdigit():
            messagebox.showerror("Error", "Por favor ingresa un número válido a buscar.")
            return
        objetivo = int(objetivo_str)

        metodo = self.metodo.get()
        inicio = time.time()

        if metodo == "lineal":
            resultado = busqueda_lineal_funcional(self.lista, objetivo)
        elif metodo == "binaria":
            if self.lista != sorted(self.lista):
                messagebox.showwarning("Advertencia", "La lista debe estar ordenada para búsqueda binaria.")
                return
            resultado = busqueda_binaria_funcional(self.lista, objetivo)
        else:
            resultado = -1

        tiempo = time.time() - inicio
        fecha_hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        mensaje = f"{'Encontrado en la posición' if resultado != -1 else 'No encontrado'} | Tiempo: {tiempo:.6f} segundos"
        messagebox.showinfo("Resultado", mensaje)

        historial.append({
            "Método": metodo,
            "Elemento": objetivo,
            "Resultado": resultado,
            "Tiempo (s)": f"{tiempo:.6f}",
            "Fecha y Hora": fecha_hora
        })

    def ver_historial(self):
        ventana_historial = tk.Toplevel(self.root)
        ventana_historial.title("Historial de búsquedas")
        ventana_historial.geometry("750x400")
        ventana_historial.configure(bg="#ffffff")

        columnas = ("Método", "Elemento", "Resultado", "Tiempo (s)", "Fecha y Hora")
        tabla = ttk.Treeview(ventana_historial, columns=columnas, show="headings")

        for col in columnas:
            tabla.heading(col, text=col)
            tabla.column(col, anchor="center")

        for fila in historial:
            tabla.insert("", tk.END, values=(
                fila["Método"], fila["Elemento"], fila["Resultado"],
                fila["Tiempo (s)"], fila["Fecha y Hora"]
            ))

        tabla.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    def guardar_historial_csv(self):
        with open("historial_busqueda.csv", mode="w", newline='') as file:
            fieldnames = ["Método", "Elemento", "Resultado", "Tiempo (s)", "Fecha y Hora"]
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(historial)
        messagebox.showinfo("Guardado", "Historial guardado como historial_busqueda.csv")


# Ejecutar app es para hacer referencia 
if __name__ == "__main__":
    root = tk.Tk()
    app = BusquedaApp(root)
    root.mainloop()
