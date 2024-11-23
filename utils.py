import pygame
import os
import sys

def resource_path(relative_path):
    """Obtiene la ruta absoluta de los recursos"""
    try:
        # PyInstaller crea un directorio temporal y almacena la ruta en _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    
    return os.path.join(base_path, relative_path)

def load_sound(path):
    """Cargar un sonido desde un archivo."""
    try:
        return pygame.mixer.Sound(resource_path(path))
    except pygame.error:
        return None

def load_questions():
    """Cargar preguntas desde un archivo de texto."""
    questions = []
    try:
        with open(resource_path('preguntas.txt'), 'r', encoding='utf-8') as file:
            questions = [line.strip() for line in file if line.strip()]
    except FileNotFoundError:
        questions = ["Pregunta de prueba 1", "Pregunta de prueba 2", "Pregunta de prueba 3"]
    return questions