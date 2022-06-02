import subprocess
import time
import os
import keyboard

numero_midias = 0
opcao = ""
copiar_de = ""

lista_de_dispositivos = []
lista_arquivos = []


class BColors:
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'


def mensagens_formatar():
    global lista_de_dispositivos

    time.sleep(1)
    subprocess.run("cls", shell=True)
    print("Modo selecionado: Formatar mídias.")
    print("\nSegure ESC para voltar ao menu inicial.")
    print("\nInsira as mídias, " + str(numero_midias) + " no total.")
    print("\nNúmero de mídias inseridas: " + str(len(lista_de_dispositivos)) + ".")
    print("\n" + str(lista_de_dispositivos))
    print(f"{BColors.WARNING}\nAguardando a inserção de todas as mídias nas portas USBs." + BColors.ENDC)


def mensagens_copiar():
    global lista_de_dispositivos
    global copiar_de
    global lista_arquivos

    time.sleep(1)
    subprocess.run("cls", shell=True)
    print("Modo selecionado: Copiar arquivos para as mídias.")
    print("\nSegure ESC para voltar ao menu inicial.")
    print(f"{BColors.WARNING}\nDiretório de origem dos arquivos copiados: " + copiar_de + BColors.ENDC)
    print(f"{BColors.WARNING}\nUm total de " + str(
        len(lista_arquivos)) + " arquivos serão copiados para as mídias." + BColors.ENDC)
    print("\nLista de arquivos que serão copiados:")
    print("\n" + str(lista_arquivos))
    print("\nInsira as mídias, " + str(numero_midias) + " no total.")
    print("\nNúmero de mídias inseridas: " + str(len(lista_de_dispositivos)) + ".")
    print("\n" + str(lista_de_dispositivos))
    print(f"{BColors.WARNING}\nAguardando a inserção de todas as mídias nas portas USBs." + BColors.ENDC)


def formatar(lista):
    for midia in lista:
        dir = []

        for file in os.listdir(midia + ":/"):
            if os.path.isfile(os.path.join(midia + ":/", file)):
                dir.append(file)

        if len(dir) == 0:
            print(f"{BColors.WARNING}Unidade " + midia + " já foi formatada. Ignorando..." + BColors.ENDC)
        else:
            result = subprocess.run("format /q /x /y " + midia + ":", shell=True, stdout=subprocess.DEVNULL,
                                    stderr=subprocess.STDOUT)

            if str(result.returncode) == "0":
                print(f"{BColors.OKBLUE}Unidade " + midia + " formatada com sucesso." + BColors.ENDC)
            else:
                print(f"{BColors.FAIL}Ocorreu um erro ao tentar formatar a unidade: " + midia + "." + BColors.ENDC)


def copiar(lista):
    global copiar_de

    for midia in lista:
        result = subprocess.run("robocopy " + str(copiar_de) + " " + midia + ":", shell=True, stdout=subprocess.DEVNULL,
                                stderr=subprocess.STDOUT)
        if str(result.returncode) == "0":
            print(f"{BColors.WARNING}Nenhum erro ocorreu e nenhuma cópia foi feita. "
                  "As árvores de diretório de origem e destino são completamente sincronizadas em: " + midia + "." + BColors.ENDC)
        if str(result.returncode) == "1":
            print(f"{BColors.OKBLUE}Os arquivos foram copiados com sucesso para: " + midia + "." + BColors.ENDC)
        if str(result.returncode) == "2":
            print(f"{BColors.OKBLUE}Os arquivos foram copiados com sucesso para: " + midia + "." + BColors.ENDC)
        if str(result.returncode) == "3":
            print(f"{BColors.OKBLUE}Os arquivos foram copiados com sucesso para: " + midia + "." + BColors.ENDC)
        if str(result.returncode) == "4":
            print(
                f"{BColors.WARNING}Alguns arquivos ou diretórios incompatíveis foram detectados em: " + midia + "." + BColors.ENDC)
        if str(result.returncode) == "5":
            print(
                f"{BColors.WARNING}Alguns arquivos foram copiados. Alguns arquivos foram incompatíveis. Nenhuma falha foi encontrada em: " + midia + "." + BColors.ENDC)
        if str(result.returncode) == "6":
            print(
                f"{BColors.WARNING}Existem arquivos adicionais e arquivos incompatíveis. Nenhum arquivo foi copiado e nenhuma falha foi encontrada. Isso significa que os arquivos já existem no diretório de destino em: " + midia + "." + BColors.ENDC)
        if str(result.returncode) == "7":
            print(
                f"{BColors.WARNING}Os arquivos foram copiados, uma incompatibilidade de arquivo estava presente e arquivos adicionais estavam presentes em: " + midia + "." + BColors.ENDC)
        if str(result.returncode) == "8":
            print(
                f"{BColors.FAIL}Alguns arquivos ou diretórios não puderam ser copiados (ocorreram erros de cópia e o limite de repetição foi excedido) em: " + midia + "." + BColors.ENDC)
        if str(result.returncode) == "16":
            print(
                f"{BColors.FAIL}Erro grave. Robocopy não copiou nenhum arquivo. Um erro de uso ou um erro devido a privilégios de acesso insuficientes nos diretórios de origem ou destino em: " + midia + "." + BColors.ENDC)

        dir = []

        if os.path.isdir(midia + ":/"):
            for file in os.listdir(midia + ":/"):
                if os.path.isfile(os.path.join(midia + ":/", file)):
                    dir.append(file)

        print(f"{BColors.WARNING}Um total de " + str(len(dir)) + " arquivos foram copiados.\n" + BColors.ENDC)


