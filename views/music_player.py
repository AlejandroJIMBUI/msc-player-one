from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                             QPushButton, QLabel, QFileDialog,
                             QTabWidget, QMessageBox, QInputDialog)
from PyQt6.QtCore import Qt, QUrl, QTimer
from PyQt6.QtMultimedia import QMediaPlayer, QAudioOutput
from PyQt6.QtGui import QIcon

#imports of models. package
from models.library_manager import LibraryManager
from models.palylist_manager import PlaylistManager
from models.player_controls import PlayerControls
from models.album_info import AlbumInfo

class MusicPlayer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Reproductor de Música")
        self.setGeometry(100, 100, 800, 600)
        self.setWindowIcon(QIcon("icon.png"))

        # Configuración del reproductor multimedia
        self.media_player = QMediaPlayer()
        self.audio_output = QAudioOutput()
        self.media_player.setAudioOutput(self.audio_output)

        # Inicialización de clases auxiliares
        self.library_manager = LibraryManager()
        self.playlist_manager = PlaylistManager()
        self.player_controls = PlayerControls(self.media_player, self.audio_output)
        self.album_info = AlbumInfo()

        # Interfaz de usuario
        self.init_ui()

        # Temporizador para actualizar la barra de progreso
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.player_controls.update_position)
        self.timer.start(1000)

    def init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)

        # Panel izquierdo (biblioteca y playlists)
        left_panel = QWidget()
        left_layout = QVBoxLayout(left_panel)

        self.tabs = QTabWidget()

        # Pestaña de biblioteca
        self.library_tab = QWidget()
        library_layout = QVBoxLayout(self.library_tab)

        self.library_manager.search_box.setPlaceholderText("Buscar...")
        self.library_manager.search_box.textChanged.connect(self.library_manager.search_music)
        library_layout.addWidget(self.library_manager.search_box)

        self.library_manager.library_list.itemDoubleClicked.connect(self.play_selected_song)
        library_layout.addWidget(self.library_manager.library_list)

        add_folder_btn = QPushButton("Agregar Carpeta")
        add_folder_btn.clicked.connect(self.add_music_folder)
        library_layout.addWidget(add_folder_btn)

        self.tabs.addTab(self.library_tab, "Biblioteca")

        # Pestaña de playlists
        self.playlists_tab = QWidget()
        playlists_layout = QVBoxLayout(self.playlists_tab)

        self.playlist_manager.playlist_selector.itemClicked.connect(self.change_playlist)
        playlists_layout.addWidget(self.playlist_manager.playlist_selector)

        self.playlist_manager.playlist_list.itemDoubleClicked.connect(self.play_selected_song)
        playlists_layout.addWidget(self.playlist_manager.playlist_list)

        new_playlist_btn = QPushButton("Nueva Playlist")
        new_playlist_btn.clicked.connect(self.create_new_playlist)
        playlists_layout.addWidget(new_playlist_btn)

        self.tabs.addTab(self.playlists_tab, "Playlists")

        left_layout.addWidget(self.tabs)

        # Panel derecho (reproductor e información)
        right_panel = QWidget()
        right_layout = QVBoxLayout(right_panel)

        self.album_info.update_album_info("Desconocido", "Desconocido", "Desconocido", None)
        right_layout.addWidget(self.album_info.album_art)
        right_layout.addWidget(self.album_info.song_info)

        # Controles de reproducción
        self.player_controls.progress_slider.sliderMoved.connect(self.player_controls.set_position)

        right_layout.addWidget(self.player_controls.progress_slider)

        buttons_layout = QHBoxLayout()
        self.prev_btn = QPushButton("Anterior")
        self.prev_btn.clicked.connect(self.play_previous)
        buttons_layout.addWidget(self.prev_btn)

        self.play_btn = QPushButton("Reproducir")
        self.play_btn.clicked.connect(self.toggle_play)
        buttons_layout.addWidget(self.play_btn)

        self.next_btn = QPushButton("Siguiente")
        self.next_btn.clicked.connect(self.play_next)
        buttons_layout.addWidget(self.next_btn)

        right_layout.addLayout(buttons_layout)

        self.player_controls.volume_slider.valueChanged.connect(self.player_controls.set_volume)
        right_layout.addWidget(QLabel("Volumen:"))
        right_layout.addWidget(self.player_controls.volume_slider)

        main_layout.addWidget(left_panel, 3)
        main_layout.addWidget(right_panel, 2)

        # Conectar señales del reproductor
        self.media_player.positionChanged.connect(self.player_controls.update_position)

    def add_music_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Seleccionar carpeta de música")
        if folder:
            self.library_manager.add_music_folder(folder)
            self.library_manager.update_library_list()

    def play_selected_song(self, item):
        song_path = item.data(Qt.ItemDataRole.UserRole)
        self.play_song(song_path)

    def play_song(self, path):
        self.media_player.setSource(QUrl.fromLocalFile(path))
        self.media_player.play()

        # Leer metadatos de la canción
        title, artist, album, album_art_data = self.library_manager.get_song_metadata(path)
        self.album_info.update_album_info(title, artist, album, album_art_data)

    def toggle_play(self):
        if self.media_player.playbackState() == QMediaPlayer.PlaybackState.PlayingState:
            self.media_player.pause()
        else:
            if self.media_player.source().isEmpty():
                if self.library_manager.music_library:
                    self.play_song(self.library_manager.music_library[0])
            else:
                self.media_player.play()

    def play_next(self):
        if self.library_manager.music_library:
            current_index = self.library_manager.music_library.index(self.media_player.source().toLocalFile())
            if current_index < len(self.library_manager.music_library) - 1:
                self.play_song(self.library_manager.music_library[current_index + 1])

    def play_previous(self):
        if self.library_manager.music_library:
            current_index = self.library_manager.music_library.index(self.media_player.source().toLocalFile())
            if current_index > 0:
                self.play_song(self.library_manager.music_library[current_index - 1])

    def change_playlist(self, item):
        self.playlist_manager.change_playlist(item.text())
        self.playlist_manager.update_playlist_list()

    def create_new_playlist(self):
        name, ok = QInputDialog.getText(self, "Nueva Playlist", "Nombre de la playlist:")
        if ok and name:
            try:
                self.playlist_manager.create_new_playlist(name)
            except ValueError:
                QMessageBox.warning(self, "Error", "Ya existe una playlist con ese nombre")