from pynamodb.attributes import MapAttribute, NumberAttribute
from src.models.base_model import BaseModel

# Classe que define o formato dos dados da entidade "Order"
class OrderDataMap(MapAttribute):
    total = NumberAttribute(null=True)  # Valor total do pedido (permitido ser nulo)

# Modelo de pedido que herda da estrutura base
class OrderModel(BaseModel):
    data = OrderDataMap()  # Campo de dados flexível contendo as informações do pedido

    @classmethod
    def build_pk(cls, user_id):
        # Define a chave de partição no formato: USER#<id>
        return f"USER#{user_id}"

    @classmethod
    def build_sk(cls, order_id):
        # Define a chave de ordenação no formato: ORDER#<id>
        return f"ORDER#{order_id}"
