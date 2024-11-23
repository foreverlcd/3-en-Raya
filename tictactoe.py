import os
import sys

# Redirigir la salida estándar y la salida de error estándar a os.devnull
sys.stdout = open(os.devnull, 'w')
sys.stderr = open(os.devnull, 'w')

import pygame

# Restaurar la salida estándar y la salida de error estándar
sys.stdout = sys.__stdout__
sys.stderr = sys.__stderr__

import tkinter as tk
from PIL import Image, ImageTk
import random
from utils import load_sound, load_questions
import webbrowser

class TicTacToe:
    def __init__(self, root):
        self.root = root
        self.root.title("3 en Raya")
        self.root.configure(bg='#1a1a1a')
        self.root.state('zoomed')
        self.player = "X"
        self.buttons = [[None for _ in range(3)] for _ in range(3)]
        self.moves = []
        self.score_x = 0
        self.score_o = 0
        self.score_label = None
        self.custom_game = False
        self.questions = load_questions()
        self.used_questions = []

        # Redirigir la salida estándar y la salida de error estándar a os.devnull durante la inicialización de pygame
        sys.stdout = open(os.devnull, 'w')
        sys.stderr = open(os.devnull, 'w')
        pygame.mixer.init()
        sys.stdout = sys.__stdout__
        sys.stderr = sys.__stderr__

        self.sounds = {
            'click': load_sound('music/click.wav'),
            'victory': load_sound('music/victory.wav'),
            'draw': load_sound('music/draw.wav'),
            'question': load_sound('music/question.wav'),
            'menu': load_sound('music/menu.wav')
        }
        self.create_background()
        self.create_menu()
        self.create_developer_label()

    def create_background(self):
        self.canvas = tk.Canvas(self.root, width=self.root.winfo_screenwidth(), height=self.root.winfo_screenheight())
        self.canvas.pack(fill="both", expand=True)
        
        # Inicializar background_photo como None
        self.background_photo = None
        
        try:
            # Usar resource_path para la ruta de la imagen
            from utils import resource_path
            background_path = resource_path("image/fondo.jpg")
            self.background_image = Image.open(background_path)
            self.background_image = self.background_image.resize(
                (self.root.winfo_screenwidth(), self.root.winfo_screenheight()), 
                Image.LANCZOS
            )
            self.background_photo = ImageTk.PhotoImage(self.background_image)
            self.canvas.create_image(0, 0, image=self.background_photo, anchor=tk.NW)
        except Exception as e:
            print(f"Error al cargar el fondo: {e}")
            # Establecer un color de fondo por defecto si falla la carga de la imagen
            self.canvas.configure(bg='#1a1a1a')
        
        # Mantener la referencia incluso si es None
        self.canvas.image = self.background_photo

    def create_developer_label(self):
        developer_label = tk.Label(self.root, text="Developed by foreverlcd - Team DeadHack", font=('normal', 10), bg='#1a1a1a', fg='cyan')
        developer_label.place(relx=1.0, rely=1.0, anchor='se')

    def play_sound(self, sound_name):
        try:
            pygame.mixer.stop()
            if self.sounds[sound_name]:
                self.sounds[sound_name].play()
        except KeyError:
            pass
        except pygame.error:
            pass

    def create_menu(self):
        self.clear_board()
        self.play_sound('menu')
        menu_frame = tk.Frame(self.canvas, bg='#1a1a1a', padx=20, pady=20)
        menu_frame.pack(expand=True)
        try:
            self.menu_image = Image.open("image/logo.png")
            self.menu_image = self.menu_image.resize((400, 300), Image.LANCZOS)
            self.menu_photo = ImageTk.PhotoImage(self.menu_image)
            image_label = tk.Label(menu_frame, image=self.menu_photo, bg='#1a1a1a')
            image_label.pack(pady=20)
        except Exception as e:
            pass

        def button_click(command):
            command()

        tk.Button(menu_frame, text="Nuevo Juego", font=('normal', 20), bg='#1a1a1a', fg='cyan',
                  activebackground='cyan', activeforeground='#1a1a1a', relief='flat', bd=5,
                  command=lambda: button_click(self.start_game)).pack(pady=20)
        tk.Button(menu_frame, text="Versión Personalizada", font=('normal', 20), bg='#1a1a1a', fg='cyan',
                  activebackground='cyan', activeforeground='#1a1a1a', relief='flat', bd=5,
                  command=lambda: button_click(self.start_custom_game)).pack(pady=20)
        tk.Button(menu_frame, text="More Info", font=('normal', 20), bg='#1a1a1a', fg='cyan',
                  activebackground='cyan', activeforeground='#1a1a1a', relief='flat', bd=5,
                  command=self.show_about).pack(pady=20)
        tk.Button(menu_frame, text="Salir", font=('normal', 20), bg='#1a1a1a', fg='cyan',
                  activebackground='cyan', activeforeground='#1a1a1a', relief='flat', bd=5,
                  command=self.root.quit).pack(pady=20)

    def show_about(self):
        about_window = tk.Toplevel(self.root)
        about_window.title("More Info")
        about_window.configure(bg='#1a1a1a')
        about_window.geometry("400x300")
        about_window.overrideredirect(True)  # Quitar botones de cerrar, minimizar y maximizar
        content_frame = tk.Frame(about_window, bg='#333333', bd=10, relief='ridge')
        content_frame.pack(expand=True, fill='both', padx=10, pady=10)
        tk.Label(content_frame, text="Desarrollado por foreverlcd (Jhon) - Team DeadHack", 
                font=('normal', 20), bg='#333333', fg='cyan', wraplength=350).pack(pady=20)
        linkedIn_label = tk.Label(content_frame, text="LinkedIn", font=('normal', 12), 
                                bg='#333333', fg='#1e90ff', cursor="hand2", relief="flat")
        linkedIn_label.pack(pady=5)
        linkedIn_label.bind("<Button-1>", lambda e: self.open_link("https://www.linkedin.com/in/jhonjesusqm"))
        github_label = tk.Label(content_frame, text="GitHub", font=('normal', 12), 
                                bg='#333333', fg='#ff6600', cursor="hand2", relief="flat")
        github_label.pack(pady=5)
        github_label.bind("<Button-1>", lambda e: self.open_link("https://github.com/foreverlcd"))
        tk.Button(content_frame, text="Cerrar", font=('normal', 20), bg='lightgrey', fg='black', 
                width=10, command=about_window.destroy).pack(pady=20)
        self.root.update_idletasks()
        width = 400
        height = 300
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        about_window.geometry(f"{width}x{height}+{x}+{y}")

    def open_link(self, url):
        webbrowser.open_new(url)

    def start_game(self):
        self.custom_game = False
        self.clear_board()
        self.create_score_label()
        self.create_buttons()
        self.create_back_to_menu_button()

    def start_custom_game(self):
        self.custom_game = True
        self.clear_board()
        self.create_score_label()
        self.create_buttons()
        self.create_back_to_menu_button()

    def create_score_label(self):
        score_frame = tk.Frame(self.canvas, bg='#1a1a1a', padx=20, pady=20, relief='ridge', bd=5)
        score_frame.place(relx=0.95, rely=0.05, anchor='ne')  # Ajusta 'relx' y 'rely' para mover la barra de puntuación
        self.score_label = tk.Label(score_frame, text=f"Jugador X: {self.score_x}  Jugador O: {self.score_o}",
                                    font=('normal', 20), bg='#333333', fg='cyan', padx=10, pady=10)
        self.score_label.pack()

    def create_buttons(self):
        button_frame = tk.Frame(self.canvas, bg='#1a1a1a', padx=20, pady=20)
        button_frame.place(relx=0.33, rely=0.5, anchor='center')  # Ajusta 'rely' para subir el tablero
        for i in range(3):
            for j in range(3):
                self.buttons[i][j] = tk.Button(button_frame, text=str(i * 3 + j + 1), font=('normal', 16),
                                            width=20, height=10, bg='white', fg='black',
                                            activebackground='white', activeforeground='black',
                                            relief='solid', bd=2, highlightbackground='white', highlightthickness=2,
                                            wraplength=200, justify="center",
                                            command=lambda i=i, j=j: self.on_button_click(i, j))
                self.buttons[i][j].grid(row=i, column=j, padx=5, pady=5)

    def create_back_to_menu_button(self):
        tk.Button(self.canvas, text="Regresar al Menú", font=('normal', 20), bg='#1a1a1a', fg='cyan',
                activebackground='cyan', activeforeground='#1a1a1a', relief='flat', bd=5,
                command=lambda: self.create_menu()).place(relx=0.83, rely=0.9, anchor='center')  # Ajusta 'rely' para posicionar el botón

    def on_button_click(self, i, j):
        if self.custom_game and self.buttons[i][j]["text"].isdigit():
            self.play_sound('question')
            self.show_question(i, j)
        elif not self.custom_game and self.buttons[i][j]["text"].isdigit():
            self.play_sound('click')
            self.mark_square(i, j, self.player)
            self.player = "O" if self.player == "X" else "X"

    def show_question(self, i, j):
        if len(self.used_questions) == len(self.questions):
            self.used_questions = []
        question = random.choice([q for q in self.questions if q not in self.used_questions])
        self.used_questions.append(question)
        self.buttons[i][j].config(text=question, bg='lightyellow', state='disabled')
        self.show_player_selector(i, j)

    def show_player_selector(self, i, j):
        selector_frame = tk.Frame(self.canvas, bg='#1a1a1a', padx=20, pady=20)
        selector_frame.place(relx=0.8, rely=0.5, anchor=tk.CENTER)
        tk.Label(selector_frame, text="Elige X o O:", font=('normal', 20), bg='#1a1a1a', fg='cyan').pack(pady=10)
        button_frame = tk.Frame(selector_frame, bg='#1a1a1a')
        button_frame.pack()
        tk.Button(button_frame, text="X", font=('normal', 20), bg='#00ff00', fg='black', width=5,  # Verde más intenso
                  command=lambda: self.set_custom_player(i, j, "X", selector_frame)).pack(side=tk.LEFT, padx=20, pady=20)
        tk.Button(button_frame, text="O", font=('normal', 20), bg='#ff0000', fg='black', width=5,  # Rojo más intenso
                  command=lambda: self.set_custom_player(i, j, "O", selector_frame)).pack(side=tk.LEFT, padx=20, pady=20)
        tk.Button(button_frame, text="Deshacer", font=('normal', 20), bg='lightgrey', fg='black', width=10,
                  command=lambda: self.undo_question(i, j, selector_frame)).pack(side=tk.LEFT, padx=20, pady=20)

    def set_custom_player(self, i, j, player, frame):
        self.play_sound('click')
        self.buttons[i][j]["text"] = player
        self.buttons[i][j]["bg"] = '#00ff00' if player == 'X' else '#ff0000'  # Verde y rojo más intensos
        self.moves.append((i, j))
        frame.destroy()
        if self.check_winner():
            self.play_sound('victory')
            self.mark_winning_line()
            self.show_victory_message(player)
            self.update_score(player)
        elif self.is_draw():
            self.play_sound('draw')
            self.show_draw_message()
            self.reset_board()
            
    def undo_question(self, i, j, frame):
        pygame.mixer.stop()  # Detener todos los sonidos
        self.buttons[i][j].config(text=str(i * 3 + j + 1), bg='white', fg='black', state='normal')
        frame.destroy()

    def mark_square(self, i, j, player):
        self.buttons[i][j].config(text=player, bg='#00ff00' if player == 'X' else '#ff0000', state='disabled')  # Verde y rojo más intensos
        self.moves.append((i, j))
        if self.check_winner():
            self.play_sound('victory')
            self.mark_winning_line()
            self.show_victory_message(player)
            self.update_score(player)
        elif self.is_draw():
            self.play_sound('draw')
            self.show_draw_message()
            self.reset_board()

    def check_winner(self):
        self.winning_line = []
        for i in range(3):
            if self.buttons[i][0]["text"] == self.buttons[i][1]["text"] == self.buttons[i][2]["text"] != "":
                self.winning_line = [(i, 0), (i, 1), (i, 2)]
                return True
            if self.buttons[0][i]["text"] == self.buttons[1][i]["text"] == self.buttons[2][i]["text"] != "":
                self.winning_line = [(0, i), (1, i), (2, i)]
                return True
        if self.buttons[0][0]["text"] == self.buttons[1][1]["text"] == self.buttons[2][2]["text"] != "":
            self.winning_line = [(0, 0), (1, 1), (2, 2)]
            return True
        if self.buttons[0][2]["text"] == self.buttons[1][1]["text"] == self.buttons[2][0]["text"] != "":
            self.winning_line = [(0, 2), (1, 1), (2, 0)]
            return True
        return False

    def is_draw(self):
        return all(self.buttons[i][j]["text"] in ["X", "O"] for i in range(3) for j in range(3))

    def mark_winning_line(self):
        for (i, j) in self.winning_line:
            self.buttons[i][j]["bg"] = 'purple'

    def show_victory_message(self, player):
        victory_window = tk.Toplevel(self.root)
        victory_window.title("¡Victoria!")
        victory_window.configure(bg='#1a1a1a')
        victory_window.geometry("400x250")
        victory_window.overrideredirect(True)
        victory_window.update_idletasks()
        x = (self.root.winfo_screenwidth() - victory_window.winfo_reqwidth()) // 2
        y = (self.root.winfo_screenheight() - victory_window.winfo_reqheight()) // 2
        victory_window.geometry(f"+{x}+{y}")
        content_frame = tk.Frame(victory_window, bg='#333333', bd=10, relief='ridge')
        content_frame.pack(expand=True, fill='both', padx=10, pady=10)
        tk.Label(content_frame, text=f"¡Felicidades! Jugador {player} gana!", font=('normal', 20), 
                bg='#333333', fg='cyan', wraplength=350).pack(pady=20)
        tk.Button(content_frame, text="Aceptar", font=('normal', 20), bg='lightgreen', fg='black', 
                 width=10, command=victory_window.destroy).pack(pady=20)
        self.root.after(2000, self.reset_board)

    def show_draw_message(self):
        draw_window = tk.Toplevel(self.root)
        draw_window.title("¡Empate!")
        draw_window.configure(bg='#1a1a1a')
        draw_window.geometry("400x200")
        draw_window.overrideredirect(True)
        draw_window.update_idletasks()
        x = (self.root.winfo_screenwidth() - draw_window.winfo_reqwidth()) // 2
        y = (self.root.winfo_screenheight() - draw_window.winfo_reqheight()) // 2
        draw_window.geometry(f"+{x}+{y}")
        content_frame = tk.Frame(draw_window, bg='#333333', bd=10, relief='ridge')
        content_frame.pack(expand=True, fill='both', padx=10, pady=10)
        tk.Label(content_frame, text="¡Es un empate!", font=('normal', 20), 
                bg='#333333', fg='cyan', wraplength=350).pack(pady=20)
        tk.Button(content_frame, text="Aceptar", font=('normal', 20), bg='lightgrey', fg='black', 
                 width=10, command=draw_window.destroy).pack(pady=20)
        self.root.after(2000, self.reset_board)

    def update_score(self, player):
        if player == "X":
            self.score_x += 1
        else:
            self.score_o += 1
        self.score_label.config(text=f"Jugador X: {self.score_x}  Jugador O: {self.score_o}")

    def reset_board(self):
        for i in range(3):
            for j in range(3):
                if self.buttons[i][j].winfo_exists():
                    self.buttons[i][j].config(text=str(i * 3 + j + 1), bg='white', fg='black', state='normal')
        self.moves.clear()

    def clear_board(self):
        for widget in self.canvas.winfo_children():
            widget.destroy()