import cloudscraper
from song import Song
from typing import Callable, List
from workers.stoppable_thread import StoppableThread
import os
import zipfile

__all__ = ["DownloadSongsWorker"]
ZIP_FILE = "song.zip"


class DownloadSongsWorker(StoppableThread):
    update_progress: Callable[[float], None]
    on_done: Callable[[], None]
    set_status: Callable[[str], None]
    songs: List[Song]
    game_path: str
    scraper: cloudscraper.CloudScraper

    def __init__(self, songs: List[Song], game_path: str, on_done: Callable[[], None],
                 update_progress: Callable[[float], None], set_status: Callable[[str], None]):
        super(DownloadSongsWorker, self).__init__()
        self.songs = [song for song in songs if not song.downloaded]
        self.song_count = len(self.songs)
        self.game_path = game_path

        self.set_status = set_status
        self.on_done = on_done
        self.update_progress = update_progress

        self.scraper = cloudscraper.create_scraper()

    def run(self) -> None:
        for i, song in enumerate(self.songs):
            self.set_status(f"Downloading {song.song_name}")
            self.download_song(song)
            self.update_progress((i + 1) / self.song_count)
            if self.stopped():
                break
        else:
            self.update_progress(1)
        self.on_done()

    def download_song(self, song: Song):
        # song folder
        bs_songs_path = os.path.join(self.game_path, "Beat Saber_Data", "CustomLevels")
        song_path = os.path.join(bs_songs_path, song.get_filename())

        # download zip
        is_done = self.download_file(song.get_link(), ZIP_FILE)
        if not is_done:
            self.set_status(f"Failed to download {song.song_name}")
            return

        # unpack zip
        os.makedirs(song_path, exist_ok=True)
        try:
            with zipfile.ZipFile(ZIP_FILE, mode="r") as z_file:
                z_file.extractall(song_path)
        except Exception as e:
            os.removedirs(song_path)
            print(f"Zip error: {e}")
            self.set_status(f"Failed to unpack {song.song_name}")

        # delete zip
        os.remove(ZIP_FILE)

    def download_file(self, url: str, file: str) -> bool:
        try:
            with open(file, mode="wb") as f:
                resp = self.scraper.get(url, stream=True, allow_redirects=True, timeout=5.0)
                total_length = resp.headers.get("content-length")
                if total_length is None:
                    f.write(resp.content)
                else:
                    for data in resp.iter_content(chunk_size=4096):
                        f.write(data)
                        if self.stopped():
                            raise Exception("Thread stopped")
            return True
        except Exception as e:
            print(f"Download failed: {e}")
            if os.path.isfile(file):
                os.remove(file)
            return False
