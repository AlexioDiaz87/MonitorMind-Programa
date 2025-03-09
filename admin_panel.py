import tkinter as tk
import sqlite3
from tkinter import messagebox

# Función para verificar las credenciales del administrador
def verificar_credenciales(usuario, contrasena):
    return usuario == "admin" and contrasena == "admin2025"

# Función para obtener los usuarios registrados
def obtener_usuarios():
    conn = sqlite3.connect("usuarios.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id, usuario FROM usuarios")
    usuarios = cursor.fetchall()
    conn.close()
    return usuarios

# Función para eliminar un usuario
def eliminar_usuario(usuario_id):
    conn = sqlite3.connect("usuarios.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM usuarios WHERE id = ?", (usuario_id,))
    conn.commit()
    conn.close()

# Función para iniciar sesión como administrador
def iniciar_sesion():
    usuario = entry_usuario.get()
    contrasena = entry_contrasena.get()

    if verificar_credenciales(usuario, contrasena):
        ventana_login.destroy()  # Cerrar ventana de login
        mostrar_usuarios()  # Mostrar ventana de administración de usuarios
    else:
        messagebox.showerror("Error", "Usuario o contraseña incorrectos")

# Función para mostrar los usuarios en la ventana
def mostrar_usuarios():
    ventana_usuarios = tk.Toplevel()
    ventana_usuarios.title("Administrar Usuarios")
    ventana_usuarios.geometry("600x600")

    listbox = tk.Listbox(ventana_usuarios, font=("Arial", 14), width=50, height=15)
    listbox.grid(row=0, column=0, padx=20, pady=20)

    usuarios = obtener_usuarios()

    for usuario in usuarios:
        listbox.insert(tk.END, f"{usuario[1]} (ID: {usuario[0]})")

    # Función para eliminar un usuario seleccionado
    def eliminar_usuario_seleccionado():
        seleccion = listbox.curselection()
        if seleccion:
            usuario_seleccionado = listbox.get(seleccion[0])
            usuario_id = int(usuario_seleccionado.split(" (ID: ")[1].replace(")", ""))
            eliminar_usuario(usuario_id)
            listbox.delete(seleccion)  # Eliminar de la lista visible
            messagebox.showinfo("Éxito", f"Usuario {usuario_seleccionado} eliminado.")
            # Actualizar la lista de usuarios después de la eliminación
            actualizar_lista_usuarios(listbox)

    # Botón para eliminar usuario
    boton_eliminar = tk.Button(ventana_usuarios, text="Eliminar Usuario", command=eliminar_usuario_seleccionado, font=("Arial", 14))
    boton_eliminar.grid(row=1, column=0, pady=10)

    # Botón para cerrar la ventana
    boton_cerrar = tk.Button(ventana_usuarios, text="Cerrar", command=ventana_usuarios.destroy, font=("Arial", 14))
    boton_cerrar.grid(row=2, column=0, pady=10)

# Función para actualizar la lista de usuarios
def actualizar_lista_usuarios(listbox):
    usuarios = obtener_usuarios()  # Obtener los usuarios más recientes de la base de datos
    listbox.delete(0, tk.END)  # Limpiar la lista actual
    for usuario in usuarios:
        listbox.insert(tk.END, f"{usuario[1]} (ID: {usuario[0]})")

# Crear ventana de login para administrador
ventana_login = tk.Tk()
ventana_login.title("Login Admin")
ventana_login.geometry("400x300")

# Campo para ingresar usuario
label_usuario = tk.Label(ventana_login, text="Usuario", font=("Arial", 16))
label_usuario.grid(row=0, column=0, pady=10, padx=10)
entry_usuario = tk.Entry(ventana_login, font=("Arial", 16))
entry_usuario.grid(row=0, column=1, pady=5, padx=10)

# Campo para ingresar contraseña
label_contrasena = tk.Label(ventana_login, text="Contraseña", font=("Arial", 16))
label_contrasena.grid(row=1, column=0, pady=10, padx=10)
entry_contrasena = tk.Entry(ventana_login, font=("Arial", 16), show="*")
entry_contrasena.grid(row=1, column=1, pady=5, padx=10)

# Botón para iniciar sesión
boton_iniciar_sesion = tk.Button(ventana_login, text="Iniciar Sesión", command=iniciar_sesion, font=("Arial", 16))
boton_iniciar_sesion.grid(row=2, column=0, columnspan=2, pady=20)

# Mostrar ventana de login
ventana_login.mainloop()