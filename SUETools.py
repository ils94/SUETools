import subprocess
import time

numero_usb = 0
opcao = ""

array = []


def selecionar_modo():
    global opcao

    subprocess.run("cls", shell=True)

    opcao = input("Pressione 1 para copiar arquivos para as mídias\n"
                  "Pressione 2 para formatar as mídias\n\nOpção: ")

    subprocess.run("cls", shell=True)

    numero_de_midias()


def numero_de_midias():
    global numero_usb
    global opcao

    numero_usb = input("Entre a quantidade de mídias que serão utilizadas durante a operação: ")

    if opcao == "1":
        subprocess.run("cls", shell=True)
        copiar_para_midia()
    else:
        subprocess.run("cls", shell=True)
        formatar_midia()


def formatar_midia():
    global array
    global numero_usb

    array.clear()

    while True:

        result = str(
            subprocess.check_output("wmic logicaldisk where drivetype=2 get DeviceID", text=True,
                                    stderr=subprocess.DEVNULL)).replace(
            "\r", "").replace("\n", "").replace("DeviceID  ", "").replace(":        ", "|")

        if str(result) != "":
            array = result.split("|")
            array.remove("")

            time.sleep(1)
            subprocess.run("cls", shell=True)
            print("Modo selecionado: Formatar mídias\n\n")
            print("Insira as mídias, " + str(numero_usb) + " no total.\n")
            print("Número de mídias inseridas: " + str(len(array)) + "\n")
            print(str(array) + "\n")

            if len(array) != int(numero_usb):
                array.clear()
            else:
                break
        elif str(result) == "":
            time.sleep(1)
            subprocess.run("cls", shell=True)
            print("Modo selecionado: Formatar mídias\n\n")
            print("Insira as mídias, " + str(numero_usb) + " no total.\n")
            print("Número de mídias inseridas: " + str(len(array)) + "\n")
            print(str(array) + "\n")

    for usb in array:
        result = subprocess.run("format /q /x /y " + usb + ":", shell=True, stdout=subprocess.DEVNULL,
                                stderr=subprocess.STDOUT)
        if str(result.returncode) == "0":
            print("Unidade " + usb + " Formatada com sucesso.")
        else:
            print("Unidade " + usb + " Formatação falhou.")

    print("\nRemova todas as Mídias")

    while True:
        result = str(subprocess.check_output("wmic logicaldisk where drivetype=2 get DeviceID", text=True,
                                             stderr=subprocess.DEVNULL)).replace(
            "\r", "").replace("\n", "").replace("DeviceID  ", "").replace(":        ", "")
        if result == "":
            break

    formatar_midia()


def copiar_para_midia():
    global array
    global numero_usb

    array.clear()

    while True:
        result = str(
            subprocess.check_output("wmic logicaldisk where drivetype=2 get DeviceID", text=True,
                                    stderr=subprocess.DEVNULL)).replace(
            "\r", "").replace("\n", "").replace("DeviceID  ", "").replace(":        ", "|")

        if str(result) != "":
            array = result.split("|")
            array.remove("")
            time.sleep(1)
            subprocess.run("cls", shell=True)
            print("Modo selecionado: Copiar arquivos para mídias\n\n")
            print("Insira as mídias, " + str(numero_usb) + " no total.\n")
            print("Número de mídias inseridas: " + str(len(array)) + "\n")
            print(str(array) + "\n")
            if len(array) != int(numero_usb):
                array.clear()
            else:
                break
        elif str(result) == "":
            time.sleep(1)
            subprocess.run("cls", shell=True)
            print("Modo selecionado: Copiar arquivos para mídias\n\n")
            print("Insira as mídias, " + str(numero_usb) + " no total.\n")
            print("Número de mídias inseridas: " + str(len(array)) + "\n")
            print(str(array) + "\n")

    for midia in array:
        result = subprocess.run("robocopy C:/copia " + midia + ":", shell=True, stdout=subprocess.DEVNULL,
                                stderr=subprocess.STDOUT)
        if str(result.returncode) == "1" or "2" or "3":
            print("Os arquivos foram copiados com sucesso para: " + midia)
        elif str(result.returncode) == "0":
            print("Nenhum erro ocorreu e nenhuma cópia foi feita. "
                  "As árvores de diretório de origem e destino são completamente sincronizadas em: " + midia)
        elif str(result.returncode) == "4":
            print("Alguns arquivos ou diretórios incompatíveis foram detectados em: " + midia)
        elif str(result.returncode) == "5":
            print(
                "Alguns arquivos foram copiados. Alguns arquivos foram incompatíveis. Nenhuma falha foi encontrada em: " + midia)
        elif str(result.returncode) == "6":
            print(
                "Existem arquivos adicionais e arquivos incompatíveis. Nenhum arquivo foi copiado e nenhuma falha foi encontrada. Isso significa que os arquivos já existem no diretório de destino em: " + midia)
        elif str(result.returncode) == "7":
            print(
                "Os arquivos foram copiados, uma incompatibilidade de arquivo estava presente e arquivos adicionais estavam presentes em: " + midia)
        elif str(result.returncode) == "8":
            print(
                "Alguns arquivos ou diretórios não puderam ser copiados (ocorreram erros de cópia e o limite de repetição foi excedido) em: " + midia)
        elif str(result.returncode) == "16":
            print(
                "Erro grave. Robocopy não copiou nenhum arquivo. Um erro de uso ou um erro devido a privilégios de acesso insuficientes nos diretórios de origem ou destino em: " + midia)

    print("\nRemova todas as Mídias")

    while True:
        result = str(subprocess.check_output("wmic logicaldisk where drivetype=2 get DeviceID", text=True,
                                             stderr=subprocess.DEVNULL)).replace(
            "\r", "").replace("\n", "").replace("DeviceID  ", "").replace(":        ", "")
        if result == "":
            break

    copiar_para_midia()


selecionar_modo()
