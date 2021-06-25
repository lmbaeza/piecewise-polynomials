# Integrantes:
# Camilo Ernesto Vargas Romero        camevargasrom@unal.edu.co 
# Sarah Lancheros Soler               slancheross@unal.edu.co 
# Gustavo Galvez Bello                ggalvezb@unal.edu.co 
# Luis Miguel Báez Aponte             lmbaeza@unal.edu.co
# Jefferson Daniel Castro             jedcastroag@unal.edu.co 

# Piecewise Polynomials and Splines5

# Importar Librerias de la Interfaz Grafica
import tkinter
from tkinter import ttk
from tkinter import messagebox

# Importar libreria para graficar los datos
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

# Importar el Modelo
from model import PiecewiseCubicPolynomials
# Importar algunas funciones matematicas implementadas
from lib import *
# Importar los datos de ejemplo
from data import EXAMPLE_DATA

from math import cos, sin

class Windows:

    def __init__(self, window):
        self.frame = window
        self.x_min = -1
        self.x_knot_1 = 1.5
        self.x_knot_2 = 4.5
        self.x_max = 7
        self.canRead = False
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
            values=["cos", "sin", "2*x"])
        self.selectGenerator.grid(row=3, column=0)
        self.selectGenerator.bind("<<ComboboxSelected>>", self.callselectGenerator)
        self.selectGenerator.current(0)

        # Label Ejemplo de datos
        self.labelEjemplo = tkinter.Label(self.frame, text="Elegir Ejemplo de datos")
        self.labelEjemplo.grid(row=4, column=0)
        # Ejemplo de datos
        self.selectEjemplo = ttk.Combobox(self.frame, state="disabled", justify='center',
            values=["¿Generar ejemplo?", "Ingresar Datos"])
        self.selectEjemplo.grid(row=5, column=0)
        self.selectEjemplo.bind("<<ComboboxSelected>>", self.callSelectExample)
        self.selectEjemplo.current(0)

        # Texto donde se ingresan los datos
        self.inputText = tkinter.Text(self.frame, height=10, width=55, bg="light yellow")
        self.inputText.grid(row=0, column=1, rowspan=4)

        # Boton que permite refrescar el grafico
        self.refresh = tkinter.Button(self.frame, text="Refrescar Grafico", command=self.refreshClick)
        self.refresh.grid(row=6, column=0)

        # Mostrar Grafica
        self.getDataWithFuncion(cos, 1.0)
        self.updatePlot(self.x_data, self.y_data, self.y_target, self.y_hat)
    
    def getDataWithFuncion(self, funct, dispersion):
        self.x_data = my_linspace(self.x_min, self.x_max, 50)
        self.y_data, self.y_target = function(self.x_data, funct, dispersion)

        model = PiecewiseCubicPolynomials(self.x_data, self.y_data, self.y_target)
        self.x_data, self.y_data, self.y_target, self.y_hat = model.build()
        if type(self.x_data) == type(True):
            self.x_data = []
            self.y_data = []
            self.y_target = []
            self.y_hat = []
            self.inputText.delete("1.0", "end")
            messagebox.showinfo(message="Datos Invalidos", title="Error")
        
    
    def updatePlot(self, x_data, y_data, y_target, y_hat):
        self.fig = Figure(figsize=(5, 4), dpi=100)

        if y_target:
            self.fig.add_subplot(111).plot(
                x_data, y_data, 'o',
                x_data, y_target, 'r',
                x_data, y_hat, 'orange'
            )
            self.fig.legend(["data", "Target", "Regression Splines"])
        else:
            self.fig.add_subplot(111).plot(
                x_data, y_data, 'o',
                x_data, y_hat, 'orange'
            )
            self.fig.legend(["data", "Regression Splines"])
        
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().grid(row=4, column=1, rowspan=11, columnspan=10)

    def callSelectMode(self, event=None):
        print("From callSelectMode")
        if event:
            if event.widget.get() == "Generar datos":
                self.selectGenerator.configure(state="readonly")
                self.selectEjemplo.configure(state="disabled")
                self.canRead = False
                self.callselectGenerator(self.selectGenerator.get())
                self.updatePlot(self.x_data, self.y_data, self.y_target, self.y_hat)
            elif event.widget.get() == "Ingresar datos":
                self.selectGenerator.configure(state="disabled")
                self.selectEjemplo.configure(state="readonly")
                self.inputText.insert(tkinter.INSERT, EXAMPLE_DATA)
                self.readData()
                self.canRead = True

    def callselectGenerator(self, event=None):
        print("From callselectGenerator")
        if event:
            if type(event) != type(""):
                event = event.widget.get()

            if event == "cos":
                self.getDataWithFuncion(cos, 1.0)
                self.updatePlot(self.x_data, self.y_data, self.y_target, self.y_hat)
            elif event == "sin":
                self.getDataWithFuncion(sin, 1.0)
                self.updatePlot(self.x_data, self.y_data, self.y_target, self.y_hat)
            elif event == "2*x":
                def f(x):
                    return 2*x
                self.getDataWithFuncion(f, 3.5)
                self.updatePlot(self.x_data, self.y_data, self.y_target, self.y_hat)
    
    def callSelectExample(self, event=None):
        print("From callSelectExample")
        if event:
            if event.widget.get() == "¿Generar ejemplo?":
                self.inputText.delete("1.0", "end")
                self.inputText.insert(tkinter.INSERT, EXAMPLE_DATA)
                self.readData()
            elif event.widget.get() == "Ingresar Datos":
                self.inputText.delete("1.0", "end")
                self.x_data = []
                self.y_data = []
                self.y_target = []
                self.y_hat = []
                self.updatePlot(self.x_data, self.y_data, self.y_target, self.y_hat)
    
    def readData(self):
        self.x_data = []
        self.y_data = []
        self.y_target = []
        self.y_hat = []

        data = self.inputText.get("1.0", tkinter.END).split("\n")

        for line in data:
            if line != '':
                values = line.split(" ")
                if len(values) != 2:
                    self.x_data = []
                    self.y_data = []
                    self.y_target = []
                    self.y_hat = []
                    self.inputText.delete("1.0", "end")
                    messagebox.showinfo(message="Formato Invalidos", title="Error")
                    return
                else:
                    self.x_data.append(float(values[0]))
                    self.y_data.append(float(values[1]))
        
        model = PiecewiseCubicPolynomials(self.x_data, self.y_data, self.y_target)
        self.x_data, self.y_data, self.y_target, self.y_hat = model.build()
        if type(self.x_data) == type(True):
            self.x_data = []
            self.y_data = []
            self.y_target = []
            self.y_hat = []
            self.inputText.delete("1.0", "end")
            messagebox.showinfo(message="Datos Invalidos", title="Error")

        self.updatePlot(self.x_data, self.y_data, self.y_target, self.y_hat)
    
    def refreshClick(self):
        if self.canRead:
            self.readData()
        else:
            model = PiecewiseCubicPolynomials(self.x_data, self.y_data, self.y_target)

            self.x_data, self.y_data, self.y_target, self.y_hat = model.build()

            if type(self.x_data) == type(True):
                self.x_data = []
                self.y_data = []
                self.y_target = []
                self.y_hat = []
                self.inputText.delete("1.0", "end")
                messagebox.showinfo(message="Datos Invalidos", title="Error")

            self.updatePlot(self.x_data, self.y_data, self.y_target, self.y_hat)

root = tkinter.Tk()
Window = Windows(root)
tkinter.mainloop()
