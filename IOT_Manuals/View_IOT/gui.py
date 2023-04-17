from tkinter import ttk
import tkinter as tk

from Controller_IOT.connect_MQTT import *
from Controller_IOT.uart import *
from Model_IOT.model_iot import *
import threading
import io

class TextRedirector(io.TextIOBase):
    def __init__(self, textbox):
        self.textbox = textbox

    def write(self, s):
        self.textbox.insert(tk.END, s)
        self.textbox.see(tk.END)

model = Model_IOT()
window = tk.Tk()
get_value = tk.StringVar()

window.title("IOT SYSTEM")
window.geometry("800x600")

def handle_write_mcu():
    value = combo.get()
    if(value == '10s'):
        str_data =  '0@'
    else:
        str_data = value[0]+'@'
    writeData(str_data)
    model.get_selected_value(value)

def handle_write_server():
    value = combo1.get()
    if value == '10s':
        str2int_data = (int(value[0]) * 10 + int(value[1])) * 10
        print(str2int_data)
    else:
        str2int_data = int(value[0])*10
    Controller_IOT.uart.period_default = str2int_data
    model.get_selected_value1(value)

lbl_title = tk.Label(window, text="WELCOME TO IOT SYSTEM", fg="blue", font=("Arial", 20))
lbl_title.place(x=200, y=10)

lbl1 = tk.Label(window, text="Period Send Data",fg="blue", font=("Arial", 8))
lbl1.place(x=10, y=70)

lbl2 = tk.Label(window, text="Period Publish Data",fg="blue", font=("Arial", 8))
lbl2.place(x=10, y=140)

combo = ttk.Combobox(window, width=8, font=("Arial", 8))
combo['value'] = ("1s", "2s", "3s", "4s", "5s", "6s", "7s", "8s", "9s", "10s")
combo.place(x=120, y=70)


combo1 = ttk.Combobox(window, width=8, font=("Arial", 8))
combo1['value'] = ("1s", "2s", "3s", "4s", "5s", "6s", "7s", "8s", "9s", "10s")
combo1.place(x=120, y=140)


btn = tk.Button(window, text="Apply", width=8, fg='blue', bg='yellow', command=handle_write_mcu)
btn.place(x=200, y=68)

btn1 = tk.Button(window, text="Apply", width=8,  fg='blue', bg='yellow', command=handle_write_server)
btn1.place(x=200, y=137)

textbox = tk.Text(window, height=20, width=96)
textbox.place(x=14, y=200)

t1 = threading.Thread(target=run_MQTT, name='t1')
t1.start()
#t1.join()
sys.stdout = TextRedirector(textbox)
sys.stderr = TextRedirector(textbox)
window.mainloop()