def listar_dispositivos():
    result = str(
        subprocess.check_output("wmic logicaldisk where drivetype=2 get DeviceID", text=True,
                                stderr=subprocess.DEVNULL)).replace(
        "\r", "").replace("\n", "").replace("DeviceID  ", "").replace(":        ", "|")

    return result


def selecionar_modo():
    global opcao
    global lista_arquivos

    lista_arquivos.clear()

    subprocess.run("cls", shell=True)

    opcao = input("Pressione 1 para copiar arquivos para as mídias"
                  "\nPressione 2 para formatar as mídias\n\nOpção: ")

    subprocess.run("cls", shell=True)

    if opcao == "1":
        print("Copiar arquivos para as mídias.\n")
    else:
        print("Formatar mídias.\n")

    numero_de_midias()


def numero_de_midias():
    global numero_midias
    global opcao

    print("Para voltar ao menu inicial, digite ''voltar''.\n")

    numero_midias = input("Entre a quantidade de mídias que serão utilizadas durante a operação: ")

    if numero_midias == "voltar":
        selecionar_modo()
    else:
        try:
            int(numero_midias)
        except ValueError:
            subprocess.run("cls", shell=True)
            print(f"{BColors.FAIL}Apenas números inteiros são permitidos.\n" + BColors.ENDC)
            numero_de_midias()

        if opcao == "1":
            subprocess.run("cls", shell=True)
            diretorio_copia()
        else:
            subprocess.run("cls", shell=True)
            formatar_midia()


def diretorio_copia():
    global copiar_de

    print("Para voltar ao menu inicial, digite ''voltar''.\n")

    copiar_de = input("Insira o diretório com os arquivos que serão copiados: ")

    if copiar_de == "voltar":
        selecionar_modo()
    else:
        if os.path.isdir(copiar_de):
            for file in os.listdir(copiar_de):
                if os.path.isfile(os.path.join(copiar_de, file)):
                    lista_arquivos.append(file)

            copiar_para_midia()
        else:
            subprocess.run("cls", shell=True)
            print(f"{BColors.FAIL}Diretório não existe.\n" + BColors.ENDC)
            diretorio_copia()


def formatar_midia():
    global lista_de_dispositivos
    global numero_midias

    lista_de_dispositivos.clear()

    while True:

        if keyboard.is_pressed("Esc"):
            selecionar_modo()

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
    print(f"{BColors.WARNING}Iniciando formatação. Não remova as mídias durante o processo...\n" + BColors.ENDC)

    formatar(lista_de_dispositivos)

    print(f"{BColors.OKGREEN}\nOperação concluída." + BColors.ENDC)
    print(f"{BColors.OKGREEN}\nRemova todas as mídias das portas USBs." + BColors.ENDC)

    while True:
        if listar_dispositivos() == "":
            break

    formatar_midia()


def copiar_para_midia():
    global lista_de_dispositivos
    global numero_midias

    lista_de_dispositivos.clear()

    while True:

        if keyboard.is_pressed("Esc"):
            selecionar_modo()

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
    print(
        f"{BColors.WARNING}Formatando a mídia por precaução. Não remova as mídias durante o processo...\n" + BColors.ENDC)

    formatar(lista_de_dispositivos)

    print(f"{BColors.WARNING}\nIniciando copia. Não remova as mídias durante o processo...\n" + BColors.ENDC)

    copiar(lista_de_dispositivos)

    print(f"{BColors.OKGREEN}Operação concluída." + BColors.ENDC)
    print(f"{BColors.OKGREEN}\nRemova todas as mídias das portas USBs." + BColors.ENDC)

    while True:
        if listar_dispositivos() == "":
            break

    copiar_para_midia()


selecionar_modo()
