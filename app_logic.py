from song_manager import SongManager, Song
from typing import Callable, List, Optional
from workers.stoppable_thread import StoppableThread
from workers.fetch_songs import FetchSongsWorker
from workers.download_songs import DownloadSongsWorker
from workers.make_playlist import make_playlist

__all__ = ["AppLogic"]


class AppLogic:
    game_path: str
    playlist_name: str
    song_manager: SongManager
    show_songs: Callable[[List[Song]], None]
    show_message: Callable[[str], None]
    set_status: Callable[[str], None]
    set_buttons: Callable[[bool], None]
    update_progress: Callable[[float], None]
    worker: Optional[StoppableThread]
    current_songs: List[Song]

    def __init__(self, game_path: str, show_songs: Callable[[List[Song]], None], show_message: Callable[[str], None],
                 set_buttons: Callable[[bool], None], set_status: Callable[[str], None],
                 update_progress: Callable[[float], None]):
        self.game_path = game_path
        self.song_manager = SongManager(game_path)
        self.show_songs = show_songs
        self.show_message = show_message
        self.set_buttons = set_buttons
        self.set_status = set_status
        self.update_progress = update_progress
        self.worker = None
        self.current_songs = []

    def set_path(self, path: str):
        self.game_path = path
        self.song_manager.game_path = path

    def cancel_task(self):
        if self.worker is not None and not self.worker.stopped():
            self.worker.stop()
            self.worker.join()

    def find_songs(self, min_score: float):
        self.playlist_name = "Top"
        self.__fetch_songs(min_score, 10000)

    def recommend_songs(self, player_link: str):
        pass

    def download(self):
        if len(self.current_songs) == 0:
            return

        self.cancel_task()
        self.song_manager.check_exist(self.current_songs)
        song_count = len(self.current_songs)

        def on_done():
            self.song_manager.check_exist(self.current_songs)
            new_song_count = sum(1 for s in self.current_songs if s.downloaded)
            self.show_songs(self.current_songs)
            make_playlist(self.current_songs, self.game_path, self.playlist_name)
            self.set_buttons(True)
            self.set_status(f"Downloaded {new_song_count}/{song_count} songs.")

        def update_progress(progress: float):
            self.song_manager.check_exist(self.current_songs)
            self.show_songs(self.current_songs)
            self.update_progress(progress)

        self.set_buttons(False)
        self.set_status("Downloading songs...")
        self.worker = DownloadSongsWorker(self.current_songs, self.game_path, on_done,
                                          update_progress, self.set_status)
        self.worker.start()

    def __fetch_songs(self, min_score: float, avg_score: float):
        def on_done(songs: List[Song]):
            self.song_manager.check_exist(songs)
            songs.sort(key=lambda s: s.best_score)
            self.current_songs = songs
            self.set_status(f"Found {len(songs)} songs")
            self.show_songs(songs)
            self.set_buttons(True)

        def on_message(msg: str):
            self.set_status("Search failed")
            self.show_message(f"Error: {msg}")
            self.show_songs([])
            self.set_buttons(True)

        self.set_buttons(False)
        self.set_status("Searching songs...")
        FetchSongsWorker(min_score, avg_score, on_done, on_message).start()

