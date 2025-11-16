from views.tela_base import TelaBase


class TelaRelatorio(TelaBase):
    def le_opcao(self):
        """
        Mostra o menu de opções de relatórios e retorna a escolha.
        O loop principal e o "Voltar" (opção 0) são gerenciados
        pelo ControladorBase.
        """
        opcoes = {1: "Destinos Mais Populares"}

        self.tela_opcoes("RELATÓRIOS", opcoes)

        try:
            opcao = int(input("Escolha a opção: "))
            return opcao
        except ValueError:
            self.mostra_erro("Opção inválida! Digite um número.")
            return -1

    def pega_dados_entidade(self, dados_atuais=None):
        pass  # Não aplicável para relatórios

    def mostra_relatorio_destinos(self, destinos):
        """
        Recebe uma lista de tuplas (destino, visitas) e a exibe
        de forma formatada na tela.
        """
        try:
            self.limpar_tela()
            print("\n-------- DESTINOS MAIS POPULARES --------")

            print(f"\n{'Posição':<8} {'Destino':<30} {'Número de Visitas':<20}")
            print("-" * 60)

            for i, (destino, visitas) in enumerate(destinos, 1):
                print(f"{i:<8} {destino:<30} {visitas:<20}")

            print(f"\nTotal de destinos analisados: {len(destinos)}")

        except Exception as e:
            print(f"ERRO inesperado ao exibir relatório: {str(e)}")

        input("\nPressione ENTER para continuar...")
        self.limpar_tela()
