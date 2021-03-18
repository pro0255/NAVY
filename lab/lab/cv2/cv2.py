from models.XORnet import XORnet
from lab.cv2 import CONSTANTS
from tabulate import tabulate


def cv2():
    net = XORnet(CONSTANTS.learning_rate)
    net.fit(CONSTANTS.X_train, CONSTANTS.y_train)
    prediction = net.predict(CONSTANTS.X_test)

    headers = ["X1", "X2", "Prediction", "Y"]

    def construct(x, i):
        res = []
        res = list(x)
        res.append(prediction[i])
        res.append(CONSTANTS.y_test[i][0])
        return res

    tabulate_data = [construct(x, i) for i, x in enumerate(CONSTANTS.X_test)]
    print(tabulate(tabulate_data, headers=headers, tablefmt="orgtbl"))
