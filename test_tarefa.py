import json
from main import app
from modelo import memdb, Tarefa


def test_criar_tarefa():
    with app.test_client() as c:
        # realiza a requisição utilizando o verbo POST
        resp = c.post('/task', data={'titulo': 'titulo',
                                     'descricao': 'descricao'})
        # é realizada a análise e transformação para objeto python da resposta
        data = json.loads(resp.data.decode('utf-8'))
        # 201 CREATED é o status correto aqui
        assert resp.status_code == 201
        assert data['titulo'] == 'titulo'
        assert data['descricao'] == 'descricao'
        # qaundo a comparação é com True, False ou None, utiliza-se o "is"
        assert data['status'] is False


def test_erro_ao_criar_tarefa():
    memdb.clear()
    with app.test_client() as c:
        resp = c.post('/task', data={'titulo': 'titulo'})
        assert resp.status_code == 400


def test_listar_tarefa_sem_conteudo():
    memdb.clear()
    with app.test_client() as c:
        resp = c.get('/task')
        data = json.loads(resp.data.decode('utf-8'))
        assert resp.status_code == 200
        assert data == []


def test_listar_tarefa_com_conteudo():
    memdb.clear()
    tarefa1 = Tarefa('titulo 1', 'descrição')
    memdb[tarefa1.id] = tarefa1
    with app.test_client() as c:
        resp = c.get('/task')
        data = json.loads(resp.data.decode('utf-8'))
        assert resp.status_code == 200
        assert len(data) == 1
        assert 'descricao' not in data[0]


def test_remover_tarefa():
    memdb.clear()
    tarefa1 = Tarefa('titulo 1', 'descrição')
    memdb[tarefa1.id] = tarefa1
    with app.test_client() as c:
        resp = c.delete('/task/{}'.format(tarefa1.id))
        assert resp.data == b''
        assert resp.status_code == 204


def test_erro_ao_remover_tarefa():
    memdb.clear()
    with app.test_client() as c:
        resp = c.delete('/task/42')
        assert resp.status_code == 404


def test_detalhando_tarefa():
    memdb.clear()
    tarefa = Tarefa('titulo', 'descrição')
    memdb[tarefa.id] = tarefa
    with app.test_client() as c:
        resp = c.get('/task/{}'.format(tarefa.id))
        assert resp.status_code == 200
        data = json.loads(resp.data.decode('utf-8'))
        assert data['titulo'] == 'titulo'
        assert data['descricao'] == 'descrição'


def test_erro_ao_detalhar_tarefa():
    memdb.clear()
    with app.test_client() as c:
        resp = c.get('/task/42')
        assert resp.status_code == 404


def test_entregando_tarefas():
    memdb.clear()
    tarefa = Tarefa('titulo', 'descrição')
    memdb[tarefa.id] = tarefa
    with app.test_client() as c:
        resp = c.put('/task/{}'.format(tarefa.id), data={
            'titulo': tarefa.titulo,
            'descricao': tarefa.descricao,
            'status': True})
        data = json.loads(resp.data.decode('utf-8'))
        assert resp.status_code == 200
        assert data['status'] == 'True'