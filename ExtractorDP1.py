import ast
import os
import tkinter as tk
from tkinter import filedialog

def analizar_codigo(filename):
    with open(filename, 'r') as file:
        tree = ast.parse(file.read(), filename=filename)

    dependencies = set()

    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                dependencies.add(alias.name)
        elif isinstance(node, ast.ImportFrom):
            module = node.module
            if node.names:
                for alias in node.names:
                    dependencies.add(f"{module}.{alias.name}")
            else:
                dependencies.add(module)

    return dependencies

def generar_requirements_txt(codigo_filename):
    dependencies = analizar_codigo(codigo_filename)

    # Solicitar al usuario la ubicación para guardar el archivo
    save_path = filedialog.asksaveasfilename(defaultextension=".txt",
                                               filetypes=[("Archivos de texto", "*.txt")],
                                               title="Guardar como")

    if save_path:
        with open(save_path, 'w') as file:
            for dependency in sorted(dependencies):
                file.write(f"{dependency}\n")

            # Agregar el comando de instalación al final del archivo
            file.write("\n# Comando para instalar las dependencias:\n")
            file.write("# pip install -r requirements.txt")

        print(f"Archivo {save_path} generado con éxito.")

def seleccionar_archivo():
    filename = filedialog.askopenfilename(title="Seleccionar archivo Python",
                                          filetypes=[("Archivos Python", "*.py")])
    if filename:
        generar_requirements_txt(filename)

def salir():
    root.destroy()

# Crear la GUI
root = tk.Tk()
root.title("Extractor de dependencias")
root.configure(bg="#456783")
ancho_pantalla = root.winfo_screenwidth()
alto_pantalla = root.winfo_screenheight()
ventana_ancho = 640 
ventana_alto = 420
x_pos = (ancho_pantalla - ventana_ancho) // 2
y_pos = (alto_pantalla - ventana_alto) // 2
root.geometry(f"{ventana_ancho}x{ventana_alto}+{x_pos}+{y_pos}")

# Botón para seleccionar archivo
btn_seleccionar_archivo = tk.Button(root, text="Seleccionar Archivo", command=seleccionar_archivo, width=20, height=2)
btn_seleccionar_archivo.place(x=156, y=310)
btn_seleccionar_archivo.configure(bg="black", fg="white")

# Botón para salir
btn_salir = tk.Button(root, text="Salir", command=salir, width=10, height=2)
btn_salir.place(x=360, y=310)
btn_salir.configure(bg="black", fg="white")

# Configurar la acción de cerrar la ventana
root.protocol("WM_DELETE_WINDOW", salir)

# Ejecutar el bucle de eventos
root.mainloop()
