import os
import sys


# currentPath = os.path.dirname(__file__)
# fatherPath = os.path.dirname(currentPath)
# sys.path.append(fatherPath)
# sys.path.append(currentPath)
sys.path.append('..')

from TriggerController import TriggerController
import time

if __name__ == '__main__':


    # Neuracle串口测试
    neuracleSerial = TriggerController('neuracle', 'serial', 'COM4')
    neuracleSerial.open()

    for i in range(1, 40):
        neuracleSerial.send(i)
        time.sleep(0.1)

    # print(7 * 16 * 16 * 16 + 1 5 * 16 * 16 + 15 * 16 + 8)
    #
    # # Neuracle并口测试
    # neuracleParallel = TriggerController('neuracle', 'parallel', 16376)
    # neuracleParallel.open()
    # for i in range(1, 40):
    #     neuracleParallel.send(i)
    #     time.sleep(0.1)

    # for i in range(1, 11):
    # neuracleParallel.send(243)
    # time.sleep(0.1)
    # clock.wait(0.1)
    #
    # neuracleParallel.close()

    # # Neuroscan并口测试
    # neuroscanParallel = TriggerController('neuroscan', 'parallel', 53504)
    # neuroscanParallel.open()
    #
    # for i in range(1, 10):
    #     neuroscanParallel.send(i)
    #     time.sleep(0.02)
