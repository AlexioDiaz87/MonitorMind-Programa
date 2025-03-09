import tkinter as tk
from tkinter import messagebox
from db import obtener_usuarios, obtener_resultados_usuario, eliminar_usuario

# Función para verificar las credenciales del administrador (predefinidas)
def verificar_credenciales(usuario, contrasena):
    return usuario == "admin" and contrasena == "admin2025"

def iniciar_sesion():
    """Verifica las credenciales y muestra el panel de administración si son correctas"""
    usuario = entry_usuario.get()
    contrasena = entry_contrasena.get()

    if verificar_credenciales(usuario, contrasena):
        ventana_login.destroy()  # Cerrar ventana de login
        mostrar_panel_admin()  # Mostrar panel de administración
    else:
        messagebox.showerror("Error", "Usuario o contraseña incorrectos")

def mostrar_panel_admin():
    """Crea la ventana de administración de usuarios"""
    ventana_admin = tk.Tk()
    ventana_admin.title("Panel de Administración")
    ventana_admin.geometry("800x600")

    # Lista de usuarios
    listbox_usuarios = tk.Listbox(ventana_admin, font=("Arial", 14), width=40, height=15)
    listbox_usuarios.grid(row=0, column=0, padx=20, pady=20)

    # Lista de resultados
    listbox_resultados = tk.Listbox(ventana_admin, font=("Arial", 14), width=50, height=15)
    listbox_resultados.grid(row=0, column=1, padx=20, pady=20)

    # Cargar usuarios en la lista
    usuarios = obtener_usuarios()
    for usuario in usuarios:
        listbox_usuarios.insert(tk.END, f"{usuario[1]} (ID: {usuario[0]})")

    # Función para cargar los resultados del usuario seleccionado
    def cargar_resultados():
        listbox_resultados.delete(0, tk.END)
        seleccion = listbox_usuarios.curselection()
        if seleccion:
            usuario_seleccionado = listbox_usuarios.get(seleccion[0])
            idUser = int(usuario_seleccionado.split("(ID: ")[1].replace(")", ""))
            resultados = obtener_resultados_usuario(idUser)
            for res in resultados:
                listbox_resultados.insert(tk.END, f"ID:{res[0]} | F1:{res[1]:.2f}% | F2:{res[2]:.2f}% | CP:{res[3]:.2f}% | RF:{res[4]:.2f}%")

    # Función para eliminar usuario
    def eliminar_usuario_seleccionado():
        seleccion = listbox_usuarios.curselection()
        if seleccion:
            usuario_seleccionado = listbox_usuarios.get(seleccion[0])
            idUser = int(usuario_seleccionado.split("(ID: ")[1].replace(")", ""))
            eliminar_usuario(idUser)
            listbox_usuarios.delete(seleccion)
            listbox_resultados.delete(0, tk.END)
            messagebox.showinfo("Éxito", f"Usuario {usuario_seleccionado} eliminado.")

    # Botón para cargar resultados
    boton_cargar = tk.Button(ventana_admin, text="Ver Resultados", command=cargar_resultados, font=("Arial", 14))
    boton_cargar.grid(row=1, column=0, pady=10)

    # Botón para eliminar usuario
    boton_eliminar = tk.Button(ventana_admin, text="Eliminar Usuario", command=eliminar_usuario_seleccionado, font=("Arial", 14))
    boton_eliminar.grid(row=1, column=1, pady=10)

    # Botón para cerrar
    boton_cerrar = tk.Button(ventana_admin, text="Cerrar", command=ventana_admin.destroy, font=("Arial", 14))
    boton_cerrar.grid(row=2, column=0, columnspan=2, pady=10)

    ventana_admin.mainloop()

# Crear ventana de login para el administrador
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
