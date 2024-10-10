Esta aplicação é uma API simples desenvolvida em **Flask** que gerencia uma lista de tarefas (To-Do list). Utilizando o banco de dados SQLite e a biblioteca **SQLAlchemy** para manipulação de dados, a API permite realizar as operações básicas de **CRUD** (Criar, Ler, Atualizar e Deletar) em itens de uma tabela chamada "Todos".

### Funcionalidades principais:
- **`/`** `GET`: Retorna uma lista de todos os itens "Todo" armazenados no banco de dados.
- **`/`** `POST`: Adiciona um novo item "Todo" com um título e um status de conclusão (`completed`), que por padrão é falso.
- **`/:id`** `PUT`: Atualiza o título ou status de conclusão de um item específico pelo seu ID.
- **`/:id`** `DELETE`: Remove um item "Todo" específico pelo seu ID.

### Objeto JSON fornecido para as rotas de adicionar e atualizar:

Ao criar ou atualizar um item "Todo", você envia o seguinte objeto no corpo da requisição:

```json
{
    "text": "Comprar leite",
    "completed": false
}
```

- **`text`** (obrigatório para `GET /`): String contendo o título da tarefa.
- **`completed`** (opcional): Booleano que indica se a tarefa está concluída ou não. O valor padrão é `false` caso não seja fornecido.

A aplicação é um exemplo básico de gerenciamento de tarefas, implementada de forma simples para manipulação de dados via API.