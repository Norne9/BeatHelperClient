
class Song:
    key: str
    hash: str
    song_name: str
    uploader: str
    difficulty: str
    best_score: float
    worst_score: float
    downloaded: bool

    def __init__(self, key: str, hash: str, song_name: str, uploader: str,
                 difficulty: str, best_score: float, worst_score: float):
        self.key = key
        self.hash = hash
        self.song_name = song_name
        self.uploader = uploader
        self.difficulty = difficulty
        self.best_score = best_score
        self.worst_score = worst_score

    def get_link(self) -> str:
        return f"https://beatsaver.com/cdn/{self.key}/{self.hash.lower()}.zip"

    def get_filename(self) -> str:
        filename_dict = {ord(i): None for i in '<>:"\\/|?*'}
        name = self.song_name.split('-')[0].strip() if "-" in self.song_name else self.song_name
        return f"{self.key} ({name.translate(filename_dict)} - {self.uploader.translate(filename_dict)})"
