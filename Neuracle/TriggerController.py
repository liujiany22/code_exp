from Trigger.Neuracle.NeuracleTriggerSystemImplement import NeuracleTriggerSystemImplement
from Trigger.Neuroscan.NeuroscanTriggerSystemImplement import NeuroscanTriggerSystemImplement
# from StimulationTest.ExchangeMessage import ExchangeMessage


class TriggerController:    

    def __init__(self, eegServerType:str, triggerHandle:str, port):
        """

        :param eegServerType: 输入'neuracle'则使用neuracle的trigger系统,输入'neuroscan'则使用neuroscan的trigger系统
        :param triggerHandle: 输入'serial'表示使用串口,输入'parallel'表示使用并口
        :param port: 串口/并口所对应的端口,如:neuracle串口输入'COM3'(字符串格式),并口输入32760;neuroscan并口输入53504
        """
        # 脑电类型
        self.eegServerType = eegServerType

        # trigger的串口或者并口选择
        self.triggerHandle = triggerHandle

        # 端口
        self.port = port

        if self.eegServerType.lower() == 'neuracle':
            self.__triggerSystemHandle = NeuracleTriggerSystemImplement(self.triggerHandle, self.port)
        elif self.eegServerType.lower() == 'neuroscan':
            self.__triggerSystemHandle = NeuroscanTriggerSystemImplement(self.port)

    def open(self):
        self.__triggerSystemHandle.open()

    def close(self):
        self.__triggerSystemHandle.close()

    def send(self, event):
        """

        :param event: 输入想输入的trigger值
        :return: None
        """
        self.__triggerSystemHandle.send(event)
