import subprocess
import time
import os
import keyboard
import re
from playsound import playsound

numero_midias = 0
sleep = 0.1
opcao = ""
copiar_de = ""
drivetype = ""
tipo_de_formatacao = ""

lista_de_dispositivos = []
lista_arquivos = []
unidades_excluidas = []
erro_lista = []

erro_critico = None


class BColors:
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'


def mensagens_formatar_midias():
    global lista_de_dispositivos
    global tipo_de_formatacao

    time.sleep(sleep)
    subprocess.run("cls", shell=True)

    print("Modo selecionado: Formatar Mídias.")
    print("\nTipo de formatação: " + tipo_de_formatacao)
    print('\nSegure "ESC" para cancelar a operação, e voltar ao Menu Inicial.')
    print('\nSegure "F" para forçar a operação.')
    print("\nInsira as Mídias, " + str(numero_midias) + " no total.")
    print("\nNúmero de Mídias inseridas: " + str(len(lista_de_dispositivos)) + ".")
    print("\n" + str(lista_de_dispositivos))
    print(f"{BColors.WARNING}\nAguardando a inserção de todas as Mídias nas portas USBs." + BColors.ENDC)


def mensagens_copiar_midias():
    global lista_de_dispositivos
    global copiar_de
    global lista_arquivos
    global tipo_de_formatacao

    time.sleep(sleep)
    subprocess.run("cls", shell=True)

    print("Modo selecionado: Copiar arquivos para as Mídias.")
    print("\nTipo de formatação: " + tipo_de_formatacao)
    print('\nSegure "ESC" para cancelar a operação, e voltar ao Menu Inicial.')
    print('\nSegure "F" para forçar a operação.')
    print(f"{BColors.WARNING}\nDiretório de origem dos arquivos copiados: " + copiar_de + BColors.ENDC)
    print(f"{BColors.WARNING}\nUm total de " + str(
        len(lista_arquivos)) + " arquivos serão copiados para as Mídias." + BColors.ENDC)
    print("\nLista de arquivos que serão copiados:")
    print("\n" + str(lista_arquivos))
    print("\nInsira as Mídias, " + str(numero_midias) + " no total.")
    print("\nNúmero de Mídias inseridas: " + str(len(lista_de_dispositivos)) + ".")
    print("\n" + str(lista_de_dispositivos))
    print(f"{BColors.WARNING}\nAguardando a inserção de todas as Mídias nas portas USBs." + BColors.ENDC)


def mensagens_formatar_fmc():
    global unidades_excluidas

    time.sleep(sleep)
    subprocess.run("cls", shell=True)

    print("Modo selecionado: Formatar Flash Memory Card.")
    print("\nLista de unidades excluídas: " + str(unidades_excluidas))
    print('\nSegure "ESC" para cancelar a operação, e voltar ao Menu Inicial.')
    print(f"{BColors.WARNING}\nAguardando a inserção do Flash Memory Card." + BColors.ENDC)


def formatar(lista_de_midias):
    global lista_de_dispositivos
    global opcao
    global erro_critico
    global erro_lista
    global tipo_de_formatacao

    erro_critico = False
    erro_lista.clear()

    for midia in lista_de_midias:
        try:
            if tipo_de_formatacao == "normal":
                dir = os.listdir(midia + ":/")

                if "System Volume Information" in dir:
                    dir.remove("System Volume Information")
                if len(dir) == 0:
                    print(f"{BColors.WARNING}Unidade " + midia + " já foi formatada. Ignorando..." + BColors.ENDC)
                else:
                    subprocess_formatar(midia)
            else:
                subprocess_formatar(midia)
        except Exception as e:
            print(str(f"{BColors.FAIL} " + str(e) + BColors.ENDC))
            erro_critico = True
            erro_lista.append(midia)
            continue

    if erro_critico and opcao == "1":
        for e in erro_lista:
            lista_de_dispositivos.remove(e)


def copiar(lista):
    global copiar_de
    global erro_critico

    for midia in lista:
        result = subprocess.run("robocopy " + str(copiar_de) + " " + midia + ":", shell=True,
                                stdout=subprocess.DEVNULL,
                                stderr=subprocess.STDOUT)
        if str(result.returncode) == "1":
            print(f"{BColors.OKBLUE}Os arquivos foram copiados com sucesso para: " + midia + "." + BColors.ENDC)
        if str(result.returncode) == "2":
            print(f"{BColors.OKBLUE}Os arquivos foram copiados com sucesso para: " + midia + "." + BColors.ENDC)
        if str(result.returncode) == "3":
            print(f"{BColors.OKBLUE}Os arquivos foram copiados com sucesso para: " + midia + "." + BColors.ENDC)
        else:
            print(f"{BColors.FAIL}Ocorreu um erro ao copiar arquivos para: " + midia + "." + BColors.ENDC)
            erro_critico = True

        dir = []

        if os.path.isdir(midia + ":/"):
            for file in os.listdir(midia + ":/"):
                if os.path.isfile(os.path.join(midia + ":/", file)):
                    dir.append(file)

        print(f"{BColors.WARNING}Um total de " + str(len(dir)) + " arquivos foram copiados.\n" + BColors.ENDC)


