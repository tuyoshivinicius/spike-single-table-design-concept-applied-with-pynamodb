from src.models.order_model import OrderModel, OrderDataMap
from src.models.user_model import UserModel, UserDataMap

# Função responsável por inserir dados de exemplo na tabela DynamoDB
def insert_sample_data():
    # Cria um usuário com ID "001" e salva na tabela com chave PK/SK específica
    UserModel(
        PK=UserModel.build_pk("001"),              # PK: USER#001
        SK=UserModel.build_sk(),                   # SK: PROFILE
        data=UserDataMap(name="Ana", email="ana@example.com")  # Dados do usuário encapsulados em MapAttribute
    ).save()

    # Cria um pedido para o usuário "001" com ID do pedido "A1001"
    OrderModel(
        PK=OrderModel.build_pk("001"),             # PK: USER#001 (relacionado ao mesmo usuário)
        SK=OrderModel.build_sk("A1001"),           # SK: ORDER#A1001
        data=OrderDataMap(total=99.99)             # Valor do pedido encapsulado
    ).save()

    # Cria um segundo pedido para o mesmo usuário
    OrderModel(
        PK=OrderModel.build_pk("001"),
        SK=OrderModel.build_sk("A1002"),           # SK: ORDER#A1002
        data=OrderDataMap(total=102.2)
    ).save()

# Função principal que inicializa a tabela, insere os dados e realiza uma consulta
def run():
    # Cria a tabela DynamoDB caso ela ainda não exista
    if not UserModel.exists():
        UserModel.create_table(read_capacity_units=1, write_capacity_units=1, wait=True)

    # Popula a tabela com os dados de exemplo definidos acima
    insert_sample_data()

    # Define o ID do usuário que será consultado
    user_id = "001"

    # Consulta o registro do perfil do usuário com PK = USER#001 e SK = PROFILE
    user_iterator = UserModel.query(
        hash_key=UserModel.build_pk(user_id),
        range_key_condition=UserModel.SK == UserModel.build_sk()
    )

    # Obtém o primeiro (e único) item retornado pela consulta
    user_model = next(user_iterator, None)
    if not user_model:
        print("User not found")
        return

    # Constrói um dicionário com os dados do usuário
    user_dict = {
        "user_id": user_model.PK.split("#")[1],  # Extrai apenas o ID numérico a partir da PK
        "name": user_model.data.name,
        "email": user_model.data.email
    }

    # Consulta todos os pedidos do usuário com SKs que começam com "ORDER#"
    order_iterator = OrderModel.query(
        hash_key=OrderModel.build_pk(user_id),
        range_key_condition=OrderModel.SK.startswith("ORDER#")  # Filtra pedidos via prefixo
    )

    # Constrói uma lista com os pedidos encontrados
    order_dicts = []
    for order in order_iterator:
        order_dicts.append({
            "order_id": order.SK.split("#")[1],  # Extrai o ID do pedido da SK
            "total": order.data.total            # Valor total do pedido
        })

    # Adiciona os pedidos ao dicionário do usuário
    user_dict["orders"] = order_dicts

    # Retorna a estrutura completa do usuário com seus pedidos
    return user_dict
