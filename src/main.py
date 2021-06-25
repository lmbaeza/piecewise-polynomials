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

from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure

import matplotlib.pyplot as plt

# plt.plot(x_data, y_data, 'o')
# plt.plot(x_data, y_target, color='red')
# plt.plot(x_data, y_hat, color='orange')
# plt.title('Piecewise Cubic Polynomials')
# plt.legend(["data", "Target", "Regression Splines"])
# plt.show()

class Windows:

    def __init__(self, window):
        self.frame = window

        self.frame.wm_title("Piecewise Cubic Polynomials")

        tkinter.Button(self.frame, text="HI").grid(row=0, column=0)

        fig = Figure(figsize=(5, 4), dpi=100)

        fig.add_subplot(111).plot(x_data, y_data, 'o', x_data, y_target, 'r', x_data, y_hat, 'orange')

        canvas = FigureCanvasTkAgg(fig, master=self.frame)  # A tk.DrawingArea.
        canvas.draw()
        # canvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)
        canvas.get_tk_widget().grid(row=1, column=0)

root = tkinter.Tk()
Window = Windows(root)
tkinter.mainloop()