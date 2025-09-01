# Modelagem de Classes - Gerenciamento de Viagens

A seguir, a descrição das classes, atributos, métodos e relacionamentos que compõem o sistema de gerenciamento de viagens.

---

### **Classe: Pessoa**

Representa as pessoas que participam do grupo de viagem.

- **Atributos:**

  - `- nome: str`
  - `- celular: str`
  - `- identificacao: str` (CPF ou Passaporte)
  - `- idade: int` (Para validar a regra de maiores de 18 anos)

- **Métodos:**
  - `+ __init__(nome: str, celular: str, identificacao: str, idade: int)`
  - `+ get_nome() -> str`
  - `+ set_nome(nome: str) -> None`
  - `+ get_celular() -> str`
  - `+ set_celular(celular: str) -> None`
  - `+ get_identificacao() -> str`
  - `+ set_identificacao(identificacao: str) -> None`
  - `+ get_idade() -> int`
  - `+ set_idade(idade: int) -> None`

---

### **Classe: Viagem**

Classe central que representa o planejamento da viagem em grupo.

- **Atributos:**

  - `- destinos: list[Destino]`
  - `- data_inicio: date`
  - `- data_fim: date`
  - `- participantes: list[Pessoa]`
  - `- itinerario: list[PasseioTuristico]`
  - `- trechos: list[Trecho]`
  - `- pagamentos: list[Pagamento]`

- **Métodos:**
  - `+ __init__(data_inicio: date, data_fim: date)`
  - `+ get_destinos() -> list[Destino]`
  - `+ add_destino(destino: Destino) -> None`
  - `+ get_data_inicio() -> date`
  - `+ set_data_inicio(data_inicio: date) -> None`
  - `+ get_data_fim() -> date`
  - `+ set_data_fim(data_fim: date) -> None`
  - `+ get_participantes() -> list[Pessoa]`
  - `+ add_participante(participante: Pessoa) -> None`
  - `+ get_itinerario() -> list[PasseioTuristico]`
  - `+ add_passeio(passeio: PasseioTuristico) -> None`
  - `+ get_trechos() -> list[Trecho]`
  - `+ add_trecho(trecho: Trecho) -> None`
  - `+ get_pagamentos() -> list[Pagamento]`
  - `+ add_pagamento(pagamento: Pagamento) -> None`
  - `+ calcular_saldo_devedor(pessoa: Pessoa) -> float`

---

### **Classe: Destino**

Representa os locais (cidades e países) a serem visitados.

- **Atributos:**

  - `- cidade: str`
  - `- pais: str`

- **Métodos:**
  - `+ __init__(cidade: str, pais: str)`
  - `+ get_cidade() -> str`
  - `+ set_cidade(cidade: str) -> None`
  - `+ get_pais() -> str`
  - `+ set_pais(pais: str) -> None`

---

### **Classe: PasseioTuristico**

Representa os passeios a serem realizados em cada cidade do itinerário.

- **Atributos:**

  - `- cidade: str`
  - `- atracao_turistica: str`
  - `- horario_inicio: time`
  - `- horario_fim: time`
  - `- valor: float`
  - `- pessoa: Pessoa`

- **Métodos:**
  - `+ __init__(cidade: str, atracao: str, inicio: time, fim: time, valor: float, pessoa: Pessoa)`
  - `+ get_cidade() -> str`
  - `+ set_cidade(cidade: str) -> None`
  - `+ get_atracao_turistica() -> str`
  - `+ set_atracao_turistica(atracao: str) -> None`
  - `+ get_horario_inicio() -> time`
  - `+ set_horario_inicio(inicio: time) -> None`
  - `+ get_horario_fim() -> time`
  - `+ set_horario_fim(fim: time) -> None`
  - `+ get_valor() -> float`
  - `+ set_valor(valor: float) -> None`
  - `+ get_pessoa() -> Pessoa`
  - `+ set_pessoa(pessoa: Pessoa) -> None`

---

### **Classe: Trecho**

Representa cada um dos trechos da viagem.

- **Atributos:**

  - `- data: date`
  - `- local_origem: str`
  - `- local_destino: str`
  - `- meio_transporte: MeioTransporte`
  - `- compra_feita: bool`
  - `- responsavel_compra: Pessoa`

