# Integrantes:
# Camilo Ernesto Vargas Romero        camevargasrom@unal.edu.co 
# Sarah Lancheros Soler               slancheross@unal.edu.co 
# Gustavo Galvez Bello                ggalvezb@unal.edu.co 
# Luis Miguel Báez Aponte             lmbaeza@unal.edu.co
# Jefferson Daniel Castro             jedcastroag@unal.edu.co 

# Piecewise Polynomials and Splines

import math
from lib import *

# Axes limits and knots
x_min, x_knot_1, x_knot_2, x_max = -1, 1.5, 4.5, 7

x_data = my_linspace(x_min, x_max, 50)
y_data, y_target = function(x_data, math.cos)

h1 = my_ones(x_data)
h2 = x_data.copy()
h3 = my_power(h2, 2)
h4 = my_power(h2, 3)
h5 = my_transform(x_data, x_knot_1)
h6 = my_transform(x_data, x_knot_2)

H = my_matrix_transpose([h1, h2, h3, h4, h5, h6])

# Ajustar "Basis Expansion" via OLS

HH1 = multiply(my_matrix_transpose(H), H)

HH2 = multiply(my_matrix_transpose(H), to_col(y_data))

for i, val in enumerate(HH2):
    HH1[i].append(val[0])

beta = gauss(HH1)

y_hat = multiply(H, to_col(beta))

# Ploting
import tkinter
from tkinter import ttk

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

# import matplotlib.pyplot as plt
# plt.plot(x_data, y_data, 'o')
# plt.plot(x_data, y_target, color='red')
# plt.plot(x_data, y_hat, color='orange')
# plt.title('Piecewise Cubic Polynomials')
# plt.legend(["data", "Target", "Regression Splines"])
# plt.show()

class Windows:

    def __init__(self, window):
        self.frame = window
        self.initUI()
    
    def initUI(self):
        # Configurar el Titulo
        self.frame.wm_title("Piecewise Cubic Polynomials")
        root.resizable(0, 0)

        # Label Selecionar Modo
        self.labelMode = tkinter.Label(self.frame, text="Selecionar Modo de Uso")
        self.labelMode.grid(row=0, column=0)
        # Selecionar modo de uso
        self.selectMode = ttk.Combobox(self.frame, state="readonly", justify='center',
            values=["Generar datos", "Ingresar datos"])
        self.selectMode.grid(row=1, column=0)
        self.selectMode.bind("<<ComboboxSelected>>", self.callSelectMode)
        self.selectMode.current(0)

        # Label Generar datos utilizando funciones
        self.labelGenerar = tkinter.Label(self.frame, text="Selecionar función que desea utilizar")
        self.labelGenerar.grid(row=2, column=0)
        # Generar datos utilizando funciones
        self.selectGenerator = ttk.Combobox(self.frame, state="readonly", justify='center',
            values=["cos", "sin"])
        self.selectGenerator.grid(row=3, column=0)
        self.selectGenerator.bind("<<ComboboxSelected>>", self.callselectGenerator)
        self.selectGenerator.current(0)

        # Label Ejemplo de datos
        self.labelEjemplo = tkinter.Label(self.frame, text="Elegir Ejemplo de datos")
        self.labelEjemplo.grid(row=4, column=0)
        # Ejemplo de datos
        self.selectEjemplo = ttk.Combobox(self.frame, state="disabled", justify='center',
            values=["¿Generar ejemplo?", "No generar"])
        self.selectEjemplo.grid(row=5, column=0)
        self.selectEjemplo.bind("<<ComboboxSelected>>", self.callSelectExample)
        self.selectEjemplo.current(0)

        # Texto donde se ingresan los datos
        inputText = tkinter.Text(self.frame, height=10, width=55, bg="light yellow")
        inputText.grid(row=0, column=1, rowspan=4)

        self.refresh = tkinter.Button(self.frame, text="Refrescar Grafico", command=self.refreshClick)
        self.refresh.grid(row=6, column=0)

        # Mostrar Grafica
        self.fig = Figure(figsize=(5, 4), dpi=100)

        self.fig.add_subplot(111).plot(
            x_data, y_data, 'o',
            x_data, y_target, 'r',
            x_data, y_hat, 'orange'
        )
        self.fig.legend(["data", "Target", "Regression Splines"])

        self.canvas = FigureCanvasTkAgg(self.fig, master=self.frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().grid(row=4, column=1, rowspan=11, columnspan=10)

    def callSelectMode(self, event=None):
        print("From callSelectMode")
        if event:
            if event.widget.get() == "Generar datos":
                self.selectGenerator.configure(state="readonly")
                self.selectEjemplo.configure(state="disabled")
            elif event.widget.get() == "Ingresar datos":
                self.selectGenerator.configure(state="disabled")
                self.selectEjemplo.configure(state="readonly")

    def callselectGenerator(self, event=None):
        print("From callselectGenerator")
        if event:
            if event.widget.get() == "cos":
                pass
            elif event.widget.get() == "sin":
                pass
    
    def callSelectExample(self, event=None):
        print("From callSelectExample")
        if event:
            if event.widget.get() == "cos":
                pass
            elif event.widget.get() == "sin":
                pass
    def refreshClick(self):
        print("Click")

root = tkinter.Tk()
Window = Windows(root)
tkinter.mainloop()