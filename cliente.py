class Cliente:
    def __init__(self, id_cliente, nome, telefone, prioridade=False):
        if not id_cliente or not str(id_cliente).strip():
            raise ValueError("ID do cliente nao pode ser vazio.")
        if not nome or not nome.strip():
            raise ValueError("Nome nao pode ser vazio.")
        if not telefone or not telefone.strip():
            raise ValueError("Telefone nao pode ser vazio.")

        self.id_cliente = str(id_cliente).strip()
        self.nome = nome.strip()
        self.telefone = telefone.strip()
        self.prioridade = bool(prioridade)  
        self.ativo = True

    def to_dict(self):
        return {
            "id_cliente": self.id_cliente,
            "nome": self.nome,
            "telefone": self.telefone,
            "prioridade": self.prioridade,
            "ativo": self.ativo,
        }

    @staticmethod
    def from_dict(d):
        c = Cliente(
            id_cliente=d["id_cliente"],
            nome=d["nome"],
            telefone=d["telefone"],
            prioridade=d["prioridade"],
        )
        c.ativo = d.get("ativo", True)
        return c

    def __repr__(self):
        tipo = "PRIORITARIO" if self.prioridade else "Normal"
        return f"[{self.id_cliente}] {self.nome} | {self.telefone} | {tipo}"
