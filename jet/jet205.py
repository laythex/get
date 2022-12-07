import jetFunctions as j
import time

j.initSpiAdc()
data = []

j.initStepMotorGpio()

j.stepBackward(750)

for i in range(100):
    j.stepForward(15)
    time.sleep(0.05)
    data.append(j.getMeanAdc(50))

j.save(data, 1500)

j.stepBackward(750)

j.deinitSpiAdc()
j.deinitStepMotorGpio()