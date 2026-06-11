import json
import csv
import os

from cliente import Cliente
from atendente import Atendente
from atendimento import Atendimento

ARQUIVO_CLIENTES = "dados/clientes.json"
ARQUIVO_ATENDENTES = "dados/atendentes.json"
ARQUIVO_HISTORICO = "dados/historico.json"

def _garantir_pasta():
    os.makedirs("dados", exist_ok=True)


def salvar_tudo(repositorio, historico):
    _garantir_pasta()

    with open(ARQUIVO_CLIENTES, "w", encoding="utf-8") as f:
        json.dump([c.to_dict() for c in repositorio.listar_clientes()], f, ensure_ascii=False, indent=2)

    with open(ARQUIVO_ATENDENTES, "w", encoding="utf-8") as f:
        json.dump([a.to_dict() for a in repositorio.listar_atendentes()], f, ensure_ascii=False, indent=2)

    
    with open(ARQUIVO_HISTORICO, "w", encoding="utf-8") as f:
        json.dump([a.to_dict() for a in historico], f, ensure_ascii=False, indent=2)


def carregar_tudo():
    _garantir_pasta()

    clientes = []
    if os.path.exists(ARQUIVO_CLIENTES):
        with open(ARQUIVO_CLIENTES, "r", encoding="utf-8") as f:
            clientes = [Cliente.from_dict(d) for d in json.load(f)]

    atendentes = []
    if os.path.exists(ARQUIVO_ATENDENTES):
        with open(ARQUIVO_ATENDENTES, "r", encoding="utf-8") as f:
            atendentes = [Atendente.from_dict(d) for d in json.load(f)]

    historico = []
    if os.path.exists(ARQUIVO_HISTORICO):
        with open(ARQUIVO_HISTORICO, "r", encoding="utf-8") as f:
            historico = [Atendimento.from_dict(d) for d in json.load(f)]

    return clientes, atendentes, historico


def exportar_csv(historico, caminho="dados/relatorio.csv"):
    _garantir_pasta()
    with open(caminho, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["ID", "Cliente", "Atendente", "Inicio", "Fim", "Duracao (min)"])
        for a in historico:
            writer.writerow([
                a.id_atendimento,
                a.id_cliente,
                a.id_atendente,
                a.inicio,
                a.fim or "-",
                a.duracao_minutos or "-",
            ])
    print(f"  Relatorio exportado para '{caminho}'.")
