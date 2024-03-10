from psycopg_pool import ConnectionPool
from api.settings import settings
from api.singleton.singleton import SingletonMeta

class Database(metaclass = SingletonMeta):
    def __init__(self) -> None:
        self.pool = ConnectionPool(
            settings.database_url,
            max_size= settings.database_pool_max_size,
            min_size= settings.database_pool_min_size,
            open= True
        )
    
