import ctypes
import time
from concurrent.futures import ThreadPoolExecutor
from threading import RLock
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

        self._lock = RLock()

    def _work(self, item: str) -> None:
        pass

    def worker(self) -> None:
        total_items: int = len(self._items)

        with ThreadPoolExecutor(max_workers=self._num_threads) as executor:
            futures = []
            for item in self._items:
                futures.append(executor.submit(self._work, item))

            while True:
                items_left: int = len([future for future in futures if not future.done()])
                ctypes.windll.kernel32.SetConsoleTitleW(f"Проверено {total_items - items_left}/{total_items}")
                if items_left == 0:
                    break
                time.sleep(0.1)
