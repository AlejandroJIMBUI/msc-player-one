import os
from PyQt6.QtWidgets import QListWidget, QListWidgetItem
from PyQt6.QtCore import Qt

class PlaylistManager:
    def __init__(self):
        self.playlists = {"Favoritos": []}
        self.current_playlist = "Favoritos"
        self.playlist_selector = QListWidget()
        self.playlist_list = QListWidget()

    def create_new_playlist(self, name):
        if name not in self.playlists:
            self.playlists[name] = []
        else:
            raise ValueError("Ya existe una playlist con ese nombre")

    def change_playlist(self, name):
        self.current_playlist = name
        self.update_playlist_list()

    def update_playlist_list(self):
        self.playlist_list.clear()
        for song in self.playlists[self.current_playlist]:
            item = QListWidgetItem(os.path.basename(song))
            item.setData(Qt.ItemDataRole.UserRole, song)
            self.playlist_list.addItem(item)

    def add_to_playlist(self, song_path):
        if song_path not in self.playlists[self.current_playlist]:
            self.playlists[self.current_playlist].append(song_path)