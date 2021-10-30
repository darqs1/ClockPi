from libs.matrixled import MatrixLed
from libs.variables import version
from time import sleep
from libs.messages import Messages

mled = MatrixLed()
mled.showMessage("ClockPi v." + version, 0.01)
mes = Messages()

try:
    mled.clockStart()
    while True:
        if (len(mes.messages) > 0):
            mled.showMessage(mes.messages[0], 0.01)
        sleep(1)

except KeyboardInterrupt:
    mled.showMessage('Goodbye', 0.01)
    sleep(1)
    mled.clockStop()