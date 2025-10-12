import uuid
from datetime import date
from models.pessoa import Pessoa
from models.cidade import Cidade
from models.itinerario_viagem import ItinerarioViagem
from models.trecho_viagem import TrechoViagem
from models.passagem import Passagem


class Viagem:

    def __init__(
        self,
        data_inicio: date,
        data_fim: date,
        valor_total_pacote: float,
        id: str = None,
    ):
        if not isinstance(data_inicio, date):
            raise TypeError("data_inicio deve ser uma instância de date")
        if not isinstance(data_fim, date):
            raise TypeError("data_fim deve ser uma instância de date")
        if not isinstance(valor_total_pacote, (int, float)):
            raise TypeError("valor_total_pacote deve ser um número")
        if valor_total_pacote < 0:
            raise ValueError("valor_total_pacote não pode ser negativo")

        self.__id = id if id else str(uuid.uuid4())
        self.__data_inicio = data_inicio
        self.__data_fim = data_fim
        self.__valor_total_pacote = valor_total_pacote
        self.__participantes = []
        self.__destinos_visitados = []
        self.__itinerarios = []
        self.__trechos = []
        self.__pagamentos_recebidos = []
        self.__passagens_compradas = []

    @property
    def id(self) -> str:
        return self.__id

    @property
    def data_inicio(self) -> date:
        return self.__data_inicio

    @data_inicio.setter
    def data_inicio(self, data: date):
        if not isinstance(data, date):
            raise TypeError("data deve ser uma instância de date")
        self.__data_inicio = data

    @property
    def data_fim(self) -> date:
        return self.__data_fim

    @data_fim.setter
    def data_fim(self, data: date):
        if not isinstance(data, date):
            raise TypeError("data deve ser uma instância de date")
        self.__data_fim = data

    @property
    def valor_total_pacote(self) -> float:
        return self.__valor_total_pacote

    @valor_total_pacote.setter
    def valor_total_pacote(self, valor: float):
        if not isinstance(valor, (int, float)):
            raise TypeError("valor deve ser um número")
        if valor < 0:
            raise ValueError("valor não pode ser negativo")
        self.__valor_total_pacote = valor

    def incluir_participante(self, pessoa: Pessoa):
        if not isinstance(pessoa, Pessoa):
            raise TypeError("pessoa deve ser uma instância de Pessoa")
        if pessoa not in self.__participantes and pessoa.pode_participar_viagem():
            self.__participantes.append(pessoa)

    def excluir_participante(self, pessoa: Pessoa):
        if not isinstance(pessoa, Pessoa):
            raise TypeError("pessoa deve ser uma instância de Pessoa")
        if pessoa in self.__participantes:
            self.__participantes.remove(pessoa)

    def incluir_destino(self, cidade: Cidade):
        if not isinstance(cidade, Cidade):
            raise TypeError("cidade deve ser uma instância de Cidade")
        if cidade not in self.__destinos_visitados:
            self.__destinos_visitados.append(cidade)

    def excluir_destino(self, cidade: Cidade):
        if not isinstance(cidade, Cidade):
            raise TypeError("cidade deve ser uma instância de Cidade")
        if cidade in self.__destinos_visitados:
            self.__destinos_visitados.remove(cidade)

    def incluir_itinerario(self, itinerario: ItinerarioViagem):
        if not isinstance(itinerario, ItinerarioViagem):
            raise TypeError("itinerario deve ser uma instância de ItinerarioViagem")
        if itinerario not in self.__itinerarios:
            self.__itinerarios.append(itinerario)

    def excluir_itinerario(self, itinerario: ItinerarioViagem):
        if not isinstance(itinerario, ItinerarioViagem):
            raise TypeError("itinerario deve ser uma instância de ItinerarioViagem")
        if itinerario in self.__itinerarios:
            self.__itinerarios.remove(itinerario)

    def incluir_trecho(self, trecho: TrechoViagem):
        if not isinstance(trecho, TrechoViagem):
            raise TypeError("trecho deve ser uma instância de TrechoViagem")
        if trecho not in self.__trechos:
            self.__trechos.append(trecho)

    def excluir_trecho(self, trecho: TrechoViagem):
        if not isinstance(trecho, TrechoViagem):
            raise TypeError("trecho deve ser uma instância de TrechoViagem")
        if trecho in self.__trechos:
            self.__trechos.remove(trecho)

    def incluir_pagamento(self, pagamento):
        from models.pagamento import Pagamento

        if not isinstance(pagamento, Pagamento):
            raise TypeError("pagamento deve ser uma instância de Pagamento")
        if pagamento not in self.__pagamentos_recebidos:
            self.__pagamentos_recebidos.append(pagamento)

    def excluir_pagamento(self, pagamento):
        from models.pagamento import Pagamento

        if not isinstance(pagamento, Pagamento):
            raise TypeError("pagamento deve ser uma instância de Pagamento")
        if pagamento in self.__pagamentos_recebidos:
            self.__pagamentos_recebidos.remove(pagamento)

    def incluir_passagem(self, passagem: Passagem):
        if not isinstance(passagem, Passagem):
            raise TypeError("passagem deve ser uma instância de Passagem")
        if passagem not in self.__passagens_compradas:
            self.__passagens_compradas.append(passagem)

    def excluir_passagem(self, passagem: Passagem):
        if not isinstance(passagem, Passagem):
            raise TypeError("passagem deve ser uma instância de Passagem")
        if passagem in self.__passagens_compradas:
            self.__passagens_compradas.remove(passagem)

    def get_valor_total_pago(self) -> float:
        return sum(pagamento.valor_pago for pagamento in self.__pagamentos_recebidos)

    def get_valor_restante(self) -> float:
        return self.__valor_total_pacote - self.get_valor_total_pago()

    def get_valor_pago_por_pessoa(self, pessoa: Pessoa) -> float:
        if not isinstance(pessoa, Pessoa):
            raise TypeError("pessoa deve ser uma instância de Pessoa")

        total_pago = 0.0
        for pagamento in self.__pagamentos_recebidos:
            if pagamento.pagador == pessoa:
                total_pago += pagamento.valor_pago
        return total_pago

    def get_valor_restante_por_pessoa(self, pessoa: Pessoa) -> float:
        if not isinstance(pessoa, Pessoa):
            raise TypeError("pessoa deve ser uma instância de Pessoa")

        if pessoa not in self.__participantes:
            raise ValueError("pessoa não é participante desta viagem")

        valor_por_pessoa = self.__valor_total_pacote / len(self.__participantes)
        valor_pago = self.get_valor_pago_por_pessoa(pessoa)
        return valor_por_pessoa - valor_pago

    def get_pessoas_com_pagamento_completo(self) -> list:
        pessoas_completas = []
        for pessoa in self.__participantes:
            if self.get_valor_restante_por_pessoa(pessoa) <= 0:
                pessoas_completas.append(pessoa)
        return pessoas_completas

    def get_pessoas_com_pagamento_pendente(self) -> list:
        pessoas_pendentes = []
        for pessoa in self.__participantes:
            if self.get_valor_restante_por_pessoa(pessoa) > 0:
                pessoas_pendentes.append(pessoa)
        return pessoas_pendentes

    def pode_iniciar_viagem(self) -> bool:
        from datetime import date

        if len(self.get_pessoas_com_pagamento_pendente()) > 0:
            return False

        for passagem in self.__passagens_compradas:
            if not passagem.compra_efetuada:
                return False

        if self.__data_inicio < date.today():
            return False

        return True

    def validar_viagem(self) -> bool:

        if len(self.__participantes) == 0:
            return False

        for pessoa in self.__participantes:
            if not pessoa.pode_participar_viagem():
                return False

        if self.__data_fim <= self.__data_inicio:
            return False

        if len(self.__destinos_visitados) == 0:
            return False

        if len(self.__trechos) == 0:
            return False

        return True

    @property
    def participantes(self) -> list:
        return self.__participantes.copy()

    @property
    def destinos_visitados(self) -> list:
        return self.__destinos_visitados.copy()

    @property
    def itinerarios(self) -> list:
        return self.__itinerarios.copy()

    @property
    def trechos(self) -> list:
        return self.__trechos.copy()

    @property
    def pagamentos_recebidos(self) -> list:
        return self.__pagamentos_recebidos.copy()

    @property
    def passagens_compradas(self) -> list:
        return self.__passagens_compradas.copy()

    def __str__(self) -> str:
        return f"Viagem({self.__data_inicio} a {self.__data_fim}, R$ {self.__valor_total_pacote:.2f}, {len(self.__participantes)} participantes)"
