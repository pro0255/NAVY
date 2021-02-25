
from models.XORnet import XORnet
from lab.cv2 import CONSTANTS

def cv2():
    net = XORnet(CONSTANTS.learning_rate)
    net.fit(CONSTANTS.X_train, CONSTANTS.y_train)
    net.predict(CONSTANTS.X_test)
    print('cv2')