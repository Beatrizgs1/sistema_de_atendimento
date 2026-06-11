from datetime import datetime


class Atendimento:
    def __init__(self, id_atendimento, id_cliente, id_atendente, inicio):
        self.id_atendimento = id_atendimento
        self.id_cliente = id_cliente
        self.id_atendente = id_atendente
        self.inicio = inicio          
        self.fim = None               
        self.duracao_minutos = None   

    def finalizar(self, fim):
        self.fim = fim
        inicio_dt = datetime.fromisoformat(self.inicio)
        fim_dt = datetime.fromisoformat(self.fim)
        delta = fim_dt - inicio_dt
        self.duracao_minutos = round(delta.total_seconds() / 60, 2)

    def to_dict(self):
        return {
            "id_atendimento": self.id_atendimento,
            "id_cliente": self.id_cliente,
            "id_atendente": self.id_atendente,
            "inicio": self.inicio,
            "fim": self.fim,
            "duracao_minutos": self.duracao_minutos,
        }

    @staticmethod
    def from_dict(d):
        a = Atendimento(
            id_atendimento=d["id_atendimento"],
            id_cliente=d["id_cliente"],
            id_atendente=d["id_atendente"],
            inicio=d["inicio"],
        )
        a.fim = d.get("fim")
        a.duracao_minutos = d.get("duracao_minutos")
        return a

    def __repr__(self):
        return (
            f"Atendimento {self.id_atendimento} | "
            f"Cliente {self.id_cliente} | "
            f"Atendente {self.id_atendente} | "
            f"Inicio: {self.inicio} | "
            f"Duracao: {self.duracao_minutos} min"
        )
