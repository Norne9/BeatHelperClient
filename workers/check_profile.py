import cloudscraper
from bs4 import BeautifulSoup
from typing import Callable, List
from workers.stoppable_thread import StoppableThread

__all__ = ["CheckProfileWorker"]


class CheckProfileWorker(StoppableThread):
    user_id: str
    on_done: Callable[[float, float], None]
    on_fail: Callable[[str], None]
    scraper: cloudscraper.CloudScraper

    def __init__(self, user_id: str, on_done: Callable[[float, float], None],
                 on_fail: Callable[[str], None]):
        super(CheckProfileWorker, self).__init__()
        self.user_id = user_id
        self.on_done = on_done
        self.on_fail = on_fail
        self.scraper = cloudscraper.create_scraper()

    def run(self) -> None:
        try:
            avg_scores = self.get_scores(1)
            avg = sum(avg_scores) / len(avg_scores)

            low_scores = self.get_scores(3)
            low = min(low_scores)

            # print(f"Lowest: {low} | Average: {avg}")
            self.on_done(low, avg)
        except Exception as e:
            self.on_fail(str(e))

    def get_scores(self, page) -> List[float]:
        data = self.scraper.get(f"https://scoresaber.com/u/{self.user_id}&page={page}&sort=1").text
        soup = BeautifulSoup(data, "html.parser")
        return [float(e.text) for e in soup.find_all("span", {"class": "scoreTop ppValue"})]
