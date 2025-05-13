from PyQt6.QtWidgets import QSlider
from PyQt6.QtCore import Qt

class PlayerControls:
    def __init__(self, media_player, audio_output):
        self.media_player = media_player
        self.audio_output = audio_output
        self.progress_slider = QSlider(Qt.Orientation.Horizontal)
        self.volume_slider = QSlider(Qt.Orientation.Horizontal)

    def set_volume(self, value):
        self.audio_output.setVolume(value / 100)

    def set_position(self, position):
        if self.media_player.duration() > 0:
            self.media_player.setPosition(position * self.media_player.duration() // 100)

    def update_position(self):
        if self.media_player.duration() > 0:
            position = self.media_player.position() * 100 // self.media_player.duration()
            self.progress_slider.setValue(position)