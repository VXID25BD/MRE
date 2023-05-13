import configparser
from dataclasses import dataclass


@dataclass
class DB:
    user: str
    password: str
    host: str
    port: str
    schema: str
    max_pool_size: int


@dataclass
class Config:
    db: DB


def load_config(path: str = "run.ini") -> Config:
    config: configparser.ConfigParser = configparser.ConfigParser()
    config.read(path)

    db: configparser.SectionProxy = config["db"]

    return Config(
        db=DB(
            user=db.get("user"),
            password=db.get("password"),
            host=db.get("host"),
            port=db.get("port"),
            schema=db.get("schema"),
            max_pool_size=db.getint("max_pool_size"),
        ),
    )