- **Métodos:**
  - `+ __init__(data: date, origem: str, destino: str, transporte: MeioTransporte, responsavel: Pessoa)`
  - `+ get_data() -> date`
  - `+ set_data(data: date) -> None`
  - `+ get_local_origem() -> str`
  - `+ set_local_origem(origem: str) -> None`
  - `+ get_local_destino() -> str`
  - `+ set_local_destino(destino: str) -> None`
  - `+ get_meio_transporte() -> MeioTransporte`
  - `+ set_meio_transporte(transporte: MeioTransporte) -> None`
  - `+ get_compra_feita() -> bool`
  - `+ set_compra_feita(status: bool) -> None`
  - `+ get_responsavel_compra() -> Pessoa`
  - `+ set_responsavel_compra(responsavel: Pessoa) -> None`

---

### **Classe: MeioTransporte**

Representa os tipos de meios de transporte utilizados nos trechos da viagem.

- **Atributos:**

  - `- tipo: str` (Ex: avião, carro, trem)
  - `- empresa: Empresa`

- **Métodos:**
  - `+ __init__(tipo: str, empresa: Empresa)`
  - `+ get_tipo() -> str`
  - `+ set_tipo(tipo: str) -> None`
  - `+ get_empresa() -> Empresa`
  - `+ set_empresa(empresa: Empresa) -> None`

---

### **Classe: Empresa**

Representa as empresas que fornecem os meios de transporte.

- **Atributos:**

  - `- nome: str`
  - `- cnpj: str`
  - `- telefone: str`

- **Métodos:**
  - `+ __init__(nome: str, cnpj: str, telefone: str)`
  - `+ get_nome() -> str`
  - `+ set_nome(nome: str) -> None`
  - `+ get_cnpj() -> str`
  - `+ set_cnpj(cnpj: str) -> None`
  - `+ get_telefone() -> str`
  - `+ set_telefone(telefone: str) -> None`

---

### **Classe Abstrata: Pagamento**

Classe base para registrar os pagamentos (parciais ou totais) das pessoas.

- **Atributos:**

  - `# data: date`
  - `# viagem: Viagem`
  - `# pessoa: Pessoa`
  - `# valor_pago: float`

- **Métodos:**
  - `+ __init__(data: date, viagem: Viagem, pessoa: Pessoa, valor: float)`
  - `+ get_data() -> date`
  - `+ set_data(data: date) -> None`
  - `+ get_viagem() -> Viagem`
  - `+ set_viagem(viagem: Viagem) -> None`
  - `+ get_pessoa() -> Pessoa`
  - `+ set_pessoa(pessoa: Pessoa) -> None`
  - `+ get_valor_pago() -> float`
  - `+ set_valor_pago(valor: float) -> None`

---

### **Classe: PagamentoDinheiro**

Representa um pagamento feito em dinheiro. Herda de `Pagamento`.

- **Atributos:**

  - _(Herda todos os atributos de Pagamento)_

- **Métodos:**
  - `+ __init__(data: date, viagem: Viagem, pessoa: Pessoa, valor: float)`

---

### **Classe: PagamentoPix**

Representa um pagamento feito via PIX. Herda de `Pagamento`.

- **Atributos:**

  - _(Herda todos os atributos de Pagamento)_
  - `- cpf_pagador: str`

- **Métodos:**
  - `+ __init__(data: date, viagem: Viagem, pessoa: Pessoa, valor: float, cpf: str)`
  - `+ get_cpf_pagador() -> str`
  - `+ set_cpf_pagador(cpf: str) -> None`

---

### **Classe: PagamentoCartao**

Representa um pagamento feito com cartão de crédito. Herda de `Pagamento`.

- **Atributos:**

  - _(Herda todos os atributos de Pagamento)_
  - `- numero_cartao: str`
  - `- bandeira: str`

- **Métodos:**
  - `+ __init__(data: date, viagem: Viagem, pessoa: Pessoa, valor: float, numero: str, bandeira: str)`
  - `+ get_numero_cartao() -> str`
  - `+ set_numero_cartao(numero: str) -> None`
  - `+ get_bandeira() -> str`
  - `+ set_bandeira(bandeira: str) -> None`
