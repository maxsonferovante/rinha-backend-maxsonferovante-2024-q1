from psycopg.errors import CheckViolation, RaiseException
from psycopg.rows import dict_row

from api.exception.exceptions import InsufficientBalance, ClientNotFound
from api.infra.model import Transaction
from api.infra.database import Database
from api.singleton.singleton import SingletonMeta

class ClientRepository(metaclass = SingletonMeta):
    def __init__(self) -> None:
        self.pool = Database().pool

    def get_client(self, client_id: int):
        with self.pool.connection() as conn:            
            with conn.cursor(row_factory=dict_row, binary=True) as cursor:                
                try:
                    row = cursor.execute("SELECT get_client(%(id)s)",{"id": client_id}, prepare=True).fetchone()                
                    return row
                except RaiseException:
                    raise ClientNotFound
            
    def add_transaction(self, client_id: int, transaction: Transaction):
         with self.pool.connection() as conn:
            with conn.cursor(row_factory=dict_row, binary=True) as cur:
                try:
                    return cur.execute(
                        "SELECT add_transaction(%(id)s, %(transaction)s)",
                        {"id": client_id, "transaction": transaction.model_dump_json(by_alias=True)},
                        prepare=True,
                    ).fetchone()
                except RaiseException:
                    raise ClientNotFound
                except CheckViolation:
                    raise InsufficientBalance

        