import serial

    # 0V dc = b'000001102\r\n'
    # 1.3459V dc = b'134571102\r\n' range:2.000

    # Decode 11 bytes from UT71A/B/C
    # ==============================
    # Byte / Bit          6    5    4    3    2    1    0
    # [0]    Digit 1      0    1    1    =====Digit======
    # [1]    Digit 2      0    1    1    =====Digit======
    # [2]    Digit 3      0    1    1    =====Digit======
    # [3]    Digit 4      0    1    1    =====Digit======
    # [4]    Digit 5      0    1    1    =====Digit======
    # [5]    Range        0    1    1    0    =see below=
    # [6]    Unit         0    1    1    ====see below===
    # [7]    Coupling     0    1    1    0    0    DC   AC    (also DC and AC possible)
    # [8]    Info         0    1    1    0    NEG  MAN  AUTO  (MAN or AUTO only)
    # [9]    '\r'         0    0    0    1    1    0    1
    # [10]   '\n'         0    0    0    1    0    1    0
    #
    # Digit: 0x30..0x39 = '0..9', 0x3A = ' ', 0x3B = '-', 0x3C = 'L', 0x3F = 'H'
    # REL not sent
    # No transmission in HOLD state
    # If NEG set at Range 15 sent value is duty cycle
    # No LowBat info sent
    # Storage data not accessible
    #
    #       Range:   0   1     2     3     4     5    6     7     8     9    10    11    12    13   14  15
    # Multiply:      mV  V     V     mV    Ω     F    °C    µA    mA    A    Pipes Diode Hz    °F   W   %
    #         '0'    .01 -     -     .01  -      -    .1   .01   .001   -    .01   .0001 .001  .1   -   .01
    #         '1'    -   .0001 .0001 -    .01   .001  -    .1    .01    .001 -     -     .01   -    -   -
    #         '2'    -   .001  .001  -    .0001 .01   -    -     -      -    -     -     .0001 -    -   -
    #         '3'    -   .01   .01   -    .001  .0001 -    -     -      -    -     -     .001  -    -   -
    #         '4'    -   .1    .1    -    .01   .001  -    -     -      -    -     -     .01   -    -   -
    #         '5'    -   -     -     -    .0001 .01   -    -     -      -    -     -     .0001 -    -   -
    #         '6'    -   -     -     -    .001  .0001 -    -     -      -    -     -     .001  -    -   -
    #         '7'    -   -     -     -    .01   .001  -    -     -      -    -     -     .01   -    -   -


class UT:
    BAUD = 2400
    PARITY = serial.STOPBITS_ONE
    BITS = serial.SEVENBITS
    PORT = None

    EoF = "\r\n"
    MSG_SIZE = 11
    OV = "::0<:"

    DIGITS = 5


    MEASURE_MULTIPLY = [
            [0.01, 1,      1, 0.01, 1, 1, 0.1, 0.01,   0.001, 1,   0.01, 0.0001, 0.001, 0.1, 1,  0.01],
            [1,    0.0001, 0.0001,  1, 0.01,   0.001,  1,     0.1, 0.01, 0.001,  1,     1,   0.01, 1, 1, 1],
            [1,    0.001,  0.001,   1, 0.0001, 0.01,   1,     1,   1,    1,      1,     1,   0.0001, 1, 1, 1],
            [1,    0.01,   0.01,    1, 0.001,  0.0001, 1,     1,   1,    1,      1,     1,   0.001, 1, 1, 1],
            [1,    0.1,    0.1,     1, 0.01,   0.001,  1,     1,   1,    1,      1,     1,   0.01, 1, 1, 1],
            [1,    1,      1,       1, 0.0001, 0.01,   1,     1,   1,    1,      1,     1,   0.0001, 1, 1, 1],
            [1,    1,      1,       1, 0.001,  0.0001, 1,     1,   1,    1,      1,     1,   0.001, 1, 1, 1],
            [1,    1,      1,       1, 0.01,   0.001,  1,     1,   1,    1,      1,     1,   0.01, 1, 1, 1]
        ]

    MEASURE_UNIT = [
        "mV~", "V—", "V~", "mV–",
        "Ω", "F", "°C:", 
        "µA", "mA", "A",
        "Ω", "V diode",
        "Hz", "W", "%"
    ]

    Ω_PREFIX = ["", "", "k", "k", "k", "M", "M", "M"]
    F_PREFIX = ["", "n", "n", "µ", "µ", "µ", "m"]
    Hz_PREFIX =["", "", "k", "k", "k", "M", "M", "M"]




    def __init__(self, port):
        self.connect(port)

    def __del__(self):
        self.dev.close()

    def connect(self, port = None):
        self.PORT = port
        self.dev = serial.Serial(port=self.PORT, baudrate=self.BAUD, bytesize=self.BITS)

    def read(self) -> str:
        if not self.dev:
            return "-1"

        data = self.dev.read_until(self.EoF.encode(), self.MSG_SIZE)
        print(data)
        # return data
        if len(data) != self.MSG_SIZE:
            return "ERROR"
        return self.decode(data)
        
        
    def decode(self, data: bytearray) -> str:
        value = data[0:5].decode()
        if value == self.OV:
            return "OVERLOAD"

        measure_range = data[5] & 0x07
        measure_unit  = data[6] & 0x0F

        value = round(int(value) * self.MEASURE_MULTIPLY[measure_range][measure_unit], self.DIGITS)
        
        prefix = ""
        sign = ""
        unit = self.MEASURE_UNIT[measure_unit]
        if unit == "Hz":
            if data[8] & 0x4:
                measure_unit += 2
                unit = self.MEASURE_UNIT[measure_unit]
            else:
                prefix = self.Hz_PREFIX[measure_range]
        elif unit == "Ω":
            prefix = self.Ω_PREFIX[measure_range]
        elif unit == "F":
            prefix = self.F_PREFIX[measure_range]
        else:
            sign = "-" if data[8] & 0x4 else ""

        value = f"{sign}{value}{prefix}{unit}"
        return value
        


if __name__ == "__main__":
    ut = UT("/dev/ttyUSB0")
    # ut.read()
    # print(ut.read())

    # print(ut.decode(b'000001102\r\n'))
    # print(ut.decode(b'134571102\r\n'))

    while True:
        try:
            print(ut.read())
        except ValueError:
            print("ERROR")
        except KeyboardInterrupt:
            break




