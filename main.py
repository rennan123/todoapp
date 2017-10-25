from flask import Flask, jsonify, request
from modelo import (criar_tarefa, memdb, listar_tarefas, remover_tarefa,
                    recuperar_tarefa, Tarefa, editar_tarefa)

app = Flask('Meu app')


@app.route('/task', methods=['POST'])
def criar():
    memdb.clear()
    # recebe o título e a descrição através do corpo da requisição
    titulo = request.form['titulo']
    descricao = request.form['descricao']
    # utiliza estes valores para criar uma tarefa
    # a função criar tarefa foi desenvolvida e testada no passo anterior
    tarefa = criar_tarefa(titulo, descricao)
    # retorna o resultado em um formato json
    return jsonify({
        'id': tarefa.id,
        'titulo': tarefa.titulo,
        'descricao': tarefa.descricao,
        'status': tarefa.status,
    }), 201


@app.route('/task', methods=['GET'])
def listar():
    tarefas = []
    for tarefa in listar_tarefas():
        tarefas.append({
            'id': tarefa.id,
            'titulo': tarefa.titulo,
            'status': tarefa.status,
        })
    return jsonify(tarefas)


@app.route('/task/<int:id_tarefa>', methods=['DELETE'])
def remover(id_tarefa):
    try:
        remover_tarefa(id_tarefa)
        return '', 204
    except KeyError:
        return jsonify({'error': 'task not found'}), 404


@app.route('/task/<int:id_tarefa>', methods=['GET'])
def detalhar(id_tarefa):
    try:
        tarefa = recuperar_tarefa(id_tarefa)
        return jsonify({
            'id': tarefa.id,
            'titulo': tarefa.titulo,
            'descricao': tarefa.descricao,
            'status': tarefa.status,
        })
    except KeyError:
        return jsonify({'error': 'task not found'}), 404


@app.route('/task/<int:id_tarefa>', methods=['PATCH', 'PUT'])
def editar(id_tarefa):
    try:
        t = Tarefa(request.form['titulo'],
                   request.form['descricao'],
                   request.form['status'])
        tarefa = editar_tarefa(id_tarefa, t)
        return jsonify({
            'id': tarefa.id,
            'titulo': tarefa.titulo,
            'descricao': tarefa.descricao,
            'status': tarefa.status,
        })
    except KeyError:
        return jsonify({'error': 'task not found'}), 404