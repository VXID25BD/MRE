import ctypes
import time
from multiprocessing.pool import ThreadPool
from typing import List

from app.db.db_interaction import DBInteraction


class ThreadingWorker:
    _items: List[str]
    _db_interaction: DBInteraction
    _num_threads: int

    def __init__(
            self,
            items: List[str],
            db_interaction: DBInteraction,
            num_threads: int
    ) -> None:
        self._items: List[str] = items
        self._db_interaction: DBInteraction = db_interaction
        self._num_threads: int = num_threads

    def _work(self, item: str) -> None:
        pass

    def worker(self) -> None:
        total_items: int = len(self._items)
        thread_pool: ThreadPool = ThreadPool()
        thread_pool.map(self._work, self._items)
        with ThreadPool(processes=self._num_threads) as pool:
            tasks: List[bool] = list()
            for task in pool.map(self._work, self._items):
                while True:
                    items_left: int = len([task for task in tasks if not pool.apply_async(self._work).get()])
                    ctypes.windll.kernel32.SetConsoleTitleW(f"Проверено {total_items - items_left}/{total_items}")
                    if items_left == 0:
                        break
                    time.sleep(0.1)
