from datetime import datetime
from models.passagem import Passagem
from models.pessoa import Pessoa
from models.trecho_viagem import TrechoViagem
from .dao_base import DAOBase
from .dao_pessoa import DAOPessoa
from .dao_trecho_viagem import DAOTrechoViagem


class DAOPassagem(DAOBase):
    def __init__(self):
        super().__init__("passagens.json")
        self.__dao_pessoa = DAOPessoa()
        self.__dao_trecho = DAOTrechoViagem()

    def _serializar_entidade(self, passagem):
        return {
            "id": passagem.id,
            "compra_efetuada": passagem.compra_efetuada,
            "passageiro_id": passagem.passageiro.id,
            "trecho_id": passagem.trecho.id,
            "responsavel_id": passagem.responsavel_compra.id,
        }

    def _deserializar_entidade(self, dados):
        pessoas = self.__dao_pessoa.carregar()
        passageiro = next((p for p in pessoas if p.id == dados["passageiro_id"]), None)
        if not passageiro:
            raise ValueError(
                f"Passageiro com ID {dados['passageiro_id']} não encontrado"
            )

        responsavel = next(
            (p for p in pessoas if p.id == dados["responsavel_id"]), None
        )
        if not responsavel:
            raise ValueError(
                f"Responsável com ID {dados['responsavel_id']} não encontrado"
            )

        trechos = self.__dao_trecho.carregar()
        trecho = next((t for t in trechos if t.id == dados["trecho_id"]), None)
        if not trecho:
            raise ValueError(f"Trecho com ID {dados['trecho_id']} não encontrado")

        passagem = Passagem(
            passageiro,
            trecho,
            responsavel,
            dados.get("id"),
        )
        passagem.compra_efetuada = dados["compra_efetuada"]

        return passagem
