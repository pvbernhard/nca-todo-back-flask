from flask import Flask, request, jsonify, abort
from database import SessionLocal, engine
import models
from models import Todo

app = Flask(__name__)

# cria as tabelas no banco de dados caso ainda não existam
models.Base.metadata.create_all(bind=engine)


# sessão do banco de dados
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.route('/get_all', methods=['GET'])
def get_all_todos():
    db = next(get_db())
    todos = db.query(Todo).all()
    todos_list = [
        {"id": todo.id, "title": todo.title, "complete": todo.complete}
        for todo in todos
    ]
    return jsonify(todos_list), 200


@app.route('/add', methods=['POST'])
def add_todo():
    db = next(get_db())
    data = request.get_json()

    if not data or 'title' not in data:
        abort(400, description="O campo 'title' é obrigatório")

    title = data['title']
    complete = data.get('complete', False)  # padrão = False

    if not isinstance(title, str) or not title.strip():
        abort(400, description="O campo 'title' deve ser uma string não vazia")

    if not isinstance(complete, bool):
        abort(400, description="O campo 'complete' deve ser um valor booleano")

    new_todo = Todo(title=title.strip(), complete=complete)

    db.add(new_todo)
    db.commit()
    db.refresh(new_todo)

    return jsonify({
        "id": new_todo.id,
        "title": new_todo.title,
        "complete": new_todo.complete
    }), 201  # criado com sucesso


@app.route('/update/<int:todo_id>', methods=['PUT'])
def update_todo(todo_id):
    db = next(get_db())
    todo = db.query(Todo).filter(Todo.id == todo_id).first()

    if not todo:
        abort(404, description=f"Tarefa com id {todo_id} não encontrada")

    data = request.get_json()

    if 'title' in data:
        todo.title = data['title']
    if 'complete' in data:
        if isinstance(data['complete'], bool):
            todo.complete = data['complete']
        else:
            abort(400, description="'complete' deve ser um valor booleano")

    db.commit()

    return jsonify({
        "id": todo.id,
        "title": todo.title,
        "complete": todo.complete
    }), 200


@app.route('/delete/<int:todo_id>', methods=['DELETE'])
def delete_todo(todo_id):
    db = next(get_db())
    todo = db.query(Todo).filter(Todo.id == todo_id).first()

    if not todo:
        abort(404, description=f"Tarefa com id {todo_id} não encontrada")

    db.delete(todo)
    db.commit()

    return jsonify({"message": f"Tarefa com id {todo_id} deletada com sucesso"}), 200


if __name__ == '__main__':
    app.run(debug=True)
