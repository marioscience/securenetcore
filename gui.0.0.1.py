
import tkinter as tk
from tkinter import filedialog, messagebox
from threading import Thread
import subprocess
import sys
import os
from PIL import Image
from pystray import Icon as TrayIcon, Menu as TrayMenu, MenuItem as TrayItem

# Variable global para almacenar la ruta del archivo .ovpn
ovpn_file_path = None
tray_icon = None

def update_tray_icon(image_path):
    global tray_icon
    if tray_icon is not None:
        image = Image.open(image_path)
        tray_icon.icon = image

def connect_vpn():
    vpn_path = 'C:\\Program Files\\OpenVPN\\bin\\openvpn.exe'  # Ruta predeterminada
    global ovpn_file_path

    if os.path.isfile(vpn_path) and ovpn_file_path and os.path.isfile(ovpn_file_path):
        try:
            subprocess.Popen([vpn_path, '--config', ovpn_file_path])
            update_tray_icon("logo01.png")  # Actualiza la imagen del ícono de la bandeja
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo conectar a la VPN: {e}")
    else:
        messagebox.showerror("Error", "El path del binario de OpenVPN o el archivo .ovpn no es válido.")

def disconnect_vpn():
    if sys.platform.startswith('win'):
        subprocess.run(['taskkill', '/F', '/IM', 'openvpn.exe'])
    else:
        subprocess.run(['killall', 'openvpn'])
    update_tray_icon("logo.png")  # Reestablece la imagen original del ícono de la bandeja

def load_ovpn_file():
    global ovpn_file_path
    ovpn_file_path = filedialog.askopenfilename(
        title="Seleccionar archivo .ovpn",
        filetypes=(("Archivos OVPN", "*.ovpn"), ("Todos los archivos", "*.*"))
    )

def on_connect_vpn(icon, item):
    connect_vpn_thread()

def on_disconnect_vpn(icon, item):
    disconnect_vpn_thread()

def on_exit(icon, item):
    icon.stop()
    sys.exit()

def on_load_file(icon, item):
    load_ovpn_file()

def connect_vpn_thread():
    Thread(target=connect_vpn, daemon=True).start()

def disconnect_vpn_thread():
    Thread(target=disconnect_vpn, daemon=True).start()

def setup_tray_icon():
    global tray_icon
    image = Image.open("logo.png")  # Asegúrate de que la ruta al ícono sea correcta
    menu = TrayMenu(
        TrayItem('Cargar archivo .ovpn', on_load_file),
        TrayItem('Conectar', on_connect_vpn),
        TrayItem('Desconectar', on_disconnect_vpn),
        TrayItem('Salir', on_exit)
    )
    tray_icon = TrayIcon("NetcoreVPN", image, "NetcoreVPN", menu)
    tray_icon.run()

def main():
    # Inicializa Tkinter en modo sin ventana
    root = tk.Tk()
    root.withdraw()  # Oculta la ventana principal de Tkinter

    setup_tray_icon()

if __name__ == "__main__":
    main()
