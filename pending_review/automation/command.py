import numpy as np


class Command:
    def __init__(self,
                 command_id,
                 op_code,
                 password,
                 response_len):

        self.command_id = np.int16(command_id)
        self.op_code = np.int8(op_code)
        self.password = np.int32(password)
        self.response_len = np.int(response_len)

    def send(self, arg1: np.int32, arg2: np.int32):
        # TODO
        # RTC -> Real Time Clock
        pass

    def parse(self):
        # TODO
        # Takes the packet, checks byte 0 and 1, check the response status, return the data
        pass


cmds = {
    "Ping OBC": Command(0, 0x00, 0, 0),
    "Erase All Memory": Command(0, 0x37, 0, 0),
    "Set Automatic Data Collection Enable": Command(0, 0x22, 0, 0),
    "Send PAY CAN Message": Command(0, 0x41, 0, 8),
    "Set RTC Date/Time": Command(0, 0x02, 0, 0),
    "Collect Data Block": Command(0, 0x20, 0, 4)
}

