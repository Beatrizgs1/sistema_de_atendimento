import os
import logging
import arquivos
from cliente import Cliente
from atendente import Atendente
from repositorio import Repositorio
from sistema import Sistema

logging.basicConfig(
    filename="sistema.log",
    level=logging.INFO,
    format="%(asctime)s %(message)s",
)

def limpar():
    os.system("cls" if os.name == "nt" else "clear")


def pausar():
    input("\n[Enter para continuar]")

def ler_texto(msg):
    while True:
        val = input(msg).strip()
        if val:
            return val
        print("campo nao pode ser vazio!")


def ler_int(msg, minimo=1):
    while True:
        try:
            val = int(input(msg))
            if val < minimo:
                print(f"valor minimo e {minimo}")
                continue
            return val
        except ValueError:
            print("digite um numero inteiro")

def cadastrar_cliente(sistema):
    print("\n-- Cadastrar Cliente --")
    id_c = ler_texto("id: ")
    nome = ler_texto("nome: ")
    tel = ler_texto("telefone: ")
    prior = input("prioritario? s/n: ").strip().lower() == "s"

    try:
        c = Cliente(id_c, nome, tel, prior)
        sistema.repositorio.cadastrar_cliente(c)
        print("cliente cadastrado com sucesso")
        logging.info("cadastrou cliente %s", id_c)
    except ValueError as e:
        print(f"erro: {e}")


def listar_clientes(sistema):
    print("\n-- Lista de Clientes --")
    clientes = sistema.repositorio.listar_clientes()
    if not clientes:
        print("nenhum cliente cadastrado")
        return
    for c in clientes:
        print(f"  {c}")


def buscar_cliente(sistema):
    print("\n-- Buscar Cliente --")
    print("1 - por id (busca binaria O(log n))")
    print("2 - por nome (busca linear O(n))")
    op = input("opcao: ").strip()

    if op == "1":
        id_c = ler_texto("id: ")
        c = sistema.repositorio.buscar_cliente_por_id(id_c)
        if c:
            print(f"  {c}")
        else:
            print("cliente nao encontrado")
    elif op == "2":
        termo = ler_texto("nome: ")
        resultado = sistema.repositorio.buscar_cliente_por_nome(termo)
        if resultado:
            for c in resultado:
                print(f"  {c}")
        else:
            print("nenhum cliente encontrado")
    else:
        print("opcao invalida")


def remover_inativo(sistema):
    print("\n-- Remover Cliente Inativo --")
    id_c = ler_texto("id do cliente: ")
    try:
        c = sistema.remover_cliente_inativo(id_c)
        print(f"cliente {c.nome} removido")
        logging.info("removeu cliente %s", id_c)
    except (KeyError, ValueError) as e:
        print(f"erro: {e}")




def cadastrar_atendente(sistema):
    print("\n-- Cadastrar Atendente --")
    id_a = ler_texto("id: ")
    nome = ler_texto("nome: ")

    try:
        a = Atendente(id_a, nome)
        sistema.repositorio.cadastrar_atendente(a)
        print("atendente cadastrado")
        logging.info("cadastrou atendente %s", id_a)
    except ValueError as e:
        print(f"erro: {e}")


def listar_atendentes(sistema):
    print("\n-- Atendentes --")
    atendentes = sistema.repositorio.listar_atendentes()
    if not atendentes:
        print("nenhum atendente cadastrado")
        return
    for a in atendentes:
        print(f"  {a}")

def abrir_atendimento(sistema):
    print("\n-- Adicionar Cliente na Fila --")
    id_c = ler_texto("id do cliente: ")
    try:
        c = sistema.abrir_atendimento(id_c)
        tipo = "PRIORITARIO" if c.prioridade else "normal"
        print(f"{c.nome} entrou na fila ({tipo})")
        logging.info("cliente %s entrou na fila", id_c)
    except (KeyError, ValueError) as e:
        print(f"erro: {e}")


def chamar_proximo(sistema):
    print("\n-- Chamar Proximo --")
    id_a = ler_texto("id do atendente: ")
    try:
        atendimento, cliente, atendente = sistema.chamar_proximo(id_a)
        print(f"{atendente.nome} vai atender {cliente.nome}")
        print(f"id do atendimento: {atendimento.id_atendimento}")
        logging.info("atendimento %s iniciado", atendimento.id_atendimento)
    except (KeyError, ValueError) as e:
        print(f"erro: {e}")


def finalizar(sistema):
    print("\n-- Finalizar Atendimento --")
    id_at = ler_texto("id do atendimento: ")
    try:
        at = sistema.finalizar_atendimento(id_at)
        print(f"atendimento {id_at} finalizado")
        print(f"duracao: {at.duracao_minutos} minutos")
        logging.info("atendimento %s finalizado", id_at)
    except (KeyError, ValueError) as e:
        print(f"erro: {e}")

