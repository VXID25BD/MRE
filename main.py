from typing import List

from app.config import Config, load_config
from app.db.db_interaction import DBInteraction
from app.file_manager import FileManager
from app.worker import WalletWorker


def main() -> None:
    config: Config = load_config()
    addresses: List[str] = FileManager.read_lines(path="case.txt")

    db_interaction: DBInteraction = DBInteraction(
        user=config.db.user,
        password=config.db.password,
        schema=config.db.schema,
        host=config.db.host,
        port=config.db.port,
        pool_size=config.db.max_pool_size
    )

    pool_size: int = config.db.max_pool_size if len(addresses) > config.db.max_pool_size else len(addresses)

    connection = db_interaction.get_connection()
    db_interaction.put_connection(connection=connection)
    wallet_worker: WalletWorker = WalletWorker(
        items=addresses,
        db_interaction=db_interaction,
        num_threads=pool_size,
    )
    wallet_worker.worker()


if __name__ == "__main__":
    main()
