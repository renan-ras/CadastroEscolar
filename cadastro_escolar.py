##############################################################
# Raciocínio Computacional (11100010563_20231_04)
# Superior de Tecnologia em Big Data e Inteligência Analítica
# RENAN ANTONIO DA SILVA
# RA 1112023101779
##############################################################

import json

def finalizar_programa():
    print('Finalizando o programa...')
    exit(0)

def limpar_tela():
    print('\n\n')

# Pausa para verificação das informações
def espera():
    input('\nPressione [ENTER] para continuar')

# Exibe o menu principal e retorna a opção escolhida pelo usuário
def menu_principal():
    limpar_tela()
    print("###### MENU PRINCIPAL ######")
    print("(0) Sair do programa")
    print("(1) Estudantes")
    print("(2) Professores")
    print("(3) Disciplinas")
    print("(4) Turmas")
    print("(5) Matrículas")
    print("#############################")
    return int(input("Escolha uma opção: "))

# Exibe o menu de operações e retorna a opção escolhida pelo usuário
# 'titulo' referencia qual tabela de dados estamos manipulando
def menu_operacoes(titulo):
    limpar_tela()
    print(f"###### MENU DE OPERAÇÕES [{titulo}] ######")
    print("(0) Retornar ao menu principal")
    print("(1) Criar novo registro")
    print("(2) Alterar um registro")
    print("(3) Excluir um registro")
    print("(4) Listar registros")
    print("################################")
    return int(input("Escolha uma opção: "))

# Carrega os dados do arquivo JSON, ou retorna um dicionário vazio em caso de erro
def carregar_dados(arquivo):
    try:
        with open(arquivo, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def salvar_dados(arquivo, dados):
    with open(arquivo, 'w') as f:
        json.dump(dados, f)

    print("Dados salvos com sucesso!")
    espera()

# verifica a existência de um código no arquivo fornecido
# necessário para a validação de Turma e Matrícula
def validar_codigo(arquivo, codigo):
    dados = carregar_dados(arquivo)
    return codigo in dados

# 'validacoes' necessário para a validação de Turma e Matrícula
def criar_registro(arquivo, campos, validacoes=None):
    dados = carregar_dados(arquivo)
    registro = {}

    for campo in campos:
        valor = input(f'Insira o {campo}: ')

        # Verifica se há validações para o campo atual
        if validacoes and campo in validacoes:
            arquivo_validacao, mensagem_erro = validacoes[campo]
            while not validar_codigo(arquivo_validacao, valor):
                print(mensagem_erro)
                valor = input(f'Insira o {campo} novamente: ')

        registro[campo] = valor

    codigo = registro[campos[0]]
    dados[codigo] = registro
    salvar_dados(arquivo, dados)

def listar_registros(arquivo, titulo):
    dados = carregar_dados(arquivo)
    
    if not dados:  # Verifica se o dicionário de dados está vazio
        print(f"Não há dados de {titulo.lower()} cadastrados.")
    else:
        for registro in dados.values():
            print(registro)

    espera()

# 'validacoes' necessário para a validação de Turma e Matrícula
def alterar_registro(arquivo, campos, validacoes=None):
    dados = carregar_dados(arquivo)
    codigo = input(f'Insira o {campos[0]} do registro que deseja alterar: ')

    if codigo not in dados:
        print(f'Registro com {campos[0]} {codigo} não encontrado!')
        espera()
    else:
        registro_alterado = {}

        # Os campos de cada base são definidos no dicionario 'arquivos' em main()
        # Itera pelos campos (atributos) e solicita ao usuário que insira os valores
        for campo in campos:
            novo_valor = input(f'Insira o novo {campo}: ')

            # Verifica se há validações para o campo atual
            if validacoes and campo in validacoes:
                arquivo_validacao, mensagem_erro = validacoes[campo]
                while not validar_codigo(arquivo_validacao, novo_valor):
                    print(mensagem_erro)
                    novo_valor = input(f'Insira o novo {campo} novamente: ')

            registro_alterado[campo] = novo_valor

        # Verificamos se o código foi alterado. O valor atualizado do primeiro campo (que é o código) é diferente do código original? Se for diferente, significa que o usuário deseja alterar o código do registro.
        if registro_alterado[campos[0]] != codigo:
            dados.pop(codigo) # Removemos o registro antigo do dicionário 'dados'
            dados[registro_alterado[campos[0]]] = registro_alterado # Adicionamos o registro atualizado ao dicionário dados com o novo código.
        else: #Se o novo valor do campo do código for igual ao original
            dados[codigo] = registro_alterado #atualizamos o registro existente no dicionário dados com os novos valores fornecidos pelo usuário

        salvar_dados(arquivo, dados)

def excluir_registro(arquivo, campo_codigo):
    dados = carregar_dados(arquivo)
    codigo = input(f'Insira o {campo_codigo} do registro que deseja excluir: ')

    if codigo not in dados:
        print(f'Registro com {campo_codigo} {codigo} não encontrado!')
        espera()
    else:
        del dados[codigo]
        salvar_dados(arquivo, dados)

def main():
    # Dicionário que mapeia as opções do menu principal para os arquivos e campos correspondentes
    # Dessa forma podemos ter funções genéricas para manipular qualquer base de dados
    # Temos aqui o nome do arquivo da base de dados; O título a ser mostrado no menu de operações; e os campos a serem requisitados ao usuário
    arquivos = {
        1: ('estudantes.json', 'ESTUDANTES', ['Código do estudante', 'Nome do estudante', 'CPF do estudante']),
        2: ('professores.json', 'PROFESSORES', ['Código do professor', 'Nome do professor', 'CPF do professor']),
        3: ('disciplinas.json', 'DISCIPLINAS', ['Código da disciplina', 'Nome da disciplina']),
        4: ('turmas.json', 'TURMAS', ['Código da turma', 'Código do professor', 'Código da disciplina']),
        5: ('matriculas.json', 'MATRÍCULAS', ['Código da matrícula', 'Código da turma', 'Código do estudante'])
    }

    # 'validacoes' necessário para a validação de Turma e Matrícula
    # Em '4' temos as validações da Turma e em '5' as da Matrícula
    # Em seguida temos os arquivos onde serão procurados os dados da validação
    # Por último temos a mensagem de erro a ser mostrada
    validacoes = {
        4: {
            'Código do professor': ('professores.json', 'Professor não encontrado!'),
            'Código da disciplina': ('disciplinas.json', 'Disciplina não encontrada!')
        },
        5: {
            'Código da turma': ('turmas.json', 'Turma não encontrada!'),
            'Código do estudante': ('estudantes.json', 'Estudante não encontrado!')
        }
    }

    while True:
        opcao_principal = menu_principal()

        if opcao_principal == 0:
            finalizar_programa()

        if opcao_principal not in arquivos:
            print('Opção inválida!')
            espera()
            continue

        # Carrega as informações referente a base de dados selecionada
        arquivo, titulo, campos = arquivos[opcao_principal]
        # Necessário para a validação de Turma e Matrícula
        validacoes_campos = validacoes.get(opcao_principal)

        while True:
            opcao_operacao = menu_operacoes(titulo)

            if opcao_operacao == 0:
                break
            elif opcao_operacao == 1:
                criar_registro(arquivo, campos, validacoes_campos)
            elif opcao_operacao == 2:
                alterar_registro(arquivo, campos, validacoes_campos)
            elif opcao_operacao == 3:
                excluir_registro(arquivo, campos[0])
            elif opcao_operacao == 4:
                listar_registros(arquivo, titulo)
            else:
                print('Opção inválida!')
                espera()

main()