def desfazer(sistema):
    print("\n-- Desfazer Ultima Finalizacao --")
    try:
        at = sistema.desfazer_ultimo()
        print(f"atendimento {at.id_atendimento} reaberto")
        logging.info("desfez finalizacao %s", at.id_atendimento)
    except IndexError as e:
        print(f"erro: {e}")

def ver_fila(sistema):
    print("\n-- Fila de Espera --")
    fila = sistema.listar_fila()
    if not fila:
        print("fila vazia")
        return
    for i, c in enumerate(fila, 1):
        tipo = "PRIORITARIO" if c.prioridade else "normal"
        print(f"  {i}. {c.nome} - {tipo}")


def ver_andamento(sistema):
    print("\n-- Atendimentos em Andamento --")
    lista = sistema.listar_em_andamento()
    if not lista:
        print("nenhum atendimento em andamento")
        return
    for a in lista:
        print(f"  {a}")

def relatorios(sistema):
    while True:
        limpar()
        print("\n-- Relatorios --")
        print("1 - historico por cliente")
        print("2 - tempo medio de atendimento")
        print("3 - top 5 clientes mais atendidos")
        print("4 - exportar CSV")
        print("0 - voltar")

        op = input("\nopcao: ").strip()
        limpar()

        if op == "1":
            id_c = ler_texto("id do cliente: ")
            hist = sistema.historico_cliente(id_c)
            print(f"\n-- Historico do cliente {id_c} --")
            if not hist:
                print("nenhum atendimento encontrado")
            for a in hist:
                print(f"  {a}")

        elif op == "2":
            media = sistema.tempo_medio()
            print(f"\ntempo medio: {media} minutos")

        elif op == "3":
            top = sistema.top5_clientes()
            print("\n-- Top 5 --")
            if not top:
                print("sem dados ainda")
            for i, (id_c, qtd) in enumerate(top, 1):
                c = sistema.repositorio.buscar_cliente_por_id(id_c)
                nome = c.nome if c else id_c
                print(f"  {i}. {nome} - {qtd}x atendido(s)")

        elif op == "4":
            arquivos.exportar_csv(sistema.listar_historico())

        elif op == "0":
            break
        else:
            print("opcao invalida")

        pausar()

def menu():
    print("\n" + "=" * 45)
    print("   SISTEMA DE ATENDIMENTO")
    print("=" * 45)
    print(" [1] cadastrar cliente")
    print(" [2] listar clientes")
    print(" [3] buscar cliente")
    print(" [4] remover cliente inativo")
    print(" [5] cadastrar atendente")
    print(" [6] listar atendentes")
    print(" [7] adicionar cliente na fila")
    print(" [8] chamar proximo")
    print(" [9] finalizar atendimento")
    print(" [10] desfazer ultima finalizacao")
    print(" [11] ver fila")
    print(" [12] ver atendimentos em andamento")
    print(" [13] relatorios")
    print(" [0] sair")
    print("=" * 45)

def main():
    repo = Repositorio()
    sistema = Sistema(repo)

    try:
        clientes, atendentes, historico = arquivos.carregar_tudo()
        repo.carregar_clientes(clientes)
        repo.carregar_atendentes(atendentes)
        sistema.historico = historico
        if historico:
            sistema._contador_id = max(int(a.id_atendimento) for a in historico) + 1
        print(f"{len(clientes)} cliente(s) e {len(atendentes)} atendente(s) carregados")
    except Exception as e:
        print(f"aviso ao carregar dados: {e}")

    while True:
        limpar()
        menu()
        print(f" fila: {sistema.fila.tamanho()} | em andamento: {len(sistema.em_andamento)}")

        op = input("\n opcao: ").strip()
        limpar()

        acoes = {
            "1": cadastrar_cliente,
            "2": listar_clientes,
            "3": buscar_cliente,
            "4": remover_inativo,
            "5": cadastrar_atendente,
            "6": listar_atendentes,
            "7": abrir_atendimento,
            "8": chamar_proximo,
            "9": finalizar,
            "10": desfazer,
            "11": ver_fila,
            "12": ver_andamento,
        }

        if op in acoes:
            acoes[op](sistema)
        elif op == "13":
            relatorios(sistema)
        elif op == "0":
            print("salvando dados...")
            arquivos.salvar_tudo(repo, sistema.listar_historico())
            print("ate logo!")
            logging.info("sistema encerrado")
            break
        else:
            print("opcao invalida")

        if op in {"1", "4", "5", "7", "8", "9", "10"}:
            arquivos.salvar_tudo(repo, sistema.listar_historico())

        pausar()

if __name__ == "__main__":
    main()