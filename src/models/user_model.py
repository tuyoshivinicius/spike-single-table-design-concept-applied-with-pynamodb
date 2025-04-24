from pynamodb.attributes import MapAttribute, UnicodeAttribute
from src.models.base_model import BaseModel

# Classe que define o formato dos dados da entidade "User"
class UserDataMap(MapAttribute):
    name = UnicodeAttribute(null=True)   # Nome do usuário
    email = UnicodeAttribute(null=True)  # E-mail do usuário

# Modelo de usuário que herda da estrutura base
class UserModel(BaseModel):
    data = UserDataMap()  # Campo que contém os dados do perfil do usuário

    @classmethod
    def build_pk(cls, user_id):
        # Define a chave de partição no formato: USER#<id>
        return f"USER#{user_id}"

    @classmethod
    def build_sk(cls):
        # Define a chave de ordenação fixa para perfis: PROFILE
        return "PROFILE"
