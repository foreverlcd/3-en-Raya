# 3 en Raya

Este es un juego de "3 en Raya" desarrollado en Python utilizando las bibliotecas `tkinter` y `pygame`.  
El juego incluye una versión personalizada con preguntas, sonidos y un fondo, que puedes cambiar a tu gusto.

## Requisitos

- Python 3.x
- Pillow
- pygame

## Instalación

1. Clona este repositorio:
    ```sh
    git clone https://github.com/foreverlcd/3-en-Raya.git
    cd 3-en-Raya
    ```

2. Instala las dependencias:
    ```sh
    pip install -r requirements.txt
    ```

## Uso

Ejecuta el archivo `main.py` para iniciar el juego:
```sh
python main.py
```

## Estructura del Proyecto:
```
3-en-Raya
├── image/                  # Directorio con el fondo y el logo del juego
│   ├── fondo.jpg  
│   ├── icon.ico            
│   └── logo.png  
├── music/                  # Sonidos utilizados para los eventos del juego
│   ├── click.wav           
│   ├── draw.wav  
│   ├── menu.wav  
│   ├── question.wav  
│   └── victory.wav  
├── main.py                 # Programa principal del juego
├── preguntas.txt           
├── README.md
├── requirements.txt
├── tictactoe.py  
└── utils.py
```