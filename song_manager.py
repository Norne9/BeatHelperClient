from song import Song
from typing import List
import os

__all__ = ["SongManager"]


class SongManager:
    game_path: str

    def __init__(self, game_path):
        self.game_path = game_path

    def check_exist(self, songs: List[Song]):
        songs_path = os.path.join(self.game_path, "Beat Saber_Data", "CustomLevels")
        song_keys = [d.split()[0].lower() for _, dirs, _ in os.walk(songs_path) for d in dirs]
        for song in songs:
            song.downloaded = song.key in song_keys
