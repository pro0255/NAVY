from utils.equation import equation

def resolveYForPts(X):
    Y = []
    for vec in X:
        x_0 = vec[0]
        y_0 = vec[1]
        y = equation(x_0)
        if y_0 > y:
            Y.append(1)  
        elif y_0 < y:
            Y.append(-1)
        else:
            Y.append(0)
    return Y