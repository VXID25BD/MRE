from typing import List
from termcolor import colored

from app.db.db_interaction import DBInteraction
from app.worker.threading_worker import ThreadingWorker


class WalletWorker(ThreadingWorker):

    def __init__(
            self,
            items: List[str],
            db_interaction: DBInteraction,
            num_threads: int
    ) -> None:
        super().__init__(items, db_interaction, num_threads)

    def _work(self, item: str) -> None:
        connection = self._db_interaction.get_connection()
        if not self._db_interaction.wallet_exists(connection=connection, address=item):
            print(colored(f"[+] Проверка наличия {item} -> Добавление в БД", "blue"))
            self._db_interaction.add_wallet(connection=connection, address=item)
        else:
            self._items.remove(item)
            print(colored(f"[-] Проверка наличия в {item} -> В наличие", "blue"))
        self._db_interaction.put_connection(connection=connection)
