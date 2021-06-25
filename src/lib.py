import random
import sys


def cmp(a, b):
    a = float(a)
    b = float(b)
    eps = 1e-6
    
    if a + eps < b:
        return -1
    else:
        if b + eps < a:
            return 1
    return 0


def my_linspace(mn, mx, intervals):
    distance = mx - mn
    factor = distance/intervals
    output = []
    output.append(float(mn))
    current = float(mn)
    while current < float(mx):
        current += factor
        output.append(current)

    # return np.linspace(mn, mx, intervals)
    return output

def function(data, funct, dispersion):
    output = []
    target = []
    for i in data:
        delta = random.uniform(-dispersion, dispersion)
        output.append(funct(i) + delta)
        target.append(funct(i))
    return output, target

def my_ones(data):
    output = []
    for _ in data:
        output.append(1.0)
    return output

def my_power(data, n):
    output = []
    for val in data:
        output.append(val**n)
    return output

def my_transform(data, knot):
    output = []
    for val in data:
        if cmp(val, knot) < 0:
            output.append(0.0)
        else:
            output.append( (val-knot) ** 3 )
    return output


def my_matrix_transpose(m):
    rez = [[m[j][i] for j in range(len(m))] for i in range(len(m[0]))]
    return rez


def to_col(data):
    output = []
    for val in data:
        output.append([val])
    return output

def multiply(matrix1, matrix2):
    row1 = len(matrix1)
    col1 = len(matrix1[0])
    
    row2 = len(matrix2)
    col2 =  len(matrix2[0])
    
    # output = [[0]*col2]*row1

    output = [[0 for _ in range(col2)] for _ in range(row1)]
    
    for i in range(row1):
        for j in range(col2):
            for k in range(col1):
                output[i][j] += float(matrix1[i][k] * matrix2[k][j])
    return output


def gauss(a):
    n = len(a)
    x = [0.0]*n
    # Applying Gauss Elimination
    for i in range(n):
        if a[i][i] == 0.0:
            # sys.exit('Divide by zero detected!')
            return False
        
        for j in range(i+1, n):
            ratio = float(a[j][i]/a[i][i])
            
            for k in range(n+1):
                a[j][k] = float(a[j][k] - ratio * a[i][k])
    
    # Back Substitution
    x[n-1] = float(a[n-1][n]/a[n-1][n-1])
    
    for i in range(n-2, -1,-1):
        x[i] = float(a[i][n])
        
        for j in range(i+1,n):
            x[i] = float(x[i] - a[i][j]*x[j])
        
        x[i] = float(x[i]/a[i][i])
    return x


















