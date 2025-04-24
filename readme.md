
# Spike Single Table Design com PynamoDB

## Visão Geral

Este projeto é uma **spike técnica com fins didáticos**. Seu objetivo é explorar, de maneira prática e clara, a implementação de uma tabela no AWS DynamoDB usando o padrão **Single Table Design (STD)** através da biblioteca **PynamoDB** em Python.

O projeto visa auxiliar desenvolvedores na compreensão e implementação desse padrão, mostrando como utilizar modelos claros e organizados com a PynamoDB.

---

## O que é Single Table Design?

O **Single Table Design** é um padrão recomendado pela AWS para estruturar tabelas no DynamoDB, utilizando apenas uma tabela para armazenar diferentes tipos de entidades relacionadas. Ao invés de utilizar múltiplas tabelas, os dados são agrupados numa única tabela, diferenciando as entidades através de chaves de partição (`Partition Key`) e chaves de ordenação (`Sort Key`).

### Benefícios do Single Table Design:

- Redução de custos operacionais.
- Melhor performance nas consultas.
- Facilita a escalabilidade.

Exemplo simplificado:

| PK            | SK           | Dados                               |
|---------------|--------------|-------------------------------------|
| USER#123      | PROFILE      | { "nome": "João", "email": "joao@example.com" } |
| USER#123      | ORDER#987    | { "total": 50.00 }                 |

---

## Por que usar PynamoDB?

**PynamoDB** é uma biblioteca Python que oferece uma interface fácil e intuitiva para interagir com o DynamoDB, similar a um ORM (Object-Relational Mapper). Ela abstrai detalhes complexos do gerenciamento de tabelas e entidades, facilitando o desenvolvimento de aplicações claras e robustas.

Principais vantagens:

- Simplicidade na definição de modelos.
- Abstração da complexidade dos tipos e índices DynamoDB.
- Facilidade na escrita e leitura de consultas complexas.

---

## Estrutura da Tabela

A tabela utilizada neste projeto segue o padrão STD com os seguintes elementos principais:

- `PK` (Partition Key): Identifica a entidade principal (ex: USER#id).
- `SK` (Sort Key): Diferencia dados adicionais associados à entidade (ex: ORDER#id, PROFILE).
- Atributo `data`: Armazena detalhes específicos em formato estruturado.

### Exemplos de Modelagem:

### BaseModel

```python
class BaseModel(Model):
    class Meta:
        table_name = "AppData"
        region = "us-east-1"

    PK = UnicodeAttribute(hash_key=True)
    SK = UnicodeAttribute(range_key=True)
```

### UserModel

```python
class UserDataMap(MapAttribute):
    name = UnicodeAttribute(null=True)
    email = UnicodeAttribute(null=True)

class UserModel(BaseModel):
    data = UserDataMap()

    @classmethod
    def build_pk(cls, user_id):
        return f"USER#{user_id}"

    @classmethod
    def build_sk(cls):
        return "PROFILE"
```

### OrderModel

```python
class OrderDataMap(MapAttribute):
    total = NumberAttribute(null=True)

class OrderModel(BaseModel):
    data = OrderDataMap()

    @classmethod
    def build_pk(cls, user_id):
        return f"USER#{user_id}"

    @classmethod
    def build_sk(cls, order_id):
        return f"ORDER#{order_id}"
```

---

## Exemplos de Código

O projeto inclui exemplos claros e comentados:

- Criação e consulta de usuários.
- Inserção e consulta de pedidos.

Exemplo didático de inserção:

```python
UserModel(
    PK=UserModel.build_pk("001"),              
    SK=UserModel.build_sk(),                   
    data=UserDataMap(name="Ana", email="ana@example.com") 
).save()


OrderModel(
    PK=OrderModel.build_pk("001"), 
    SK=OrderModel.build_sk("A1001"),
    data=OrderDataMap(total=99.99) 
).save()
```

Consulta usando PynamoDB:

```python
user_iterator = UserModel.query(
    hash_key=UserModel.build_pk(user_id),
    range_key_condition=UserModel.SK == UserModel.build_sk()
)

order_iterator = OrderModel.query(
    hash_key=OrderModel.build_pk(user_id),
    range_key_condition=OrderModel.SK.startswith("ORDER#")  # Filtra pedidos via prefixo
)
```
Esses exemplos ajudam a visualizar claramente o funcionamento do padrão STD com PynamoDB.

---

## Estrutura de Arquivos

```
├── run.py                     # Script principal de execução
├── requirements.txt           # Dependências do projeto
└── src/
    ├── app.py                 # Lógica principal (execução e simulação)
    └── models/
        ├── base_model.py      # Modelo base compartilhado
        ├── user_model.py      # Modelo de usuário
        └── order_model.py     # Modelo de pedido
```
---

## Como Executar o Projeto Localmente

### Pré-requisitos

- Python 3.11+

### Dependências

Instale as dependências usando:

```bash
pip install -r requirements.txt
```
### Execução
Rode o projeto:

```bash
python run.py
```

### Saída Esperada

Ao executar o script `run.py`, você verá a seguinte saída (simulada via `moto`, sem conexão real com a AWS):

```json
{
  "user_id": "001",
  "name": "Ana",
  "email": "ana@example.com",
  "orders": [
    {
      "order_id": "A1001",
      "total": 99.99
    },
    {
      "order_id": "A1002",
      "total": 102.2
    }
  ]
}
```

Essa saída demonstra o funcionamento completo do padrão **Single Table Design**, mostrando como diferentes tipos de itens (usuários e pedidos) podem coexistir e ser consultados eficientemente em uma única tabela do DynamoDB.

---

## Pontos de Atenção e Boas Práticas

- **Padronização das chaves:** Utilize nomenclaturas consistentes e claras para `Partition Key` e `Sort Key`.
- **Modelos estruturados:** Utilize modelos base para abstrair configurações comuns e simplificar manutenção.
- **Validação de atributos:** Sempre valide atributos obrigatórios e opcionais explicitamente nos seus modelos.
- **Performance nas consultas:** Evite consultas que possam gerar varreduras completas da tabela (table scans).
- **Gerenciamento de dependências:** Sempre mantenha as versões das bibliotecas (como `boto3`, `pynamodb`) atualizadas.
- **Testes e simulações:** Utilize ferramentas como o Moto para simular o DynamoDB localmente antes do deploy na AWS.
---

## Recursos Adicionais

- [AWS DynamoDB Best Practices](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/best-practices.html)
- [Documentação oficial PynamoDB](https://pynamodb.readthedocs.io/en/latest/)
- [Single Table Design - Alex DeBrie](https://www.alexdebrie.com/posts/dynamodb-single-table/)

---
