from functools import lru_cache

from menu import config


# Возврат существующего экземпляра DBSettings вместо создания нового
@lru_cache
def get_db_settings() -> config.DBSettings:
    return config.DBSettings()
