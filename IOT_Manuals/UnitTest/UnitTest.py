import unittest
from Controller_IOT.uart import *
from Adafruit_IO import MQTTClient, client


class Test_IOT(unittest.TestCase):
    def test_port(self):
        port = getPort()

        self.assertEqual(port, 'COM9')

    def test_checkSum_true(self):
        data_ex = '!1:T:32.1:C:638#'

        data_test = checkSum(data_ex)
        self.assertTrue(data_test)

    def test_checkSum_false(self):
        data_ex = '!1:T:32.1:C:630#'

        data_test = checkSum(data_ex)
        self.assertFalse(data_test)

    def test_state_uart_connect(self):
        global state
        state = st.CONNECTED
        state_test = detect_NoConnect_Uart(client)
        self.assertEqual(state_test, st.CONNECTED)




