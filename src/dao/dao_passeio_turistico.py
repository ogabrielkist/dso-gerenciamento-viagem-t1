from datetime import time
from models.passeio_turistico import PasseioTuristico
from .dao_base import DAOBase
from .dao_cidade import DAOCidade
from .dao_pessoa import DAOPessoa


class DAOPasseioTuristico(DAOBase):
    def __init__(self):
        super().__init__("passeios_turisticos.json")
        self.__dao_cidade = DAOCidade()
        self.__dao_pessoa = DAOPessoa()

    def _serializar_entidade(self, passeio):
        return {
            "id": passeio.id,
            "atracao_turistica": passeio.atracao_turistica,
            "horario_inicio": passeio.horario_inicio.isoformat(),
            "horario_fim": passeio.horario_fim.isoformat(),
            "valor": passeio.valor,
            "cidade_id": passeio.cidade.id,
            "participantes": [p.id for p in passeio.participantes_passeio],
        }

    def _deserializar_entidade(self, dados):
        cidades = self.__dao_cidade.carregar()
        cidade = next((c for c in cidades if c.id == dados["cidade_id"]), None)
        if not cidade:
            raise ValueError(f"Cidade com ID {dados['cidade_id']} não encontrada")

        passeio = PasseioTuristico(
            dados["atracao_turistica"],
            time.fromisoformat(dados["horario_inicio"]),
            time.fromisoformat(dados["horario_fim"]),
            dados["valor"],
            cidade,
            dados.get("id"),
        )

        participantes_ids = dados.get("participantes", [])
        if participantes_ids:
            pessoas = self.__dao_pessoa.carregar()
            mapa_pessoas = {p.id: p for p in pessoas}
            for participante_id in participantes_ids:
                pessoa = mapa_pessoas.get(participante_id)
                if pessoa:
                    passeio.incluir_participante(pessoa)

        return passeio
