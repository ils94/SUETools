import subprocess
import time
import os
import keyboard
from playsound import playsound

numero_mrs = 0
opcao = ""
copiar_de = ""
drivetype = ""

lista_de_dispositivos = []
lista_arquivos = []
erro_critico = None
erro_lista = []


class BColors:
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'


def mensagens_formatar_mr():
    global lista_de_dispositivos

    time.sleep(1)
    subprocess.run("cls", shell=True)
    print("Modo selecionado: Formatar MRs.")
    print('\nSegure "ESC" para cancelar a operação, e voltar ao Menu Inicial.')
    print('\nSegure "F" para forçar a operação.')
    print("\nInsira as MRs, " + str(numero_mrs) + " no total.")
    print("\nNúmero de MRs inseridas: " + str(len(lista_de_dispositivos)) + ".")
    print("\n" + str(lista_de_dispositivos))
    print(f"{BColors.WARNING}\nAguardando a inserção de todas as MRs nas portas USBs." + BColors.ENDC)


def mensagens_copiar_mr():
    global lista_de_dispositivos
    global copiar_de
    global lista_arquivos

    time.sleep(1)
    subprocess.run("cls", shell=True)
    print("Modo selecionado: Copiar arquivos para as MRs.")
    print('\nSegure "ESC" para cancelar a operação, e voltar ao Menu Inicial.')
    print('\nSegure "F" para forçar a operação.')
    print(f"{BColors.WARNING}\nDiretório de origem dos arquivos copiados: " + copiar_de + BColors.ENDC)
    print(f"{BColors.WARNING}\nUm total de " + str(
        len(lista_arquivos)) + " arquivos serão copiados para as MRs." + BColors.ENDC)
    print("\nLista de arquivos que serão copiados:")
    print("\n" + str(lista_arquivos))
    print("\nInsira as MRs, " + str(numero_mrs) + " no total.")
    print("\nNúmero de MRs inseridas: " + str(len(lista_de_dispositivos)) + ".")
    print("\n" + str(lista_de_dispositivos))
    print(f"{BColors.WARNING}\nAguardando a inserção de todas as MRs nas portas USBs." + BColors.ENDC)


def mensagens_formatar_fmc():
    time.sleep(1)
    subprocess.run("cls", shell=True)
    print("Modo selecionado: Formatar Flash Memory Card.")
    print('\nSegure "ESC" para cancelar a operação, e voltar ao Menu Inicial.')
    print(f"{BColors.WARNING}\nAguardando a inserção do Flash Memory Card." + BColors.ENDC)


def formatar(lista_de_mrs):
    global lista_de_dispositivos
    global opcao
    global erro_critico
    global erro_lista

    erro_critico = False
    erro_lista.clear()

    for mr in lista_de_mrs:
        try:
            dir = os.listdir(mr + ":/")

            if "System Volume Information" in dir:
                dir.remove("System Volume Information")

            if len(dir) == 0:
                print(f"{BColors.WARNING}Unidade " + mr + " já foi formatada. Ignorando..." + BColors.ENDC)
            else:
                result = subprocess.run("format /q /x /y " + mr + ":", shell=True, stdout=subprocess.DEVNULL,
                                        stderr=subprocess.STDOUT)

                if str(result.returncode) == "0":
                    print(f"{BColors.OKBLUE}Unidade " + mr + " formatada com sucesso." + BColors.ENDC)
                else:
                    print(f"{BColors.FAIL}Ocorreu um erro ao tentar formatar a unidade: " + mr + "." + BColors.ENDC)
        except Exception as e:
            print(str(f"{BColors.FAIL} " + str(e) + BColors.ENDC))
            erro_critico = True
            erro_lista.append(mr)
            continue

    if erro_critico and opcao == "1":
        for e in erro_lista:
            lista_de_dispositivos.remove(e)


