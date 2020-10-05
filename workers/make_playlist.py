from song import Song
from typing import List
from image import b64image
import os
import json

__all__ = ["make_playlist"]


def make_playlist(songs: List[Song], game_path: str, name: str) -> None:
    # paths and directories
    playlist_dir = os.path.join(game_path, "Playlists")
    os.makedirs(playlist_dir, exist_ok=True)
    playlist_file = os.path.join(playlist_dir, f"{name.lower()}.bplist")

    # filter only unique songs
    song_hashes = set()
    filtered_song = []
    for song in songs:
        if song.hash not in song_hashes:
            song_hashes.add(song.hash)
            filtered_song.append(song)

    # playlist data
    playlist = {
        "playlistTitle": name,
        "playlistAuthor": "Norne",
        "image": b64image(),
        "songs": [{"key": s.key, "hash": s.hash, "songName": s.song_name, "uploader": s.uploader}
                  for s in filtered_song]
    }

    # write to file
    with open(playlist_file, "w") as f:
        json.dump(playlist, f)
