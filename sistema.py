from datetime import datetime
from estruturas import FilaPrioridade, Pilha, ListaEncadeada
from atendimento import Atendimento

class Sistema:
    def __init__(self, repositorio):
        self.repositorio = repositorio
        self.fila = FilaPrioridade()
        self.pilha_desfazer = Pilha()
        self.lista_ativos = ListaEncadeada()
        self.historico = []          
        self.em_andamento = []      
        self._contador_id = 1

    def abrir_atendimento(self, id_cliente):
        cliente = self.repositorio.buscar_cliente_por_id(id_cliente)
        if cliente is None:
            raise KeyError(f"Cliente '{id_cliente}' nao encontrado.")

        for c in self.fila.para_lista():
            if c.id_cliente == id_cliente:
                raise ValueError(f"Cliente '{id_cliente}' ja esta na fila.")

        self.fila.enqueue(cliente)
        return cliente

    def chamar_proximo(self, id_atendente):
        if self.fila.vazia():
            raise ValueError("Fila vazia. Nenhum cliente aguardando.")

        atendente = self.repositorio.buscar_atendente(id_atendente)
        if atendente is None:
            raise KeyError(f"Atendente '{id_atendente}' nao encontrado.")
        if atendente.ocupado:
            raise ValueError(f"Atendente '{atendente.nome}' ja esta ocupado.")

        cliente = self.fila.dequeue()
        atendente.ocupado = True

        atendimento = Atendimento(
            id_atendimento=str(self._contador_id),
            id_cliente=cliente.id_cliente,
            id_atendente=id_atendente,
            inicio=datetime.now().isoformat(),
        )
        self._contador_id += 1
        self.em_andamento.append(atendimento)
        self.lista_ativos.inserir(cliente)

        return atendimento, cliente, atendente

    def finalizar_atendimento(self, id_atendimento):
        atendimento = None
        for a in self.em_andamento:
            if a.id_atendimento == id_atendimento:
                atendimento = a
                break

        if atendimento is None:
            raise KeyError(f"Atendimento '{id_atendimento}' nao encontrado ou ja finalizado.")

        atendimento.finalizar(datetime.now().isoformat())
        self.em_andamento.remove(atendimento)
        self.historico.append(atendimento)

        atendente = self.repositorio.buscar_atendente(atendimento.id_atendente)
        if atendente:
            atendente.ocupado = False

        self.lista_ativos.remover(atendimento.id_cliente)

        self.pilha_desfazer.push(atendimento)

        return atendimento

    def desfazer_ultimo(self):
        if self.pilha_desfazer.vazia():
            raise IndexError("Nenhuma acao para desfazer.")

        atendimento = self.pilha_desfazer.pop()
        atendimento.fim = None
        atendimento.duracao_minutos = None
        self.historico.remove(atendimento)
        self.em_andamento.append(atendimento)

        atendente = self.repositorio.buscar_atendente(atendimento.id_atendente)
        if atendente:
            atendente.ocupado = True

        cliente = self.repositorio.buscar_cliente_por_id(atendimento.id_cliente)
        if cliente:
            self.lista_ativos.inserir(cliente)

        return atendimento

    def historico_cliente(self, id_cliente):
        """Retorna todos os atendimentos de um cliente."""
        return [a for a in self.historico if a.id_cliente == id_cliente]

    def tempo_medio(self):
        
        finalizados = [a for a in self.historico if a.duracao_minutos is not None]
        if not finalizados:
            return 0

        def somar_recursivo(lista, indice):
            if indice == len(lista):
                return 0
            return lista[indice].duracao_minutos + somar_recursivo(lista, indice + 1)

        total = somar_recursivo(finalizados, 0)
        return round(total / len(finalizados), 2)

    def top5_clientes(self):
        contagem = {}
        for a in self.historico:
            contagem[a.id_cliente] = contagem.get(a.id_cliente, 0) + 1

        lista = list(contagem.items())  

        for i in range(1, len(lista)):
            chave = lista[i]
            j = i - 1
            while j >= 0 and lista[j][1] < chave[1]:
                lista[j + 1] = lista[j]
                j -= 1
            lista[j + 1] = chave

        return lista[:5]

    def alerta_espera(self, limite_minutos=10):
        alertas = []
        agora = datetime.now()
        for c in self.fila.para_lista():
            alertas.append(c)
        return alertas

    def remover_cliente_inativo(self, id_cliente):
        for a in self.em_andamento:
            if a.id_cliente == id_cliente:
                raise ValueError(f"Cliente '{id_cliente}' tem atendimento em aberto.")

        self.lista_ativos.remover(id_cliente)
        cliente = self.repositorio.remover_cliente(id_cliente)
        return cliente

    def listar_fila(self):
        return self.fila.para_lista()

    def listar_em_andamento(self):
        return list(self.em_andamento)

    def listar_historico(self):
        return list(self.historico)
