from datetime import datetime
import FreeSimpleGUI as sg
from models.utils.validadores import formata_cpf, normaliza_cpf
from views.tela_base_gui import TelaBaseGUI


class TelaPagamentoGUI(TelaBaseGUI):
    def __init__(self):
        super().__init__()
        self._controlador_pessoa = None
        self._controlador_viagem = None

    def set_controlador_pessoa(self, controlador_pessoa):
        self._controlador_pessoa = controlador_pessoa

    def set_controlador_viagem(self, controlador_viagem):
        self._controlador_viagem = controlador_viagem

    def le_opcao(self):
        layout = [
            [
                sg.Text(
                    "Pagamentos",
                    font=("Helvetica", 18, "bold"),
                    justification="center",
                    expand_x=True,
                )
            ],
            [sg.Button("Incluir", key="-INCLUIR-", size=(25, 2))],
            [sg.Button("Listar", key="-LISTAR-", size=(25, 2))],
            [sg.Button("Editar", key="-EDITAR-", size=(25, 2))],
            [sg.Button("Excluir", key="-EXCLUIR-", size=(25, 2))],
            [sg.VPush()],
            [sg.Button("Voltar", key="-VOLTAR-", size=(25, 2))],
        ]
        window = sg.Window("Pagamentos", layout, finalize=True)
        event, _ = window.read()
        window.close()
        if event in (sg.WIN_CLOSED, "-VOLTAR-"):
            return "-VOLTAR-"
        return event

    def _combo_pessoas(self):
        pessoas = (
            self._controlador_pessoa.get_entidades() if self._controlador_pessoa else []
        )
        return {f"{p.nome} ({p.identificacao})": p for p in pessoas}

    def _combo_viagens(self):
        viagens = (
            self._controlador_viagem.get_entidades() if self._controlador_viagem else []
        )
        return {
            f"{v.id[:6]} | {v.data_inicio.strftime('%d/%m/%Y')} - {v.data_fim.strftime('%d/%m/%Y')} | {v.valor_total_pacote:.2f}": v
            for v in viagens
        }

    def pega_dados_entidade(self, dados_atuais=None):
        mapa_pessoas = self._combo_pessoas()
        mapa_viagens = self._combo_viagens()
        if not mapa_pessoas:
            self.mostra_erro("Cadastre pessoas antes de registrar pagamentos.")
            return None
        if not mapa_viagens:
            self.mostra_erro("Cadastre viagens antes de registrar pagamentos.")
            return None

        pessoa_default = (
            f"{dados_atuais['pagador'].nome} ({formata_cpf(dados_atuais['pagador'].identificacao)})"
            if dados_atuais
            else next(iter(mapa_pessoas.keys()))
        )
        viagem_default = None
        if dados_atuais:
            for chave, viagem in mapa_viagens.items():
                if viagem.id == dados_atuais["viagem"].id:
                    viagem_default = chave
                    break
        if viagem_default is None:
            viagem_default = next(iter(mapa_viagens.keys()))

        data_atual = dados_atuais["data"].strftime("%Y-%m-%d") if dados_atuais else ""
        valor_atual = f"{dados_atuais['valor_pago']:.2f}" if dados_atuais else ""

        tipo_atual = 1
        extra_pix = ""
        extra_cartao = {"numero": "", "bandeira": ""}
        if dados_atuais:
            tipo_nome = dados_atuais["tipo"]
            if tipo_nome == "PagamentoPix":
                tipo_atual = 2
                extra_pix = formata_cpf(dados_atuais.get("cpf_pagador", ""))
            elif tipo_nome == "PagamentoCartao":
                tipo_atual = 3
                extra_cartao = {
                    "numero": dados_atuais.get("numero_cartao", ""),
                    "bandeira": dados_atuais.get("bandeira", ""),
                }

        titulo = "Editar Pagamento" if dados_atuais else "Novo Pagamento"
        layout = [
            [sg.Text(titulo, font=("Helvetica", 16))],
            [
                sg.Text("Data (YYYY-MM-DD):", size=(20, 1)),
                sg.Input(default_text=data_atual, key="-DATA-"),
            ],
            [
                sg.Text("Valor Pago (R$):", size=(20, 1)),
                sg.Input(default_text=valor_atual, key="-VALOR-"),
            ],
            [
                sg.Text("Pagador:", size=(20, 1)),
                sg.Combo(
                    list(mapa_pessoas.keys()),
                    default_value=pessoa_default,
                    readonly=True,
                    key="-PESSOA-",
                ),
            ],
            [
                sg.Text("Viagem:", size=(20, 1)),
                sg.Combo(
                    list(mapa_viagens.keys()),
                    default_value=viagem_default,
                    readonly=True,
                    key="-VIAGEM-",
                ),
            ],
            [
                sg.Text("Tipo de Pagamento:", size=(20, 1)),
                sg.Combo(
                    ["1 - Dinheiro", "2 - PIX", "3 - Cartão"],
                    default_value=f"{tipo_atual} - {'Dinheiro' if tipo_atual ==1 else 'PIX' if tipo_atual==2 else 'Cartão'}",
                    readonly=True,
                    key="-TIPO-",
                ),
            ],
            [
                sg.Text("CPF (PIX):", size=(20, 1)),
                sg.Input(default_text=extra_pix, key="-CPF-"),
            ],
            [
                sg.Text("Número Cartão:", size=(20, 1)),
                sg.Input(default_text=extra_cartao["numero"], key="-NUMERO-"),
            ],
            [
                sg.Text("Bandeira Cartão:", size=(20, 1)),
                sg.Input(default_text=extra_cartao["bandeira"], key="-BANDEIRA-"),
            ],
            [
                sg.Button("Salvar", key="-SALVAR-"),
                sg.Button("Cancelar", key="-CANCELAR-"),
            ],
        ]

        window = sg.Window(titulo, layout, finalize=True)
        dados = None
        while True:
            event, values = window.read()
            if event in (sg.WIN_CLOSED, "-CANCELAR-"):
                break
            if event == "-SALVAR-":
                try:
                    data_pagto = datetime.strptime(values["-DATA-"], "%Y-%m-%d").date()
                    valor = float(values["-VALOR-"])
                    tipo = int(values["-TIPO-"].split(" - ")[0])

                    dados = {
                        "data": data_pagto,
                        "valor_pago": valor,
                        "pagador": mapa_pessoas[values["-PESSOA-"]],
                        "viagem": mapa_viagens[values["-VIAGEM-"]],
                        "tipo": tipo,
                    }

                    if tipo == 2:
                        cpf_informado = values["-CPF-"].strip()
                        if not cpf_informado:
                            raise ValueError("Informe o CPF para pagamentos via PIX.")
                        dados["cpf_pagador"] = normaliza_cpf(cpf_informado)
                    elif tipo == 3:
                        numero = values["-NUMERO-"].strip()
                        bandeira = values["-BANDEIRA-"].strip()
                        if not numero or not bandeira:
                            raise ValueError("Informe número e bandeira do cartão.")
                        dados["numero_cartao"] = numero
                        dados["bandeira"] = bandeira

                    break
                except ValueError as err:
                    self.mostra_erro(str(err))

        window.close()
        return dados

    def mostra_lista_entidades(self, dados_lista):
        if not dados_lista:
            self.mostra_mensagem("Pagamentos", "Nenhum pagamento registrado.")
            return

        headings = ["ID", "Data", "Pagador", "Viagem", "Valor", "Tipo"]
        data = []
        for d in dados_lista:
            viagem = (
                f"{d['viagem'].data_inicio.strftime('%d/%m/%Y')} - "
                f"{d['viagem'].data_fim.strftime('%d/%m/%Y')}"
            )
            data.append(
                [
                    d["id"],
                    d["data"].strftime("%d/%m/%Y"),
                    d["pagador"].nome,
                    viagem,
                    f"{d['valor_pago']:.2f}",
                    d["tipo"].replace("Pagamento", ""),
                ]
            )

        self.mostra_lista("Pagamentos", headings, data)

    def seleciona_entidade(self, dados_lista, titulo_janela):
        if not dados_lista:
            self.mostra_erro("Nenhum pagamento cadastrado.")
            return None

        headings = ["ID", "Pagador", "Data", "Valor"]
        data = []
        id_lookup = []
        for d in dados_lista:
            data.append(
                [
                    d["id"],
                    d["pagador"].nome,
                    d["data"].strftime("%d/%m/%Y"),
                    f"{d['valor_pago']:.2f}",
                ]
            )
            id_lookup.append(d["id"])

        layout = [
            [sg.Text(titulo_janela, font=("Helvetica", 16))],
            [
                sg.Table(
                    values=data,
                    headings=headings,
                    auto_size_columns=True,
                    num_rows=min(15, len(data)),
                    select_mode=sg.TABLE_SELECT_MODE_BROWSE,
                    key="-TABLE-",
                )
            ],
            [
                sg.Button("Selecionar", key="-OK-"),
                sg.Button("Cancelar", key="-CANCELAR-"),
            ],
        ]

        window = sg.Window(titulo_janela, layout, finalize=True)
        selecionado = None
        while True:
            event, values = window.read()
            if event in (sg.WIN_CLOSED, "-CANCELAR-"):
                break
            if event == "-OK-":
                if values["-TABLE-"]:
                    selecionado = id_lookup[values["-TABLE-"][0]]
                    break
                self.mostra_erro("Selecione um pagamento.")

        window.close()
        return selecionado
