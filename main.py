import tkinter as tk
from tictactoe import TicTacToe
import ctypes
import os
from utils import resource_path

if __name__ == "__main__":
    root = tk.Tk()
    
    try:
        icon_path = resource_path('image/icon.ico')
        if os.path.exists(icon_path):
            root.iconbitmap(icon_path)
            # Establecer ícono en la barra de tareas
            myappid = 'com.foreverlcd.tictactoe.1.0'
            ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
        else:
            print(f"Icono no encontrado en: {icon_path}")
    except Exception as e:
        print(f"Error al cargar el icono: {e}")

    game = TicTacToe(root)
    root.mainloop()