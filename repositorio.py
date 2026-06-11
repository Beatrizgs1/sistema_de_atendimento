from cliente import Cliente
from atendente import Atendente


class Repositorio:
    def __init__(self):
        self.clientes_nao_ordenado = []   
        self.clientes_ordenado = []       
     
        self.atendentes = []
    def buscar_cliente_por_id(self, id_cliente):
        esquerda = 0
        direita = len(self.clientes_ordenado) - 1

        while esquerda <= direita:
            meio = (esquerda + direita) // 2
            id_meio = self.clientes_ordenado[meio].id_cliente

            if id_meio == id_cliente:
                return self.clientes_ordenado[meio]
            elif id_meio < id_cliente:
                esquerda = meio + 1
            else:
                direita = meio - 1

        return None

    def buscar_cliente_por_nome(self, termo):
        termo = termo.lower()
        return [c for c in self.clientes_nao_ordenado if termo in c.nome.lower()]

    def _inserir_ordenado(self, cliente):
        posicao = 0
        for i in range(len(self.clientes_ordenado)):
            if self.clientes_ordenado[i].id_cliente < cliente.id_cliente:
                posicao = i + 1
            else:
                break
        self.clientes_ordenado.insert(posicao, cliente)

    def cadastrar_cliente(self, cliente):
        if self.buscar_cliente_por_id(cliente.id_cliente) is not None:
            raise ValueError(f"Ja existe cliente com um id '{cliente.id_cliente}'.")
        self.clientes_nao_ordenado.append(cliente)
        self._inserir_ordenado(cliente)

    def remover_cliente(self, id_cliente):
        cliente = self.buscar_cliente_por_id(id_cliente)
        if cliente is None:
            raise KeyError(f"Cliente '{id_cliente}' nao encontrado.")
        self.clientes_nao_ordenado.remove(cliente)
        self.clientes_ordenado.remove(cliente)
        return cliente

    def listar_clientes(self):
        return list(self.clientes_ordenado)

    def cadastrar_atendente(self, atendente):
        for a in self.atendentes:
            if a.id_atendente == atendente.id_atendente:
                raise ValueError(f"Ja existe um  atendente com id '{atendente.id_atendente}'.")
        self.atendentes.append(atendente)

    def buscar_atendente(self, id_atendente):
        for a in self.atendentes:
            if a.id_atendente == id_atendente:
                return a
        return None

    def atendente_livre(self):
        for a in self.atendentes:
            if not a.ocupado:
                return a
        return None

    def listar_atendentes(self):
        return list(self.atendentes)

    def carregar_clientes(self, lista):
        self.clientes_nao_ordenado = []
        self.clientes_ordenado = []
        for c in lista:
            self.cadastrar_cliente(c)

    def carregar_atendentes(self, lista):
        self.atendentes = []
        for a in lista:
            self.atendentes.append(a)