def listar_dispositivos():
    global drivetype
    global unidades_excluidas

    result = str(
        subprocess.check_output("wmic logicaldisk where drivetype=" + drivetype + " get DeviceID", text=True,
                                stderr=subprocess.DEVNULL)).replace(
        "\r", "").replace("\n", "").replace("DeviceID  ", "").replace(":        ", "|")

    if drivetype == "3":
        for u in unidades_excluidas:
            result = result.replace(u, "")
        result = result.replace("C", "").replace("|", "")
        return result
    if drivetype == "2":
        return result


def selecionar_modo():
    global opcao
    global lista_arquivos
    global drivetype

    lista_arquivos.clear()

    subprocess.run("cls", shell=True)

    opcao = input('Digite "1" para copiar arquivos para as Mídias.'
                  '\nDigite "2" para formatar as Mídias.'
                  '\nDigite "3" para formatar um Flash Memory Card.\n\nOpção: ')

    subprocess.run("cls", shell=True)

    if opcao == "1":
        print("Copiar arquivos para as Mídias.\n")
        drivetype = "2"
        tipo_formatacao()
    if opcao == "2":
        print("Formatar Mídias.\n")
        drivetype = "2"
        tipo_formatacao()
    if opcao == "3":
        drivetype = "3"
        subprocess.run("cls", shell=True)
        excluir_unidades()
    else:
        selecionar_modo()


def tipo_formatacao():
    global tipo_de_formatacao

    subprocess.run("cls", shell=True)

    print('Digite "menu" para voltar ao Menu Inicial.\n'
          '\nDigite "n" para formatação normal (a unidade só será formatada se houver arquivos)'
          '\nDigite "f" para formatação forçada (a unidade será formatada mesmo se não houver arquivos)')

    opcao = input('\nopcão: ')

    subprocess.run("cls", shell=True)

    if opcao == "n":
        tipo_de_formatacao = "normal"
        numero_de_midias()
    if opcao == "f":
        tipo_de_formatacao = "forçada"
        numero_de_midias()
    if opcao == "menu":
        selecionar_modo()
    else:
        tipo_formatacao()


def numero_de_midias():
    global numero_midias
    global opcao

    print('Digite "menu" para voltar ao Menu Inicial.\n')
    print('Digite "voltar" para voltar a etapa de tipo de formatação.\n')

    numero_midias = input("Entre a quantidade de Mídias que serão utilizadas durante a operação: ")

    if numero_midias == "menu":
        selecionar_modo()
    if numero_midias == "voltar":
        tipo_formatacao()
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
        if opcao == "2":
            subprocess.run("cls", shell=True)
            formatar_midias()


def diretorio_copia():
    global copiar_de

    print('Digite "menu" para voltar ao Menu Inicial.\n')
    print('Digite "voltar" para voltar a etapa de quantidade de Mídias para a operação.\n')

    copiar_de = input("Insira o diretório com os arquivos que serão copiados: ")

    if copiar_de == "voltar":
        subprocess.run("cls", shell=True)
        numero_de_midias()
    elif copiar_de == "menu":
        subprocess.run("cls", shell=True)
        selecionar_modo()
    else:
        if os.path.isdir(copiar_de):
            for file in os.listdir(copiar_de):
                if os.path.isfile(os.path.join(copiar_de, file)):
                    lista_arquivos.append(file)
            copiar_para_midias()
        else:
            subprocess.run("cls", shell=True)
            print(f'{BColors.FAIL}Diretório "' + copiar_de + '" não existe.\n' + BColors.ENDC)
            diretorio_copia()


def formatar_midias():
    global erro_critico

    usb_watcher(mensagens_formatar_midias)

    subprocess.run("cls", shell=True)
    print(f"{BColors.WARNING}Iniciando formatação. Não remova as Mídias durante o processo...\n" + BColors.ENDC)

    alerta_operacao_iniciada()

    formatar(lista_de_dispositivos)

    print(f"{BColors.OKGREEN}\nOperação concluída." + BColors.ENDC)
    print(f"{BColors.OKGREEN}\nRemova todas as Mídias das portas USBs." + BColors.ENDC)
    print(f'{BColors.OKGREEN}\nSegure "K" para formatar novamente.' + BColors.ENDC)
    print(f'{BColors.OKGREEN}\nSegure "ESC" para voltar ao Menu Inicial.' + BColors.ENDC)

    if erro_critico:
        erros_encontrados()
    else:
        alerta_operacao_concluida()

    while True:
        if listar_dispositivos() == "":
            break
        elif keyboard.is_pressed("K"):
            break
        elif keyboard.is_pressed("ESC"):
            break

    formatar_midias()


