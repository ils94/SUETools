import subprocess
import time
import os

numero_midias = 0
opcao = ""
copiar_de = ""

lista_de_dispositivos = []


def mensagens_formatar():
    global lista_de_dispositivos

    time.sleep(1)
    subprocess.run("cls", shell=True)
    print("Modo selecionado: Formatar mídias.")
    print("\nInsira as mídias, " + str(numero_midias) + " no total.")
    print("\nNúmero de mídias inseridas: " + str(len(lista_de_dispositivos)) + ".")
    print("\n" + str(lista_de_dispositivos))
    print("\nAguardando a inserção de todas as mídias nas portas USBs.")


def mensagens_copiar():
    global lista_de_dispositivos

    time.sleep(1)
    subprocess.run("cls", shell=True)
    print("Modo selecionado: Copiar arquivos para as mídias.")
    print("\nInsira as mídias, " + str(numero_midias) + " no total.")
    print("\nNúmero de mídias inseridas: " + str(len(lista_de_dispositivos)) + ".")
    print("\n" + str(lista_de_dispositivos))
    print("\nAguardando a inserção de todas as mídias nas portas USBs.")


def mensagens_concluido():
    print("\nOperação concluída.")
    print("\nRemova todas as mídias das portas USBs.")


def formatar(lista):
    for midia in lista:
        dir = os.listdir(midia + ":/")

        dir.remove("System Volume Information")

        if len(dir) == 0:
            print("Unidade " + midia + " já foi formatada. Ignorando...")
        else:
            result = subprocess.run("format /q /x /y " + midia + ":", shell=True, stdout=subprocess.DEVNULL,
                                    stderr=subprocess.STDOUT)

            if str(result.returncode) == "0":
                print("Unidade " + midia + " formatada com sucesso.")
            else:
                print("Ocorreu um erro ao tentar formatar a unidade: " + midia + ".")


def copiar(lista):
    global copiar_de

    for midia in lista:
        result = subprocess.run("robocopy " + str(copiar_de) + " " + midia + ":", shell=True, stdout=subprocess.DEVNULL,
                                stderr=subprocess.STDOUT)
        if str(result.returncode) == "0":
            print("Nenhum erro ocorreu e nenhuma cópia foi feita. "
                  "As árvores de diretório de origem e destino são completamente sincronizadas em: " + midia + ".\n")
        if str(result.returncode) == "1":
            print("Os arquivos foram copiados com sucesso para: " + midia + ".\n")
        if str(result.returncode) == "2":
            print("Os arquivos foram copiados com sucesso para: " + midia + ".\n")
        if str(result.returncode) == "3":
            print("Os arquivos foram copiados com sucesso para: " + midia + ".\n")
        if str(result.returncode) == "4":
            print("Alguns arquivos ou diretórios incompatíveis foram detectados em: " + midia + ".\n")
        if str(result.returncode) == "5":
            print(
                "Alguns arquivos foram copiados. Alguns arquivos foram incompatíveis. Nenhuma falha foi encontrada em: " + midia + ".\n")
        if str(result.returncode) == "6":
            print(
                "Existem arquivos adicionais e arquivos incompatíveis. Nenhum arquivo foi copiado e nenhuma falha foi encontrada. Isso significa que os arquivos já existem no diretório de destino em: " + midia + ".\n")
        if str(result.returncode) == "7":
            print(
                "Os arquivos foram copiados, uma incompatibilidade de arquivo estava presente e arquivos adicionais estavam presentes em: " + midia + ".\n")
        if str(result.returncode) == "8":
            print(
                "Alguns arquivos ou diretórios não puderam ser copiados (ocorreram erros de cópia e o limite de repetição foi excedido) em: " + midia + ".\n")
        if str(result.returncode) == "16":
            print(
                "Erro grave. Robocopy não copiou nenhum arquivo. Um erro de uso ou um erro devido a privilégios de acesso insuficientes nos diretórios de origem ou destino em: " + midia + ".\n")


def listar_dispositivos():
    result = str(
        subprocess.check_output("wmic logicaldisk where drivetype=2 get DeviceID", text=True,
                                stderr=subprocess.DEVNULL)).replace(
        "\r", "").replace("\n", "").replace("DeviceID  ", "").replace(":        ", "|")

    return result


def selecionar_modo():
    global opcao

    subprocess.run("cls", shell=True)

    opcao = input("Pressione 1 para copiar arquivos para as mídias"
                  "\nPressione 2 para formatar as mídias\n\nOpção: ")

    subprocess.run("cls", shell=True)

    numero_de_midias()


def numero_de_midias():
    global numero_midias
    global opcao

    numero_midias = input("Entre a quantidade de mídias que serão utilizadas durante a operação: ")

    try:
        int(numero_midias)
    except ValueError:
        subprocess.run("cls", shell=True)
        print("Apenas números inteiros são permitidos.\n")
        numero_de_midias()

    if opcao == "1":
        subprocess.run("cls", shell=True)
        diretorio_copia()
    else:
        subprocess.run("cls", shell=True)
        formatar_midia()


def diretorio_copia():
    global copiar_de

    copiar_de = input("Insira o diretório com os arquivos que serão copiados: ")

    if os.path.isdir(str(copiar_de)):
        copiar_para_midia()
    else:
        subprocess.run("cls", shell=True)
        print("Diretório não existe.\n")
        diretorio_copia()


def formatar_midia():
    global lista_de_dispositivos
    global numero_midias

    lista_de_dispositivos.clear()

    while True:

        result = listar_dispositivos()

        if str(result) != "":
            lista_de_dispositivos = result.split("|")
            lista_de_dispositivos.remove("")

            mensagens_formatar()

            if len(lista_de_dispositivos) != int(numero_midias):
                lista_de_dispositivos.clear()
            else:
                break
        elif str(result) == "":
            mensagens_formatar()

    subprocess.run("cls", shell=True)
    print("Iniciando formatação. Não remova as mídias durante o processo...\n")

    formatar(lista_de_dispositivos)

    mensagens_concluido()

    while True:
        if listar_dispositivos() == "":
            break

    formatar_midia()


def copiar_para_midia():
    global lista_de_dispositivos
    global numero_midias

    lista_de_dispositivos.clear()

    while True:
        result = listar_dispositivos()

        if str(result) != "":

            lista_de_dispositivos = result.split("|")
            lista_de_dispositivos.remove("")

            mensagens_copiar()

            if len(lista_de_dispositivos) != int(numero_midias):
                lista_de_dispositivos.clear()
            else:
                break
        elif str(result) == "":

            mensagens_copiar()

    subprocess.run("cls", shell=True)
    print("Formatando a mídia por precaução. Não remova as mídias durante o processo...\n")

    formatar(lista_de_dispositivos)

    print("\nIniciando copia. Não remova as mídias durante o processo...\n")

    copiar(lista_de_dispositivos)

    mensagens_concluido()

    while True:
        if listar_dispositivos() == "":
            break

    copiar_para_midia()


selecionar_modo()
