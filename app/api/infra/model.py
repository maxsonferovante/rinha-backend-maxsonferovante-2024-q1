from datetime import datetime
from enum import Enum

from pydantic import BaseModel, Field, model_serializer


class TransactionType(str, Enum):
    credit = "c"
    debit = "d"


class Transaction(BaseModel):
    amount: int = Field(alias="valor", gt=0)
    type: TransactionType = Field(alias="tipo")
    description: str = Field(alias="descricao")
    created_at: datetime = Field(alias="realizado_em", default_factory=datetime.utcnow)

class Client(BaseModel):
    id: int = Field(alias="cliente_id", gt=0)
    accont_limit: int = Field(alias="limite", ge=0)
    accont_balance: int = Field(alias="saldo", ge=0)
    transactions: list[Transaction] = Field(alias="ultimas_transacoes", default=[])
       
    @model_serializer
    def serialize_model(self):
        return {
            "saldo": {
                "total": self.account_balance,
                "data_extrato": datetime.utcnow().isoformat(),
                "limite": abs(self.account_limit),
            },
            "ultimas_transacoes": [
                {
                    "valor": t.amount,
                    "tipo": t.type.value,
                    "descricao": t.description,
                    "realizada_em": t.created_at,
                }
                for t in self.transactions
            ],
        }
    
class Error (BaseModel):
    code: int
    message: str