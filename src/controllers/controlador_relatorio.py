from collections import Counter
from typing import List, Tuple
from dao.dao_viagem import DAOViagem
from models.exceptions import ListaVaziaException


class ControladorRelatorio:
    def __init__(self, controlador_principal):
        self.__controlador_principal = controlador_principal
        self.__dao_viagem = DAOViagem()

    def relatorio_destinos_mais_populares(self) -> List[Tuple[str, int]]:
        try:
            viagens = self.__dao_viagem.carregar()

            if not viagens:
                raise ListaVaziaException(
                    "Não há viagens cadastradas para gerar o relatório"
                )

            contador_cidades = Counter()

            for viagem in viagens:
                for itinerario in viagem.itinerarios:
                    for passeio in itinerario.passeios:
                        cidade_nome = passeio.cidade.nome
                        contador_cidades[cidade_nome] += 1

            destinos_populares = contador_cidades.most_common()

            if not destinos_populares:
                raise ListaVaziaException(
                    "Não há dados suficientes para gerar o relatório de destinos populares"
                )

            return destinos_populares

        except Exception as e:
            raise Exception(f"Erro ao gerar relatório de destinos populares: {str(e)}")
