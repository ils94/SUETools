import subprocess
import os

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

    while True:
        result = str(subprocess.check_output("wmic logicaldisk where drivetype=2 get DeviceID", text=True)).replace(
            "\r", "").replace("\n", "").replace("DeviceID  ", "").replace(":        ", "|")
        if str(result) != "":
            array = result.split("|")
            array.remove("")
            print(str(array))
            if len(array) != int(numero_usb):
                array.clear()
            else:
                break

    for usb in array:
        os.system("format /q /x /y " + usb + ":")

    while True:
        result = str(subprocess.check_output("wmic logicaldisk where drivetype=2 get DeviceID", text=True)).replace(
            "\r", "").replace("\n", "").replace("DeviceID  ", "").replace(":        ", "")
        print("Remova todas as USBs")
        if result == "":
            break

    detectar_usb_e_formatar()


quantidade_usb()
