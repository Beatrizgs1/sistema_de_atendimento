from cliente import Cliente
from atendente import Atendente
from atendimento import Atendimento
from estruturas import FilaPrioridade, Pilha, ListaEncadeada
from repositorio import Repositorio
from sistema import Sistema


def testar(descricao, condicao):
    status = "OK" if condicao else "FALHOU"
    print(f"  [{status}] {descricao}")
    return condicao

def testes_cliente():
    print("\n--- Cliente ---")
    c = Cliente("001", "Ana", "99999-0000", True)
    testar("Cria cliente com dados validos", c.nome == "Ana")
    testar("Prioridade True", c.prioridade == True)
    testar("to_dict funciona", c.to_dict()["id_cliente"] == "001")
    testar("from_dict funciona", Cliente.from_dict(c.to_dict()).nome == "Ana")

    try:
        Cliente("", "Ana", "999", False)
        testar("Rejeita ID vazio", False)
    except ValueError:
        testar("Rejeita ID vazio", True)

    try:
        Cliente("001", "", "999", False)
        testar("Rejeita nome vazio", False)
    except ValueError:
        testar("Rejeita nome vazio", True)


def testes_estruturas():
    print("\n--- Pilha ---")
    p = Pilha()
    testar("Pilha vazia", p.vazia())
    p.push("a")
    p.push("b")
    testar("Push e pop", p.pop() == "b")
    testar("Topo correto", p.topo() == "a")

    try:
        Pilha().pop()
        testar("Pop em pilha vazia lanca erro", False)
    except IndexError:
        testar("Pop em pilha vazia lanca erro", True)

    print("\n--- Fila de Prioridade ---")
    fila = FilaPrioridade()
    c1 = Cliente("001", "Normal", "111", False)
    c2 = Cliente("002", "Prioritario", "222", True)
    fila.enqueue(c1)
    fila.enqueue(c2)
    testar("Prioritario sai primeiro", fila.dequeue().id_cliente == "002")
    testar("Normal sai depois", fila.dequeue().id_cliente == "001")
    testar("Fila vazia apos dequeue", fila.vazia())

    print("\n--- Lista Encadeada ---")
    lista = ListaEncadeada()
    lista.inserir(Cliente("001", "Ana", "111", False))
    lista.inserir(Cliente("002", "Bia", "222", False))
    testar("Tamanho correto", len(lista) == 2)
    testar("Busca por id", lista.buscar("001").nome == "Ana")
    lista.remover("001")
    testar("Remove por id", lista.buscar("001") is None)
    testar("Tamanho apos remocao", len(lista) == 1)


def testes_repositorio():
    print("\n--- Repositorio ---")
    repo = Repositorio()
    c1 = Cliente("003", "Julia", "333", False)
    c2 = Cliente("001", "Ana", "111", False)
    c3 = Cliente("002", "Bia", "222", True)
    repo.cadastrar_cliente(c1)
    repo.cadastrar_cliente(c2)
    repo.cadastrar_cliente(c3)

    codigos = [c.id_cliente for c in repo.listar_clientes()]
    testar("Vetor ordenado por id", codigos == sorted(codigos))
    testar("Busca binaria por id", repo.buscar_cliente_por_id("002").nome == "Bia")
    testar("Busca inexistente retorna None", repo.buscar_cliente_por_id("999") is None)
    testar("Busca linear por nome", len(repo.buscar_cliente_por_nome("an")) == 1)

    try:
        repo.cadastrar_cliente(Cliente("001", "Dup", "000", False))
        testar("Rejeita id duplicado", False)
    except ValueError:
        testar("Rejeita id duplicado", True)

    repo.remover_cliente("001")
    testar("Remove cliente", repo.buscar_cliente_por_id("001") is None)


def testes_sistema():
    print("\n--- Sistema ---")
    repo = Repositorio()
    sistema = Sistema(repo)

    repo.cadastrar_cliente(Cliente("001", "Ana", "111", False))
    repo.cadastrar_cliente(Cliente("002", "Bia", "222", True))
    repo.cadastrar_atendente(Atendente("A01", "Joao"))

    sistema.abrir_atendimento("001")
    sistema.abrir_atendimento("002")

    fila = sistema.listar_fila()
    testar("Prioritario na frente da fila", fila[0].id_cliente == "002")

    atendimento, cliente, atendente = sistema.chamar_proximo("A01")
    testar("Chama prioritario primeiro", cliente.id_cliente == "002")
    testar("Atendente fica ocupado", atendente.ocupado)

    sistema.finalizar_atendimento(atendimento.id_atendimento)
    testar("Historico tem 1 registro", len(sistema.historico) == 1)
    testar("Atendente fica livre", atendente.ocupado == False)

    sistema.desfazer_ultimo()
    testar("Desfazer move de volta para em andamento", len(sistema.em_andamento) == 1)
    testar("Historico vazio apos desfazer", len(sistema.historico) == 0)

    try:
        sistema.remover_cliente_inativo("002")
        testar("Nao remove com atendimento aberto", False)
    except ValueError:
        testar("Nao remove com atendimento aberto", True)

    print("\n--- Recursao (tempo medio) ---")
    sistema.finalizar_atendimento(atendimento.id_atendimento)
    media = sistema.tempo_medio()
    testar("Tempo medio calculado recursivamente", media >= 0)


if __name__ == "__main__":
    print("=" * 45)
    print("  TESTES UNITARIOS")
    print("=" * 45)

    testes_cliente()
    testes_estruturas()
    testes_repositorio()
    testes_sistema()

    print("\n" + "=" * 45)
    print("  TESTES CONCLUIDOS")
    print("=" * 45)
