TCM_REGISTERS = {
    "DELAY_A"       : {"address": 0x0000, "range": {"min": -1024, "max": 1024}, "readonly": False, "bits_pos": {"LSB": 0, "LEN": 16}},
    "DELAY_C"       : {"address": 0x0001, "range": {"min": -1024, "max": 1024}, "readonly": False, "bits_pos": {"LSB": 0, "LEN": 16}},
    "LASER_DELAY"   : {"address": 0x0002, "range": {"min": -1024, "max": 1024}, "readonly": False, "bits_pos": {"LSB": 0, "LEN": 16}},
    "ATTENUATOR"    : {"address": 0x0003, "range": {"min": 0,   "max": 12_000}, "readonly": False, "bits_pos": {"LSB": 0, "LEN": 16}}, #! No nie wiem czy to jest dobre zakres przekracza 13 bitów kalibracji
    "ATTEN_VALUE"   : {"address": 0x0003, "range": {"min": 0,   "max": 12_000}, "readonly": False, "bits_pos": {"LSB": 0, "LEN": 13}},
    "ATTEN_BUSY"    : {"address": 0x0003, "range": {"min": 0,   "max": 1},      "readonly": True , "bits_pos": {"LSB": 14,"LEN": 1}},
    "ATTEN_ERROR"   : {"address": 0x0003, "range": {"min": 0,   "max": 1},      "readonly": True , "bits_pos": {"LSB": 15,"LEN": 1}},
    "SWITCHES"      : {"address": 0x0004, "range": {"min": 0,   "max": 0b1111}, "readonly": False, "bits_pos": {"LSB": 0, "LEN": 16}},
    "TEMPERATURE"   : {}
}