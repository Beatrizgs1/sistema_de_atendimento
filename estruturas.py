class No:
    def __init__(self, valor):
        self.valor = valor
        self.proximo = None

class ListaEncadeada:
    def __init__(self):
        self.cabeca = None
        self.tamanho = 0

    def inserir(self, valor):
        no = No(valor)
        no.proximo = self.cabeca
        self.cabeca = no
        self.tamanho += 1

    def remover(self, id_cliente):
        atual = self.cabeca
        anterior = None

        while atual:
            if atual.valor.id_cliente == id_cliente:
                if anterior:
                    anterior.proximo = atual.proximo
                else:
                    self.cabeca = atual.proximo
                self.tamanho -= 1
                return atual.valor
            anterior = atual
            atual = atual.proximo

        return None  

    def buscar(self, id_cliente):
        atual = self.cabeca
        while atual:
            if atual.valor.id_cliente == id_cliente:
                return atual.valor
            atual = atual.proximo
        return None

    def para_lista(self):
        resultado = []
        atual = self.cabeca
        while atual:
            resultado.append(atual.valor)
            atual = atual.proximo
        return resultado

    def __len__(self):
        return self.tamanho

class Pilha:

    def __init__(self):
        self._dados = []

    def push(self, item):
        self._dados.append(item)

    def pop(self):
        if self.vazia():
            raise IndexError("Pilha vazia. Nao tem acao para desfazer...")
        return self._dados.pop()

    def topo(self):
        if self.vazia():
            return None
        return self._dados[-1]

    def vazia(self):
        return len(self._dados) == 0

    def __len__(self):
        return len(self._dados)

class FilaPrioridade:
    def __init__(self):
        self.fila_prioritaria = []
        self.fila_normal = []

    def enqueue(self, cliente):
        if cliente.prioridade:
            self.fila_prioritaria.append(cliente)
        else:
            self.fila_normal.append(cliente)

    def dequeue(self):
        if self.fila_prioritaria:
            return self.fila_prioritaria.pop(0)
        if self.fila_normal:
            return self.fila_normal.pop(0)
        return None

    def vazia(self):
        return len(self.fila_prioritaria) == 0 and len(self.fila_normal) == 0

    def tamanho(self):
        return len(self.fila_prioritaria) + len(self.fila_normal)

    def para_lista(self):
        return list(self.fila_prioritaria) + list(self.fila_normal)
