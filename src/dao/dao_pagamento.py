from datetime import date
from models.pagamento import Pagamento, PagamentoDinheiro, PagamentoPix, PagamentoCartao
from models.pessoa import Pessoa
from models.viagem import Viagem
from .dao_base import DAOBase
from .dao_pessoa import DAOPessoa
from .dao_viagem import DAOViagem


class DAOPagamento(DAOBase):
    def __init__(self):
        super().__init__("pagamentos.json")
        self.__dao_pessoa = DAOPessoa()
        self.__dao_viagem = DAOViagem()

    def _serializar_entidade(self, pagamento):
        base_data = {
            "id": pagamento.id,
            "data": pagamento.data.isoformat(),
            "valor_pago": pagamento.valor_pago,
            "pagador_id": pagamento.pagador.id,
            "viagem_id": pagamento.viagem.id,
            "tipo": pagamento.__class__.__name__,
        }

        if isinstance(pagamento, PagamentoPix):
            base_data["cpf_pagador"] = pagamento.cpf_pagador
        elif isinstance(pagamento, PagamentoCartao):
            base_data["numero_cartao"] = pagamento.numero_cartao
            base_data["bandeira"] = pagamento.bandeira

        return base_data

    def _deserializar_entidade(self, dados):
        pessoas = self.__dao_pessoa.carregar()
        pagador = next((p for p in pessoas if p.id == dados["pagador_id"]), None)
        if not pagador:
            raise ValueError(f"Pagador com ID {dados['pagador_id']} não encontrado")

        viagens = self.__dao_viagem.carregar()
        viagem = next((v for v in viagens if v.id == dados["viagem_id"]), None)
        if not viagem:
            raise ValueError(f"Viagem com ID {dados['viagem_id']} não encontrada")

        if dados["tipo"] == "PagamentoPix":
            return PagamentoPix(
                date.fromisoformat(dados["data"]),
                dados["valor_pago"],
                pagador,
                viagem,
                dados["cpf_pagador"],
                dados.get("id"),
            )
        elif dados["tipo"] == "PagamentoCartao":
            return PagamentoCartao(
                date.fromisoformat(dados["data"]),
                dados["valor_pago"],
                pagador,
                viagem,
                dados["numero_cartao"],
                dados["bandeira"],
                dados.get("id"),
            )
        else:
            return PagamentoDinheiro(
                date.fromisoformat(dados["data"]),
                dados["valor_pago"],
                pagador,
                viagem,
                dados.get("id"),
            )
