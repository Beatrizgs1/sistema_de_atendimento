class Atendente:
    def __init__(self, id_atendente, nome):
        if not id_atendente or not str(id_atendente).strip():
            raise ValueError("ID do atendente nao pode ser vazio.")
        if not nome or not nome.strip():
            raise ValueError("Nome nao pode ser vazio.")

        self.id_atendente = str(id_atendente).strip()
        self.nome = nome.strip()
        self.ocupado = False  

    def to_dict(self):
        return {
            "id_atendente": self.id_atendente,
            "nome": self.nome,
            "ocupado": self.ocupado,
        }

    @staticmethod
    def from_dict(d):
        a = Atendente(d["id_atendente"], d["nome"])
        a.ocupado = d.get("ocupado", False)
        return a

    def __repr__(self):
        status = "Ocupado" if self.ocupado else "Livre"
        return f"[{self.id_atendente}] {self.nome} | {status}"
