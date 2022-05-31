import subprocess
import time

numero_usb = 0

array = []


def quantidade_usb():
    global numero_usb

    print("Entre a quantidade de USB que serão formatados: ")
    numero_usb = input()

    detectar_usb_e_formatar()


def detectar_usb_e_formatar():
    global array
    global numero_usb

    array.clear()

    subprocess.run("cls", shell=True)

    print("Insira as mídias, " + str(numero_usb) + " no total.")

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
            print("Insira as mídias, " + str(numero_usb) + " no total.\n")
            print("Número de mídias inseridas: " + str(len(array)) + "\n")
            print(str(array) + "\n")
            if len(array) != int(numero_usb):
                array.clear()
            else:
                break

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

    detectar_usb_e_formatar()


quantidade_usb()