def copiar(lista):
    global copiar_de

    for mrs in lista:
        result = subprocess.run("robocopy " + str(copiar_de) + " " + mrs + ":", shell=True,
                                stdout=subprocess.DEVNULL,
                                stderr=subprocess.STDOUT)
        if str(result.returncode) == "0":
            print(f"{BColors.WARNING}Nenhum erro ocorreu e nenhuma cópia foi feita. "
                  "As árvores de diretório de origem e destino são completamente sincronizadas em: " + mrs + "." + BColors.ENDC)
        if str(result.returncode) == "1":
            print(f"{BColors.OKBLUE}Os arquivos foram copiados com sucesso para: " + mrs + "." + BColors.ENDC)
        if str(result.returncode) == "2":
            print(f"{BColors.OKBLUE}Os arquivos foram copiados com sucesso para: " + mrs + "." + BColors.ENDC)
        if str(result.returncode) == "3":
            print(f"{BColors.OKBLUE}Os arquivos foram copiados com sucesso para: " + mrs + "." + BColors.ENDC)
        if str(result.returncode) == "4":
            print(
                f"{BColors.WARNING}Alguns arquivos ou diretórios incompatíveis foram detectados em: " + mrs + "." + BColors.ENDC)
        if str(result.returncode) == "5":
            print(
                f"{BColors.WARNING}Alguns arquivos foram copiados. Alguns arquivos foram incompatíveis. Nenhuma falha foi encontrada em: " + mrs + "." + BColors.ENDC)
        if str(result.returncode) == "6":
            print(
                f"{BColors.WARNING}Existem arquivos adicionais e arquivos incompatíveis. Nenhum arquivo foi copiado e nenhuma falha foi encontrada. Isso significa que os arquivos já existem no diretório de destino em: " + mrs + "." + BColors.ENDC)
        if str(result.returncode) == "7":
            print(
                f"{BColors.WARNING}Os arquivos foram copiados, uma incompatibilidade de arquivo estava presente e arquivos adicionais estavam presentes em: " + mrs + "." + BColors.ENDC)
        if str(result.returncode) == "8":
            print(
                f"{BColors.FAIL}Alguns arquivos ou diretórios não puderam ser copiados (ocorreram erros de cópia e o limite de repetição foi excedido) em: " + mrs + "." + BColors.ENDC)
        if str(result.returncode) == "16":
            print(
                f"{BColors.FAIL}Erro grave. Robocopy não copiou nenhum arquivo. Um erro de uso ou um erro devido a privilégios de acesso insuficientes nos diretórios de origem ou destino em: " + mrs + "." + BColors.ENDC)

        dir = []

        if os.path.isdir(mrs + ":/"):
            for file in os.listdir(mrs + ":/"):
                if os.path.isfile(os.path.join(mrs + ":/", file)):
                    dir.append(file)

        print(f"{BColors.WARNING}Um total de " + str(len(dir)) + " arquivos foram copiados.\n" + BColors.ENDC)


def listar_dispositivos():
    global drivetype

    result = str(
        subprocess.check_output("wmic logicaldisk where drivetype=" + drivetype + " get DeviceID", text=True,
                                stderr=subprocess.DEVNULL)).replace(
        "\r", "").replace("\n", "").replace("DeviceID  ", "").replace(":        ", "|")

    if drivetype == "3":
        result = result.replace("C", "").replace("D", "").replace("|", "")
        return result
    if drivetype == "2":
        return result


def selecionar_modo():
    global opcao
    global lista_arquivos
    global drivetype

    lista_arquivos.clear()

    subprocess.run("cls", shell=True)

    opcao = input('Digite "1" para copiar arquivos para as MRs.'
                  '\nDigite "2" para formatar as MRs.'
                  '\nDigite "3" para formatar um Flash Memory Card.\n\nOpção: ')

    subprocess.run("cls", shell=True)

    if opcao == "1":
        print("Copiar arquivos para as MRs.\n")
        drivetype = "2"
        numero_de_mrs()
    if opcao == "2":
        print("Formatar MRs.\n")
        drivetype = "2"
        numero_de_mrs()
    if opcao == "3":
        drivetype = "3"
        formatar_fmc()
    else:
        selecionar_modo()


def numero_de_mrs():
    global numero_mrs
    global opcao

    print('Digite "menu" para voltar ao Menu Inicial.\n')

    numero_mrs = input("Entre a quantidade de MRs que serão utilizadas durante a operação: ")

    if numero_mrs == "menu":
        selecionar_modo()
    else:
        try:
            int(numero_mrs)
        except ValueError:
            subprocess.run("cls", shell=True)
            print(f"{BColors.FAIL}Apenas números inteiros são permitidos.\n" + BColors.ENDC)
            numero_de_mrs()

        if opcao == "1":
            subprocess.run("cls", shell=True)
            diretorio_copia()
        if opcao == "2":
            subprocess.run("cls", shell=True)
            formatar_mrs()


def diretorio_copia():
    global copiar_de

    print('Digite "voltar" para voltar a etapa de quantidade de MRs para a operação.\n')
    print('Digite "menu" para voltar ao Menu Inicial.\n')

    copiar_de = input("Insira o diretório com os arquivos que serão copiados: ")

    if copiar_de == "voltar":
        subprocess.run("cls", shell=True)
        numero_de_mrs()
    elif copiar_de == "menu":
        subprocess.run("cls", shell=True)
        selecionar_modo()
    else:
        if os.path.isdir(copiar_de):
            for file in os.listdir(copiar_de):
                if os.path.isfile(os.path.join(copiar_de, file)):
                    lista_arquivos.append(file)

            copiar_para_mrs()
        else:
            subprocess.run("cls", shell=True)
            print(f'{BColors.FAIL}Diretório "' + copiar_de + '" não existe.\n' + BColors.ENDC)
            diretorio_copia()


