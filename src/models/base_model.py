from pynamodb.attributes import UnicodeAttribute
from pynamodb.models import Model

# Classe base abstrata para todos os modelos do projeto
# Define a estrutura de chaves e configurações da tabela DynamoDB

class BaseModel(Model):
    # Metadados da tabela DynamoDB (nome e região)
    class Meta:
        table_name = "AppData"     # Nome da tabela compartilhada por todas as entidades
        region = "us-east-1"       # Região AWS onde está localizada a tabela

    # Chave de partição (Partition Key) - utilizada para agrupar registros
    PK = UnicodeAttribute(hash_key=True)

    # Chave de ordenação (Sort Key) - usada para diferenciar os registros dentro da mesma partição
    SK = UnicodeAttribute(range_key=True)
