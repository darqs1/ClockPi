from libs.matrixled import MatrixLed
from libs.variables import version

mled = MatrixLed()
mled.showMessage("ClockPi v." + version, 0.01)

try:
    mled.clockStart()
except KeyboardInterrupt:
    mled.showMessage('Goodbye', 0.01)
    mled.clockStop()