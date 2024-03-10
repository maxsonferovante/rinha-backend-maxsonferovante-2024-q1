
from http import HTTPStatus
import orjson
from pydantic import ValidationError

from api.exception.exceptions import ClientNotFound, InsufficientBalance

from api.infra.model import Transaction, Error

from api.repository.client import ClientRepository


errors = {
    "invalid_transaction_body": Error(code=1, message="dados inválidos da transação"),
    "client_not_found": Error(code=2, message="cliente não encontrado"),
    "insufficient_balance": Error(code=3, message="saldo insuficiente"),
    "url_not_found": Error(code=4, message="url não encontrada"),
}

class ClientService():

    def __init__(self) -> None:
        self.repository = ClientRepository()

    def get_client(self, client_id: int):
        try:
        
            client = self.repository.get_client(client_id)
        
        except ClientNotFound:
            return {
                "status": HTTPStatus.NOT_FOUND,
                "body": errors["client_not_found"].model_dump_json(),
            }
        
        return {
            "status": HTTPStatus.OK,
            "body": orjson.dumps(client["get_client"])
        }

    def add_transaction(self, client_id: int, transaction):
        try:
            transaction = Transaction.model_validate_json(transaction)
        except ValidationError:
            return {
                "status": HTTPStatus.UNPROCESSABLE_ENTITY,
                "body": errors["invalid_transaction_body"].model_dump_json(),
            }
        
        try:
            result = self.repository.add_transaction(client_id, transaction)
        except ClientNotFound:
            return {
                "status": HTTPStatus.NOT_FOUND,
                "body": errors["client_not_found"].model_dump_json(),
            }
        except InsufficientBalance:
            return {
                "status": HTTPStatus.UNPROCESSABLE_ENTITY,
                "body": errors["insufficient_balance"].model_dump_json(),
            }
        
        return {
            "status": HTTPStatus.OK,
            "body": orjson.dumps(result["add_transaction"]),
        }