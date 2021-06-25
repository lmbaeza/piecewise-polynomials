# Desarrollo del modelo "Piecewise Cubic Polynomials"
# Expuesto en el capítulo 5.2 del libro "The Elements of Statistical Learning"

import math
from lib import *

class PiecewiseCubicPolynomials:

    def __init__(self, x_data, y_data, y_target):
        # Axes limits and knots
        self.x_min = -1
        self.x_knot_1 = 1.5
        self.x_knot_2 = 4.5
        self.x_max = 7

        #  x_data, y_data, y_target
        self.x_data = x_data
        self.y_data = y_data
        self.y_target = y_target

        # self.x_data = my_linspace(self.x_min, self.x_max, 50)
        # self.y_data, self.y_target = function(self.x_data, math.cos)

    def buildCubicSpline(self):
        self.h1 = my_ones(self.x_data)
        self.h2 = self.x_data.copy()
        self.h3 = my_power(self.h2, 2)
        self.h4 = my_power(self.h2, 3)
        self.h5 = my_transform(self.x_data, self.x_knot_1)
        self.h6 = my_transform(self.x_data, self.x_knot_2)

    def build(self):
        self.buildCubicSpline()

        H = my_matrix_transpose([self.h1, self.h2, self.h3, self.h4, self.h5, self.h6])

        # Ajustar "Basis Expansion" via OLS

        # Definimos la multiplicacion matricial como A @ B

        # HH1 = H.transpose @ H
        HH1 = multiply(my_matrix_transpose(H), H)

        # HH2 = H.transpose @ y_data
        HH2 = multiply(my_matrix_transpose(H), to_col(self.y_data))

        # Agregar la columna de restricciones a la matriz
        for i, val in enumerate(HH2):
            HH1[i].append(val[0])

        # Resolver el sistema de ecuaciones lineales usando Gauss
        beta = gauss(HH1)
        # beta es un vector con las soluciones del sistema
        if type(beta) == type(False):
            return False, False, False, False
        # y_hat = H @ beta
        self.y_hat = multiply(H, to_col(beta))

        return self.x_data, self.y_data, self.y_target, self.y_hat