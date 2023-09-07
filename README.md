# YouTube Audio Downloader

This Python script enables you to download audio from YouTube videos belonging to a specified channel.  You have the flexibility to download videos that include a specific keyword, using it as a filtering tag. Additionally, you can opt to download all videos until a particular title is encountered, allowing you to define a subset of videos for downloading.
It utilizes the Selenium web automation library to navigate the YouTube website and the PyTube library for MP3 audio extraction.

## Features

- **YouTube Video Search:** The script opens a specified YouTube channel and searches for videos that match a given title or contain a specific word in their titles.

- **Headless Mode:** It can run in headless mode, without opening a visible web browser window.

- **Custom Configuration:** The script loads configuration settings from a JSON file, allowing you to easily customize the channel URL, search criteria, and more.

- **Scroll and Load:** It automatically scrolls down the channel page to load more videos and continues loading until the desired video is found.

- **Audio Download:** When a video that matches the given criteria is found, the script will extract the audio from all the videos that were published after the specified video. The extracted audio will then be saved as MP3 files.

**Note:** If a particular title is not specified, the script will download audio from all videos available on the YouTube channel.


## Requirements

- Python 3.x
- Selenium
- PyTube
- ChromeDriver (Already in the repository)

## Installation

1. **Install Python:** You must have Python 3.x installed on your system.

2. **Install Dependencies:** Install the required Python packages using pip:

```shell
pip install selenium pytube
```

3. **Configure Settings:** Create a `config.json` file in the same directory as this script with the following format:

```json
{
    "channel_url": "https://www.youtube.com/channel/your-channel-id",  // Mandatory: It must contain the URL of the YouTube channel you want to use.
    "search_title": "Download until this Video Title",                 // Optional: It can be an empty string "" if you don't want to use this option.
    "specific_word": "Specific Keyword in Video Title"                 // Optional: It can be an empty string "" if you don't want to use this option.
}
```


## Usage

Run the script:
```shell
python main.py
```
The script will open the specified YouTube channel, search for videos based on your criteria, and download the audio of matching videos as MP3 files.


## Disclaimer

Use this script responsibly and respect the rights of content creators.

Feel free to customize and modify the script to suit your needs, and don't hesitate to reach out if you have any questions or encounter any issues.



# Descargador de Audio de canales de YouTube

Este script de Python te permite descargar audio de videos de YouTube pertenecientes a un canal específico. Tienes la flexibilidad de descargar videos que incluyan una palabra clave específica, utilizándola como una etiqueta de filtrado. Además, puedes optar por descargar todos los videos hasta que se encuentre un título en particular, lo que te permite definir un subconjunto de videos para su descarga.
Utiliza la biblioteca de automatización web Selenium para interactuar con el sitio web de YouTube y la biblioteca PyTube para descargar el audio en formato MP3.

## Características

- **Búsqueda de Videos en YouTube:** El script abre un canal de YouTube especificado y busca videos que coincidan con un título dado o que contengan una palabra específica en sus títulos.

- **Modo Oculto:** Puede funcionar en modo oculto, sin abrir una ventana visible del navegador web.

- **Configuración Personalizada:** El script carga la configuración desde un archivo JSON, lo que te permite personalizar fácilmente la URL del canal, los criterios de búsqueda y más.

- **Desplazamiento y Carga:** Realiza un desplazamiento automático hacia abajo en la página del canal para cargar más videos y continúa cargando hasta que se encuentre el video deseado.

- **Descarga de Audio:** Cuando se encuentra un video que tiene el título buscado, el script extraerá el audio de todos los videos que fueron publicados después del título especificado. El audio extraído se guardará como archivos MP3.

**Nota:** Si no se especifica un título en particular, el script descargará todos los audios de los videos que existan en el canal de YouTube.


**Requisitos**

- Python 3.x
- Selenium
- PyTube
- ChromeDriver (Ya descargado en el repositorio)

**Instalación**

1. **Instalar Python:** Debes tener Python 3.x instalado en tu sistema.

2. **Instalar Dependencias:** Instala los paquetes de Python requeridos usando pip:

```shell
pip install selenium pytube
```

3. **Configurar Ajustes:** Crea un archivo `config.json` en el mismo directorio que este script con el siguiente formato:

```json
{
  "channel_url": "https://www.youtube.com/channel/your-channel-id",             // Obligatorio
  "search_title": "Descarga hasta encontrar este Video",                        // Opcional: Puede ser un string vacío "" si no deseas utilizar esta opción. En ese caso see descargará el audio de todos los videos del canal.
  "specific_word": "Palabra Clave que tiene que estar en el Título del Video"   // Opcional: Puede ser un string vacío "" si no deseas utilizar esta opción.
}
```

**Uso**

Ejecuta el script:

```shell
python main.py
```
El script abrirá el canal de YouTube especificado, buscará videos según tus criterios y descargará el audio de los videos coincidentes como archivos MP3.


**Descargo de Responsabilidad**

Utiliza este script de manera responsable y respeta los derechos de los creadores de contenido.

Siéntete libre de personalizar y modificar el script según tus necesidades y no dudes en contactarnos si tienes alguna pregunta o encuentras algún problema.
