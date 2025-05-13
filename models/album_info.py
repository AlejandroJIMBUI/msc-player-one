import os
from PyQt6.QtWidgets import QLabel
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt

class AlbumInfo:
    def __init__(self):
        self.album_art = QLabel()
        self.song_info = QLabel("No hay canción seleccionada")

    def update_album_info(self, title, artist, album, album_art_data):
        self.song_info.setText(f"{title}\n{artist}\n{album}")

        if album_art_data:
            pixmap = QPixmap()
            pixmap.loadFromData(album_art_data)
            self.album_art.setPixmap(pixmap.scaled(200, 200, Qt.AspectRatioMode.KeepAspectRatio))
        else:
            self.album_art.setPixmap(QPixmap("default_album.png").scaled(200, 200, Qt.AspectRatioMode.KeepAspectRatio))