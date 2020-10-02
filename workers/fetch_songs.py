import requests
import json
from song import Song
from typing import Callable, List
from workers.stoppable_thread import StoppableThread


class FetchSongsWorker(StoppableThread):
    min_score: float
    avg_score: float
    on_done: Callable[[List[Song]], None]
    on_fail: Callable[[str], None]

    def __init__(self, min_score: float, avg_score: float, on_done: Callable[[List[Song]], None],
                 on_fail: Callable[[str], None]):
        super(FetchSongsWorker, self).__init__()
        self.min_score = min_score
        self.avg_score = avg_score
        self.on_done = on_done
        self.on_fail = on_fail

    def run(self) -> None:
        try:
            payload = {"minScore": self.min_score, "avgScore": self.avg_score}
            resp = requests.get("http://51.15.122.220:12380/song", params=payload, timeout=5.0)
            data = json.loads(resp.text)
            songs = [Song(song["key"], song["hash"], song["songName"], song["uploader"], song["difficulty"],
                          song["bestScore"], song["worstScore"]) for song in data]
            self.on_done(songs)
        except Exception as e:
            self.on_fail(str(e))
