# Importa o decorador principal da biblioteca `moto`
# `moto` permite simular serviços da AWS (como DynamoDB, S3, etc.) localmente para testes.
# Aqui usamos o decorador `mock_aws`, que configura automaticamente todos os serviços suportados pelo `moto`.
from moto import mock_aws

# Criamos um contexto de execução com o serviço da AWS "mockado".
# Isso significa que qualquer chamada feita para AWS (por exemplo, criar tabela no DynamoDB)
# será redirecionada para uma instância simulada na memória, sem afetar sua conta real na AWS.
with mock_aws():
    # Importa a função `run` da aplicação principal.
    # Esta importação precisa ocorrer DENTRO do `with mock_aws()` para que a criação da tabela
    # seja interceptada corretamente pelo `moto`.
    from src import app

    # Executa a função principal que:
    # - Cria a tabela DynamoDB (caso não exista)
    # - Insere um usuário e dois pedidos
    # - Consulta os dados do usuário e seus pedidos
    result = app.run()

    # Imprime o resultado da função, que é um dicionário contendo:
    # - Dados do usuário (nome, email)
    # - Lista de pedidos associados a ele
    print(result)