def copiar_para_midias():
    global erro_lista
    global erro_critico

    usb_watcher(mensagens_copiar_midias)

    subprocess.run("cls", shell=True)
    print(
        f"{BColors.WARNING}Formatando as Mídias por precaução. Não remova as Mídias durante o processo...\n" + BColors.ENDC)

    alerta_operacao_iniciada()

    formatar(lista_de_dispositivos)

    if len(lista_de_dispositivos) > 0:

        print(f"{BColors.WARNING}\nIniciando copia. Não remova as Mídias durante o processo...\n" + BColors.ENDC)

        copiar(lista_de_dispositivos)

        if erro_critico:
            print(f"{BColors.FAIL}Não foi possível copiar os arquivos para algumas Mídias:" + BColors.ENDC)
            print(f"{BColors.FAIL}\n" + str(erro_lista) + "\n" + BColors.ENDC)

    else:
        print(f"{BColors.FAIL}\nNão foi possível copiar os arquivos para as Mídias.\n" + BColors.ENDC)

    print(f"{BColors.OKGREEN}Operação concluída." + BColors.ENDC)
    print(f"{BColors.OKGREEN}\nRemova todas as Mídias das portas USBs." + BColors.ENDC)
    print(f'{BColors.OKGREEN}\nSegure "K" para copiar novamente.' + BColors.ENDC)
    print(f'{BColors.OKGREEN}\nSegure "ESC" para voltar ao Menu Inicial.' + BColors.ENDC)

    if erro_critico:
        erros_encontrados()
    else:
        alerta_operacao_concluida()

    while True:
        if listar_dispositivos() == "":
            break
        elif keyboard.is_pressed("K"):
            break
        elif keyboard.is_pressed("ESC"):
            break

    copiar_para_midias()


def excluir_unidades():
    global unidades_excluidas

    print('Digite "menu" para voltar ao Menu Inicial.\n')

    unidades = input('A Flash Memory Card é considerada um disco fixo. Por isso, seja necessário excluir '
                     'as letras que representam as unidades desses tipos de discos, como "C".'
                     '\n\nPor padrão, a unidade "C" já está excluída nessa operação.'
                     '\n\nDigite a baixo as letras das unidades de discos fixos que você gostaria '
                     'de excluir para prevenir que o programa formate essas unidades.'
                     '\n\nDeixe o campo em branco se não quiser excluir nenhuma unidade.'
                     '\n\nSepare cada unidade com vírgulas "," para excluir mais de uma.'
                     '\n\nUnidades: ')

    if unidades == "menu":
        selecionar_modo()
    else:
        if not re.match('^[a-zA-Z,]*$', unidades):
            subprocess.run("cls", shell=True)
            print(f"{BColors.FAIL}Unidade(s) inválida(s)\n" + BColors.ENDC)
            excluir_unidades()
        if "c" in unidades or "C" in unidades:
            subprocess.run("cls", shell=True)
            print(f'{BColors.FAIL}Unidade "C" já está excluída por padrão.\n' + BColors.ENDC)
            excluir_unidades()
        else:
            lista_unidades = unidades.upper().split(",")

            for u in lista_unidades:
                if u not in unidades_excluidas:
                    unidades_excluidas.append(u)

            if "" in unidades_excluidas:
                unidades_excluidas.remove("")

            formatar_fmc()


def formatar_fmc():
    global lista_de_dispositivos
    global tipo_de_formatacao
    global erro_critico

    tipo_de_formatacao = "forçada"

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

    alerta_operacao_iniciada()

    formatar(lista_de_dispositivos)

    print(f"{BColors.OKGREEN}\nOperação concluída." + BColors.ENDC)
    print(f"{BColors.OKGREEN}\nRemova o Flash Memory Card." + BColors.ENDC)

    if erro_critico:
        erros_encontrados()
    else:
        alerta_operacao_concluida()

    while True:
        if listar_dispositivos() == "":
            break

    formatar_fmc()


def subprocess_formatar(midia):
    global erro_critico

    result = subprocess.run("format /q /y /x " + midia + ":", shell=True, stdout=subprocess.DEVNULL,
                            stderr=subprocess.STDOUT)

    if str(result.returncode) == "0":
        print(f"{BColors.OKBLUE}Unidade " + midia + " formatada com sucesso." + BColors.ENDC)
    else:
        print(f"{BColors.FAIL}Ocorreu um erro ao tentar formatar a unidade: " + midia + "." + BColors.ENDC)
        erro_critico = True


def usb_watcher(mensagens):
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

            mensagens()

            if keyboard.is_pressed("F"):
                break

            if len(lista_de_dispositivos) < int(numero_midias):
                lista_de_dispositivos.clear()
            else:
                break
        elif str(result) == "":
            mensagens()


def alerta_operacao_concluida():
    playsound("audios/sucesso.mp3")


def alerta_operacao_iniciada():
    playsound("audios/iniciando.mp3")


def erros_encontrados():
    playsound("audios/erros.mp3")


selecionar_modo()