def formatar_mrs():
    usb_watcher(mensagens_formatar_mr)

    subprocess.run("cls", shell=True)
    print(f"{BColors.WARNING}Iniciando formatação. Não remova as MRs durante o processo...\n" + BColors.ENDC)

    formatar(lista_de_dispositivos)

    print(f"{BColors.OKGREEN}\nOperação concluída." + BColors.ENDC)
    print(f"{BColors.OKGREEN}\nRemova todas as MRs das portas USBs." + BColors.ENDC)
    print(f'{BColors.OKGREEN}\nSegure "K" para formatar novamente.' + BColors.ENDC)
    print(f'{BColors.OKGREEN}\nSegure "ESC" para voltar ao Menu Inicial.' + BColors.ENDC)

    alerta()

    while True:
        if listar_dispositivos() == "":
            break
        elif keyboard.is_pressed("K"):
            break
        elif keyboard.is_pressed("ESC"):
            break

    formatar_mrs()


def copiar_para_mrs():
    global erro_lista
    global erro_critico

    usb_watcher(mensagens_copiar_mr)

    subprocess.run("cls", shell=True)
    print(
        f"{BColors.WARNING}Formatando as MRs por precaução. Não remova as MRs durante o processo...\n" + BColors.ENDC)

    formatar(lista_de_dispositivos)

    if len(lista_de_dispositivos) > 0:

        print(f"{BColors.WARNING}\nIniciando copia. Não remova as MRs durante o processo...\n" + BColors.ENDC)

        copiar(lista_de_dispositivos)

        if erro_critico:
            print(f"{BColors.FAIL}Não foi possível copiar os arquivos para algumas MRs:" + BColors.ENDC)
            print(f"{BColors.FAIL}\n" + str(erro_lista) + "\n" + BColors.ENDC)

    else:
        print(f"{BColors.FAIL}\nNão foi possível copiar os arquivos para as MRs.\n" + BColors.ENDC)

    print(f"{BColors.OKGREEN}Operação concluída." + BColors.ENDC)
    print(f"{BColors.OKGREEN}\nRemova todas as MRs das portas USBs." + BColors.ENDC)
    print(f'{BColors.OKGREEN}\nSegure "K" para copiar novamente.' + BColors.ENDC)
    print(f'{BColors.OKGREEN}\nSegure "ESC" para voltar ao Menu Inicial.' + BColors.ENDC)

    alerta()

    while True:
        if listar_dispositivos() == "":
            break
        elif keyboard.is_pressed("K"):
            break
        elif keyboard.is_pressed("ESC"):
            break

    copiar_para_mrs()


def formatar_fmc():
    global lista_de_dispositivos

    lista_de_dispositivos.clear()

    while True:

        if keyboard.is_pressed("Esc"):
            selecionar_modo()

        result = listar_dispositivos()

        if str(result) != "":
            lista_de_dispositivos.append(result)

            mensagens_formatar_fmc()

            if len(lista_de_dispositivos) != 1:
                lista_de_dispositivos.clear()
            else:
                break
        elif str(result) == "":
            mensagens_formatar_fmc()

    subprocess.run("cls", shell=True)
    print(
        f"{BColors.WARNING}Iniciando formatação. Não remova o Flash Memory Card durante o processo...\n" + BColors.ENDC)

    formatar(lista_de_dispositivos)

    print(f"{BColors.OKGREEN}\nOperação concluída." + BColors.ENDC)
    print(f"{BColors.OKGREEN}\nRemova o Flash Memory Card." + BColors.ENDC)

    alerta()

    while True:
        if listar_dispositivos() == "":
            break

    formatar_fmc()


def usb_watcher(mensagens):
    global lista_de_dispositivos
    global numero_mrs

    lista_de_dispositivos.clear()

    while True:

        if keyboard.is_pressed("Esc"):
            selecionar_modo()

        result = listar_dispositivos()

        if str(result) != "":
            lista_de_dispositivos = result.split("|")
            lista_de_dispositivos.remove("")

            mensagens()

            if keyboard.is_pressed("F"):
                break

            if len(lista_de_dispositivos) < int(numero_mrs):
                lista_de_dispositivos.clear()
            else:
                break
        elif str(result) == "":
            mensagens()


def alerta():
    playsound("audios/oc.mp3")


selecionar_modo()
