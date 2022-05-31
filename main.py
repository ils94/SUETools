import subprocess
import os
import sys
from tkinter import messagebox
import tkinter as tk

root = tk.Tk()
root.withdraw()


def detectar_usb():
    array = []

    while True:
        result = str(subprocess.check_output("wmic logicaldisk where drivetype=2 get DeviceID", text=True)).replace(
            "\r", "").replace("\n", "").replace("DeviceID  ", "").replace(":        ", "|")
        if str(result) != "":
            array = result.split("|")
            array.remove("")
            print(array)
            if len(array) != 2:
                array.clear()
            else:
                break

    for usb in array:
        os.system("format /q /x /y " + usb + ":")

    pergunta = messagebox.askyesno("Operação concluída", "Deseja começar uma nova operação?")

    if pergunta:
        pergunta_2 = messagebox.showwarning("Iniciar nova Operação",
                                            "Por favor, retire os USBs que já foram formatados")

        if pergunta_2:
            detectar_usb()
    else:
        sys.exit()


detectar_usb()