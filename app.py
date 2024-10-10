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


@app.route('/', methods=['GET'])
def get_all_todos():
    db = next(get_db())
    todos = db.query(Todo).all()
    todos_list = [
        {"id": todo.id, "text": todo.text, "completed": todo.completed}
        for todo in todos
    ]
    return jsonify(todos_list), 200


@app.route('/', methods=['POST'])
def add_todo():
    db = next(get_db())
    data = request.get_json()

    if not data or 'text' not in data:
        return jsonify({ "error": "O campo 'text' é obrigatório" }), 400

    text = data['text']
    completed = data.get('completed', False)  # padrão = False

    if not isinstance(text, str) or not text.strip():
        return jsonify({ "error": "O campo 'text' deve ser uma string não vazia" }), 400

    if not isinstance(completed, bool):
        return jsonify({ "error": "O campo 'completed' deve ser um valor booleano" }), 400

    new_todo = Todo(text=text.strip(), completed=completed)

    db.add(new_todo)
    db.commit()
    db.refresh(new_todo)

    return jsonify({
        "id": new_todo.id,
        "text": new_todo.text,
        "completed": new_todo.completed
    }), 201  # criado com sucesso


@app.route('/<int:todo_id>', methods=['PUT'])
def update_todo(todo_id):
    db = next(get_db())
    todo = db.query(Todo).filter(Todo.id == todo_id).first()

    if not todo:
        return jsonify({ "error": f"Tarefa com id {todo_id} não encontrada" }), 404

    data = request.get_json()

    if 'text' in data:
        todo.text = data['text']
    if 'completed' in data:
        if isinstance(data['completed'], bool):
            todo.completed = data['completed']
        else:
            return jsonify({ "error": "'completed' deve ser um valor booleano" }), 400

    db.commit()

    return jsonify({
        "id": todo.id,
        "text": todo.text,
        "completed": todo.completed
    }), 200


@app.route('/<int:todo_id>', methods=['DELETE'])
def delete_todo(todo_id):
    db = next(get_db())
    todo = db.query(Todo).filter(Todo.id == todo_id).first()

    if not todo:
        return jsonify({ "error": f"Tarefa com id {todo_id} não encontrada" }), 404

    db.delete(todo)
    db.commit()

    return jsonify({"message": f"Tarefa com id {todo_id} deletada com sucesso"}), 200


if __name__ == '__main__':
    app.run(debug=True)
