import os
import eyed3
from mutagen.flac import FLAC
from PyQt6.QtWidgets import QLineEdit, QListWidget, QListWidgetItem, QMenu
from PyQt6.QtGui import QAction
from PyQt6.QtCore import Qt  

class LibraryManager:
    def __init__(self, playlist_manager):
        self.music_library = []
        self.search_box = QLineEdit()
        self.library_list = QListWidget()
        self.library_list = QListWidget()
        self.library_list.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.library_list.customContextMenuRequested.connect(self.show_context_menu)
        self.playlist_manager = playlist_manager

    def add_music_folder(self, folder):
        supported_formats = ['.mp3', '.wav', '.ogg', '.flac', '.m4a']
        for root, dirs, files in os.walk(folder):
            for file in files:
                if any(file.lower().endswith(format) for format in supported_formats):
                    path = os.path.join(root, file)
                    self.music_library.append(path)

    def update_library_list(self):
        self.library_list.clear()
        for song in self.music_library:
            item = QListWidgetItem(os.path.basename(song))
            item.setData(Qt.ItemDataRole.UserRole, song)
            self.library_list.addItem(item)

    def search_music(self, search_text):
        self.library_list.clear()
        for song in self.music_library:
            if search_text in os.path.basename(song).lower():
                item = QListWidgetItem(os.path.basename(song))
                item.setData(Qt.ItemDataRole.UserRole, song)
                self.library_list.addItem(item)

    def get_song_metadata(self, song_path):
        try:
            # Intentamos leer los metadatos del archivo .mp3 con eyed3
            if song_path.lower().endswith('.mp3'):
                return self.get_mp3_metadata(song_path)
            
            # Si el archivo es .flac, utilizamos mutagen para obtener los metadatos
            elif song_path.lower().endswith('.flac'):
                return self.get_flac_metadata(song_path)

            # Si el archivo no es compatible, devolvemos valores por defecto
            return "Desconocido", "Desconocido", "Desconocido", None

        except Exception as e:
            print(f"Error al obtener metadatos de la canción {song_path}: {e}")
            return "Desconocido", "Desconocido", "Desconocido", None

    def get_mp3_metadata(self, song_path):
        try:
            audio_file = eyed3.load(song_path)
            if audio_file is None or audio_file.tag is None:
                raise ValueError(f"Archivo no tiene etiquetas ID3: {song_path}")

            title = audio_file.tag.title if audio_file.tag.title else "Desconocido"
            artist = audio_file.tag.artist if audio_file.tag.artist else "Desconocido"
            album = audio_file.tag.album if audio_file.tag.album else "Desconocido"
            album_art = None

            # Find the frame Apic for the cover art
            if audio_file.tag.images:
                album_art = audio_file.tag.images[0].image_data

            return title, artist, album, album_art

        except Exception as e:
            print(f"Error al leer metadatos MP3: {e}")
            return "Desconocido", "Desconocido", "Desconocido", None

    def get_flac_metadata(self, song_path):
        audio_file = FLAC(song_path)
        title = audio_file.tags.get('title', ['Desconocido'])[0]
        artist = audio_file.tags.get('artist', ['Desconocido'])[0]
        album = audio_file.tags.get('album', ['Desconocido'])[0]
        album_art = None

        # Extraer la carátula de audio_file.pictures
        if audio_file.pictures:
            album_art = audio_file.pictures[0].data

        return title, artist, album, album_art
    
    def show_context_menu(self, position):
        item = self.library_list.itemAt(position)
        if item is not None:
            menu = QMenu()
            action_add_to_queue = QAction("Añadir a la cola", self.library_list)
            action_add_to_playlist = QAction("Agregar a playlist", self.library_list)
            action_play = QAction("Reproducir", self.library_list)
            action_delete = QAction("Eliminar", self.library_list)

            # Aquí puedes conectar las acciones a métodos específicos si lo deseas
            # action_add_to_queue.triggered.connect(lambda: self.add_to_queue(item))
            # action_add_to_playlist.triggered.connect(lambda: self.add_to_playlist(item))
            # action_play.triggered.connect(lambda: self.play_song(item))
            # action_delete.triggered.connect(lambda: self.delete_song(item))

            menu.addAction(action_add_to_queue)
            menu.addAction(action_add_to_playlist)
            menu.addAction(action_play)
            menu.addAction(action_delete)
            menu.exec(self.library_list.viewport().mapToGlobal(position))   

    def show_context_menu(self, position):
        item = self.library_list.itemAt(position)
        if item is not None:
            menu = QMenu()
            action_add_to_queue = QAction("Añadir a la cola", self.library_list)
            action_add_to_playlist = QAction("Agregar a playlist", self.library_list)
            action_play = QAction("Reproducir", self.library_list)
            action_delete = QAction("Eliminar", self.library_list)

            # Conectar la acción de agregar a playlist
            action_add_to_playlist.triggered.connect(lambda: self.add_song_to_playlist(item))

            menu.addAction(action_add_to_queue)
            menu.addAction(action_add_to_playlist)
            menu.addAction(action_play)
            menu.addAction(action_delete)
            menu.exec(self.library_list.viewport().mapToGlobal(position))

    def add_song_to_playlist(self, item):
        song_path = item.data(Qt.ItemDataRole.UserRole)
        self.playlist_manager.show_add_to_playlist_dialog(song_path)