CHANNELS_1 = {
    "CH01" : {"address": 0,  "range": None, "readonly": None, "bits_pos": None, "additionalValue": None},
    "CH02" : {"address": 1,  "range": None, "readonly": None, "bits_pos": None, "additionalValue": None},
    "CH03" : {"address": 2,  "range": None, "readonly": None, "bits_pos": None, "additionalValue": None},
    "CH04" : {"address": 3,  "range": None, "readonly": None, "bits_pos": None, "additionalValue": None},
    "CH05" : {"address": 4,  "range": None, "readonly": None, "bits_pos": None, "additionalValue": None},
    "CH06" : {"address": 5,  "range": None, "readonly": None, "bits_pos": None, "additionalValue": None},
    "CH07" : {"address": 6,  "range": None, "readonly": None, "bits_pos": None, "additionalValue": None},
    "CH08" : {"address": 7,  "range": None, "readonly": None, "bits_pos": None, "additionalValue": None},
    "CH09" : {"address": 8,  "range": None, "readonly": None, "bits_pos": None, "additionalValue": None},
    "CH10" : {"address": 9,  "range": None, "readonly": None, "bits_pos": None, "additionalValue": None},
    "CH11" : {"address": 10, "range": None, "readonly": None, "bits_pos": None, "additionalValue": None},
    "CH12" : {"address": 11, "range": None, "readonly": None, "bits_pos": None, "additionalValue": None},
}

CHANNELS_2 = {
    "CH01" : {"address": 0,  "range": None, "readonly": None, "bits_pos": None, "additionalValue": None},
    "CH02" : {"address": 2,  "range": None, "readonly": None, "bits_pos": None, "additionalValue": None},
    "CH03" : {"address": 4,  "range": None, "readonly": None, "bits_pos": None, "additionalValue": None},
    "CH04" : {"address": 6,  "range": None, "readonly": None, "bits_pos": None, "additionalValue": None},
    "CH05" : {"address": 8,  "range": None, "readonly": None, "bits_pos": None, "additionalValue": None},
    "CH06" : {"address": 10, "range": None, "readonly": None, "bits_pos": None, "additionalValue": None},
    "CH07" : {"address": 12, "range": None, "readonly": None, "bits_pos": None, "additionalValue": None},
    "CH08" : {"address": 14, "range": None, "readonly": None, "bits_pos": None, "additionalValue": None},
    "CH09" : {"address": 16, "range": None, "readonly": None, "bits_pos": None, "additionalValue": None},
    "CH10" : {"address": 18, "range": None, "readonly": None, "bits_pos": None, "additionalValue": None},
    "CH11" : {"address": 20, "range": None, "readonly": None, "bits_pos": None, "additionalValue": None},
    "CH12" : {"address": 22, "range": None, "readonly": None, "bits_pos": None, "additionalValue": None},
}

CHANNELS_4 = {
    "CH01" : {"address": 0,  "range": None, "readonly": None, "bits_pos": None, "additionalValue": None},
    "CH02" : {"address": 4,  "range": None, "readonly": None, "bits_pos": None, "additionalValue": None},
    "CH03" : {"address": 8,  "range": None, "readonly": None, "bits_pos": None, "additionalValue": None},
    "CH04" : {"address": 12, "range": None, "readonly": None, "bits_pos": None, "additionalValue": None},
    "CH05" : {"address": 16, "range": None, "readonly": None, "bits_pos": None, "additionalValue": None},
    "CH06" : {"address": 20, "range": None, "readonly": None, "bits_pos": None, "additionalValue": None},
    "CH07" : {"address": 24, "range": None, "readonly": None, "bits_pos": None, "additionalValue": None},
    "CH08" : {"address": 28, "range": None, "readonly": None, "bits_pos": None, "additionalValue": None},
    "CH09" : {"address": 32, "range": None, "readonly": None, "bits_pos": None, "additionalValue": None},
    "CH10" : {"address": 36, "range": None, "readonly": None, "bits_pos": None, "additionalValue": None},
    "CH11" : {"address": 40, "range": None, "readonly": None, "bits_pos": None, "additionalValue": None},
    "CH12" : {"address": 44, "range": None, "readonly": None, "bits_pos": None, "additionalValue": None},
}

PM_REGISTERS = {
    "TGR_SETTINGS"                  : {"address": 0x0000, "range": {"min":  0,     "max": 511},          "readonly": False, "bits_pos": {"LSB": 0, "LEN":  9}, "additionalValue": None},
    "OR_GATE"                       : {"address": 0x0000, "range": {"min":  0,     "max": 255},          "readonly": False, "bits_pos": {"LSB": 0, "LEN":  8}, "additionalValue": None},
    "CHANNEL_SETTINGS"              : {"address": 0x0001, "range": {"min":  0,     "max": 8191},         "readonly": False, "bits_pos": {"LSB": 0, "LEN": 13}, "additionalValue": CHANNELS_1},
    "TIME_ALIGN"                    : {"address": 0x0001, "range": {"min": -2048,  "max": 2047},         "readonly": False, "bits_pos": {"LSB": 0, "LEN": 12}, "additionalValue": CHANNELS_1},
    "ADC0_BASELINE"                 : {"address": 0x000D, "range": {"min":  0,     "max": 4095},         "readonly": True,  "bits_pos": {"LSB": 0, "LEN": 12}, "additionalValue": CHANNELS_2},
    "ADC1_BASELINE"                 : {"address": 0x000E, "range": {"min":  0,     "max": 4095},         "readonly": True,  "bits_pos": {"LSB": 0, "LEN": 12}, "additionalValue": CHANNELS_2},
    "ADC0_RANGE"                    : {"address": 0x0025, "range": {"min":  0,     "max": 4095},         "readonly": False, "bits_pos": {"LSB": 0, "LEN": 12}, "additionalValue": CHANNELS_2},
    "ADC1_RANGE"                    : {"address": 0x0026, "range": {"min":  0,     "max": 4095},         "readonly": False, "bits_pos": {"LSB": 0, "LEN": 12}, "additionalValue": CHANNELS_2},
    "CFD_SATR"                      : {"address": 0x003D, "range": {"min":  0,     "max": 65535},        "readonly": False, "bits_pos": {"LSB": 0, "LEN": 16}, "additionalValue": None},
    "RAW_TDC_DATA"                  : {"address": 0x0040, "range": {"min":  0,     "max": 16383},        "readonly": True,  "bits_pos": {"LSB": 0, "LEN": 14}, "additionalValue": CHANNELS_1},
    "ADC0_DISPERSION"               : {"address": 0x004C, "range": {"min":  0,     "max": 65535},        "readonly": True,  "bits_pos": {"LSB": 0, "LEN": 16}, "additionalValue": CHANNELS_2},
    "ADC1_DISPERSION"               : {"address": 0x004D, "range": {"min":  0,     "max": 65535},        "readonly": True,  "bits_pos": {"LSB": 0, "LEN": 16}, "additionalValue": CHANNELS_2},
    "ADC0_MEANAMPL"                 : {"address": 0x0064, "range": {"min": -32768, "max": 32767},        "readonly": True,  "bits_pos": {"LSB": 0, "LEN": 16}, "additionalValue": CHANNELS_2},
    "ADC1_MEANAMPL"                 : {"address": 0x0065, "range": {"min": -32768, "max": 32767},        "readonly": True,  "bits_pos": {"LSB": 0, "LEN": 16}, "additionalValue": CHANNELS_2},
    "CH_MASK"                       : {"address": 0x007C, "range": {"min":  0,     "max": 4095},         "readonly": False, "bits_pos": {"LSB": 0, "LEN": 12}, "additionalValue": None},
    "CH_DISPLACED"                  : {"address": 0x007D, "range": {"min":  0,     "max": 4095},         "readonly": False, "bits_pos": {"LSB": 0, "LEN": 12}, "additionalValue": None},
    "BOARD_STATUS"                  : {"address": 0x007F, "range": {"min":  0,     "max": 32767},        "readonly": False, "bits_pos": {"LSB": 0, "LEN": 15}, "additionalValue": None},
    "CFD_THRESHOLD"                 : {"address": 0x0080, "range": {"min": 300,    "max": 30000},        "readonly": False, "bits_pos": {"LSB": 0, "LEN": 16}, "additionalValue": CHANNELS_4},
    "CFD_ZERO"                      : {"address": 0x0081, "range": {"min": -500,   "max": 500},          "readonly": False, "bits_pos": {"LSB": 0, "LEN": 16}, "additionalValue": CHANNELS_4},
    "ADC_ZERO"                      : {"address": 0x0082, "range": {"min": -500,   "max": 500},          "readonly": False, "bits_pos": {"LSB": 0, "LEN": 16}, "additionalValue": CHANNELS_4},
    "ADC_DELAY"                     : {"address": 0x0083, "range": {"min":  0,     "max": 20000},        "readonly": False, "bits_pos": {"LSB": 0, "LEN": 16}, "additionalValue": CHANNELS_4},
    "THRESHOLD_CALIBR"              : {"address": 0x00B0, "range": {"min":  0,     "max": 4000},         "readonly": False, "bits_pos": {"LSB": 0, "LEN": 16}, "additionalValue": CHANNELS_1},
    "TEMPERATURE"                   : {"address": 0x00BC, "range": {"min": 100,    "max": 700},          "readonly": True,  "bits_pos": {"LSB": 0, "LEN": 16}, "additionalValue": None},
    "BOARD_ID"                      : {"address": 0x00BD, "range": {"min":  0,     "max": 65535},        "readonly": True,  "bits_pos": {"LSB": 0, "LEN": 16}, "additionalValue": None},
    "BOARD_TYPE"                    : {"address": 0x00BD, "range": {"min":  0,     "max":  3},           "readonly": True,  "bits_pos": {"LSB": 0, "LEN":  2}, "additionalValue": None},
    "SERIAL_NUM"                    : {"address": 0x00BD, "range": {"min":  0,     "max": 255},          "readonly": True,  "bits_pos": {"LSB": 8, "LEN":  8}, "additionalValue": None},
    "CNT_CFD"                       : {"address": 0x00C0, "range": {"min":  0,     "max": 4294967295},   "readonly": True,  "bits_pos": {"LSB": 0, "LEN": 32}, "additionalValue": CHANNELS_2},
    "CNT_TRG"                       : {"address": 0x00C1, "range": {"min":  0,     "max": 4294967295},   "readonly": True,  "bits_pos": {"LSB": 0, "LEN": 32}, "additionalValue": CHANNELS_2},
}


TCM_REGISTERS = {           
    "DELAY_A"                       : {"address": 0x0000, "range": {"min": -1024, "max": 1024},          "readonly": False, "bits_pos": {"LSB":  0, "LEN": 16}, "additionalValue": None},
    "DELAY_C"                       : {"address": 0x0001, "range": {"min": -1024, "max": 1024},          "readonly": False, "bits_pos": {"LSB":  0, "LEN": 16}, "additionalValue": None},
    "LASER_DELAY"                   : {"address": 0x0002, "range": {"min": -1024, "max": 1024},          "readonly": False, "bits_pos": {"LSB":  0, "LEN": 16}, "additionalValue": None},
    "ATTENUATOR"                    : {"address": 0x0003, "range": {"min": 0,     "max": 0xFF_FFFF},     "readonly": False, "bits_pos": {"LSB":  0, "LEN": 16}, "additionalValue": None},
    "ATTEN_VALUE"                   : {"address": 0x0003, "range": {"min": 0,     "max": 12_000},        "readonly": False, "bits_pos": {"LSB":  0, "LEN": 14}, "additionalValue": None},
    "ATTEN_BUSY"                    : {"address": 0x0003, "range": {"min": 0,     "max": 1},             "readonly": True , "bits_pos": {"LSB": 14, "LEN":  1}, "additionalValue": None},
    "ATTEN_ERROR"                   : {"address": 0x0003, "range": {"min": 0,     "max": 1},             "readonly": True , "bits_pos": {"LSB": 15, "LEN":  1}, "additionalValue": None},
    "SWITCHES"                      : {"address": 0x0004, "range": {"min": 0,     "max": 0b1111},        "readonly": False, "bits_pos": {"LSB":  0, "LEN": 16}, "additionalValue": None},
    "TEMPERATURE"                   : {"address": 0x0005, "range": {"min": 100,   "max": 700},           "readonly": True , "bits_pos": {"LSB":  0, "LEN": 16}, "additionalValue": None},
    "BOARD_ID"                      : {"address": 0x0007, "range": {"min": 0,     "max": 0xFFFF},        "readonly": True , "bits_pos": {"LSB":  0, "LEN": 16}, "additionalValue": None},
    "BOARD_TYPE"                    : {"address": 0x0007, "range": {"min": 0,     "max": 3},             "readonly": True , "bits_pos": {"LSB":  0, "LEN":  2}, "additionalValue": None},
    "SERIAL_NUM"                    : {"address": 0x0007, "range": {"min": 0,     "max": 0xFF},          "readonly": True , "bits_pos": {"LSB":  8, "LEN":  8}, "additionalValue": None},
    "VTIME_LOW"                     : {"address": 0x0008, "range": {"min": -512,  "max": 511},           "readonly": False, "bits_pos": {"LSB":  0, "LEN": 10}, "additionalValue": None},
    "VTIME_HIGH"                    : {"address": 0x0009, "range": {"min": -512,  "max": 511},           "readonly": False, "bits_pos": {"LSB":  0, "LEN": 10}, "additionalValue": None},
    "SC_LEVEL_A"                    : {"address": 0x000A, "range": {"min": 0,     "max": 0xFFFF},        "readonly": False, "bits_pos": {"LSB":  0, "LEN": 16}, "additionalValue": None},
    "SC_LEVEL_C"                    : {"address": 0x000B, "range": {"min": 0,     "max": 0xFFFF},        "readonly": False, "bits_pos": {"LSB":  0, "LEN": 16}, "additionalValue": None},
    "C_LEVEL_A"                     : {"address": 0x000C, "range": {"min": 0,     "max": 0xFFFF},        "readonly": False, "bits_pos": {"LSB":  0, "LEN": 16}, "additionalValue": None},
    "C_LEVEL_C"                     : {"address": 0x000D, "range": {"min": 0,     "max": 0xFFFF},        "readonly": False, "bits_pos": {"LSB":  0, "LEN": 16}, "additionalValue": None},
    "MODE"                          : {"address": 0x000E, "range": {"min": 0,     "max": 0x03FF},        "readonly": False, "bits_pos": {"LSB":  0, "LEN": 10}, "additionalValue": None},
    "ADD_C_DELAY"                   : {"address": 0x000E, "range": {"min": 0,     "max": 1},             "readonly": False, "bits_pos": {"LSB":  0, "LEN":  1}, "additionalValue": None},
    "C_SC_TRG_MODE"                 : {"address": 0x000E, "range": {"min": 0,     "max": 3},             "readonly": False, "bits_pos": {"LSB":  1, "LEN":  2}, "additionalValue": None},
    "BOARD_STATUS"                  : {"address": 0x000F, "range": {"min": 0,     "max": 0xFFFF},        "readonly": False, "bits_pos": {"LSB":  0, "LEN": 32}, "additionalValue": None},
    "RESET_COUNTER"                 : {"address": 0x000F, "range": {"min": 0,     "max": 1},             "readonly": False, "bits_pos": {"LSB":  9, "LEN":  1}, "additionalValue": None},
    "FORCE_LOCAL_CLOCK"             : {"address": 0x000F, "range": {"min": 0,     "max": 1},             "readonly": False, "bits_pos": {"LSB": 10, "LEN":  1}, "additionalValue": None},
    "RESET_SYSTEM"                  : {"address": 0x000F, "range": {"min": 0,     "max": 1},             "readonly": False, "bits_pos": {"LSB": 11, "LEN":  1}, "additionalValue": None},
    "PM_LINK_A0"                    : {"address": 0x0010, "range": {"min": 0,     "max": 0xFFFF_FFFF},   "readonly": True,  "bits_pos": {"LSB":  0, "LEN": 32}, "additionalValue": None},
    "PM_LINK_A1"                    : {"address": 0x0011, "range": {"min": 0,     "max": 0xFFFF_FFFF},   "readonly": True,  "bits_pos": {"LSB":  0, "LEN": 32}, "additionalValue": None},
    "PM_LINK_A2"                    : {"address": 0x0012, "range": {"min": 0,     "max": 0xFFFF_FFFF},   "readonly": True,  "bits_pos": {"LSB":  0, "LEN": 32}, "additionalValue": None},
    "PM_LINK_A3"                    : {"address": 0x0013, "range": {"min": 0,     "max": 0xFFFF_FFFF},   "readonly": True,  "bits_pos": {"LSB":  0, "LEN": 32}, "additionalValue": None},
    "PM_LINK_A4"                    : {"address": 0x0014, "range": {"min": 0,     "max": 0xFFFF_FFFF},   "readonly": True,  "bits_pos": {"LSB":  0, "LEN": 32}, "additionalValue": None},
    "PM_LINK_A5"                    : {"address": 0x0015, "range": {"min": 0,     "max": 0xFFFF_FFFF},   "readonly": True,  "bits_pos": {"LSB":  0, "LEN": 32}, "additionalValue": None},
    "PM_LINK_A6"                    : {"address": 0x0016, "range": {"min": 0,     "max": 0xFFFF_FFFF},   "readonly": True,  "bits_pos": {"LSB":  0, "LEN": 32}, "additionalValue": None},
    "PM_LINK_A7"                    : {"address": 0x0017, "range": {"min": 0,     "max": 0xFFFF_FFFF},   "readonly": True,  "bits_pos": {"LSB":  0, "LEN": 32}, "additionalValue": None},
    "PM_LINK_A8"                    : {"address": 0x0018, "range": {"min": 0,     "max": 0xFFFF_FFFF},   "readonly": True,  "bits_pos": {"LSB":  0, "LEN": 32}, "additionalValue": None},
    "PM_LINK_A9"                    : {"address": 0x0019, "range": {"min": 0,     "max": 0xFFFF_FFFF},   "readonly": True,  "bits_pos": {"LSB":  0, "LEN": 32}, "additionalValue": None},
    "SIDE_A_STATUS"                 : {"address": 0x001A, "range": {"min": 0,     "max": 0xFFFF_FFFF},   "readonly": True,  "bits_pos": {"LSB":  0, "LEN": 32}, "additionalValue": None},
    "CH_MASK_A"                     : {"address": 0x001A, "range": {"min": 0,     "max": 511},           "readonly": False, "bits_pos": {"LSB":  0, "LEN":  9}, "additionalValue": None},
    "LASER_CONTROL"                 : {"address": 0x001B, "range": {"min": 0,     "max": 0xFFFF_FFFF},   "readonly": False, "bits_pos": {"LSB":  0, "LEN": 32}, "additionalValue": None},
    "LASER_DIVIDER"                 : {"address": 0x001B, "range": {"min": 0,     "max": 0xFF_FFFF},     "readonly": False, "bits_pos": {"LSB":  0, "LEN": 23}, "additionalValue": None},
    "LASER_SOURCE"                  : {"address": 0x001B, "range": {"min": 0,     "max": 1},             "readonly": False, "bits_pos": {"LSB": 31, "LEN":  1}, "additionalValue": None},
    "LASER_PATTERN_1"               : {"address": 0x001C, "range": {"min": 0,     "max": 0xFFFF_FFFF},   "readonly": False, "bits_pos": {"LSB":  0, "LEN": 32}, "additionalValue": None},
    "LASER_PATTERN_0"               : {"address": 0x001D, "range": {"min": 0,     "max": 0xFFFF_FFFF},   "readonly": False, "bits_pos": {"LSB":  0, "LEN": 32}, "additionalValue": None},
    "SPI_MASK"                      : {"address": 0x001E, "range": {"min": 0,     "max": 0xF_FFFF},      "readonly": False, "bits_pos": {"LSB":  0, "LEN": 20}, "additionalValue": None},
    "PM_LINK_C0"                    : {"address": 0x0030, "range": {"min": 0,     "max": 0xFFFF_FFFF},   "readonly": True,  "bits_pos": {"LSB":  0, "LEN": 32}, "additionalValue": None},
    "PM_LINK_C1"                    : {"address": 0x0031, "range": {"min": 0,     "max": 0xFFFF_FFFF},   "readonly": True,  "bits_pos": {"LSB":  0, "LEN": 32}, "additionalValue": None},
    "PM_LINK_C2"                    : {"address": 0x0032, "range": {"min": 0,     "max": 0xFFFF_FFFF},   "readonly": True,  "bits_pos": {"LSB":  0, "LEN": 32}, "additionalValue": None},
    "PM_LINK_C3"                    : {"address": 0x0033, "range": {"min": 0,     "max": 0xFFFF_FFFF},   "readonly": True,  "bits_pos": {"LSB":  0, "LEN": 32}, "additionalValue": None},
    "PM_LINK_C4"                    : {"address": 0x0034, "range": {"min": 0,     "max": 0xFFFF_FFFF},   "readonly": True,  "bits_pos": {"LSB":  0, "LEN": 32}, "additionalValue": None},
    "PM_LINK_C5"                    : {"address": 0x0035, "range": {"min": 0,     "max": 0xFFFF_FFFF},   "readonly": True,  "bits_pos": {"LSB":  0, "LEN": 32}, "additionalValue": None},
    "PM_LINK_C6"                    : {"address": 0x0036, "range": {"min": 0,     "max": 0xFFFF_FFFF},   "readonly": True,  "bits_pos": {"LSB":  0, "LEN": 32}, "additionalValue": None},
    "PM_LINK_C7"                    : {"address": 0x0037, "range": {"min": 0,     "max": 0xFFFF_FFFF},   "readonly": True,  "bits_pos": {"LSB":  0, "LEN": 32}, "additionalValue": None},
    "PM_LINK_C8"                    : {"address": 0x0038, "range": {"min": 0,     "max": 0xFFFF_FFFF},   "readonly": True,  "bits_pos": {"LSB":  0, "LEN": 32}, "additionalValue": None},
    "PM_LINK_C9"                    : {"address": 0x0039, "range": {"min": 0,     "max": 0xFFFF_FFFF},   "readonly": True,  "bits_pos": {"LSB":  0, "LEN": 32}, "additionalValue": None},
    "CH_MASK_C"                     : {"address": 0x003A, "range": {"min": 0,     "max": 511},           "readonly": False, "bits_pos": {"LSB":  0, "LEN":  9}, "additionalValue": None},
    "COUNTER_UDP_RATE"              : {"address": 0x0050, "range": {"min": 0,     "max": 7},             "readonly": False, "bits_pos": {"LSB":  0, "LEN":  3}, "additionalValue": None},
    "ORA_SIGN"                      : {"address": 0x0060, "range": {"min": 0,     "max": 0x3FF},         "readonly": False, "bits_pos": {"LSB":  0, "LEN": 14}, "additionalValue": None},
    "ORA_RATE"                      : {"address": 0x0061, "range": {"min": 0,     "max": 0x7FFF_FFFF},   "readonly": False, "bits_pos": {"LSB":  0, "LEN": 31}, "additionalValue": None},
    "ORC_SIGN"                      : {"address": 0x0062, "range": {"min": 0,     "max": 0x3FF},         "readonly": False, "bits_pos": {"LSB":  0, "LEN": 14}, "additionalValue": None},
    "ORC_RATE"                      : {"address": 0x0063, "range": {"min": 0,     "max": 0x7FFF_FFFF},   "readonly": False, "bits_pos": {"LSB":  0, "LEN": 31}, "additionalValue": None},
    "SC_SIGN"                       : {"address": 0x0064, "range": {"min": 0,     "max": 0x3FF},         "readonly": False, "bits_pos": {"LSB":  0, "LEN": 14}, "additionalValue": None},
    "SC_RATE"                       : {"address": 0x0065, "range": {"min": 0,     "max": 0x7FFF_FFFF},   "readonly": False, "bits_pos": {"LSB":  0, "LEN": 31}, "additionalValue": None},
    "C_SIGN"                        : {"address": 0x0066, "range": {"min": 0,     "max": 0x3FF},         "readonly": False, "bits_pos": {"LSB":  0, "LEN": 14}, "additionalValue": None},
    "C_RATE"                        : {"address": 0x0067, "range": {"min": 0,     "max": 0x7FFF_FFFF},   "readonly": False, "bits_pos": {"LSB":  0, "LEN": 31}, "additionalValue": None},
    "V_SIGN"                        : {"address": 0x0068, "range": {"min": 0,     "max": 0x3FF},         "readonly": False, "bits_pos": {"LSB":  0, "LEN": 14}, "additionalValue": None},
    "V_RATE"                        : {"address": 0x0069, "range": {"min": 0,     "max": 0x7FFF_FFFF},   "readonly": False, "bits_pos": {"LSB":  0, "LEN": 31}, "additionalValue": None},
    "STATUS_OPTIONCODE"             : {"address": 0x006A, "range": {"min": 0,     "max": 0x7FFF},        "readonly": False, "bits_pos": {"LSB":  0, "LEN": 15}, "additionalValue": None},
    "ORA_ENABLED"                   : {"address": 0x006A, "range": {"min": 0,     "max": 1},             "readonly": False, "bits_pos": {"LSB":  2, "LEN":  1}, "additionalValue": None},
    "ORC_ENABLED"                   : {"address": 0x006A, "range": {"min": 0,     "max": 1},             "readonly": False, "bits_pos": {"LSB":  5, "LEN":  1}, "additionalValue": None},
    "SC_ENABLED"                    : {"address": 0x006A, "range": {"min": 0,     "max": 1},             "readonly": False, "bits_pos": {"LSB":  8, "LEN":  1}, "additionalValue": None},
    "C_ENABLED"                     : {"address": 0x006A, "range": {"min": 0,     "max": 1},             "readonly": False, "bits_pos": {"LSB": 11, "LEN":  1}, "additionalValue": None},
    "V_ENABLED"                     : {"address": 0x006A, "range": {"min": 0,     "max": 1},             "readonly": False, "bits_pos": {"LSB": 14, "LEN":  1}, "additionalValue": None},
    "MODE_SETTINGS"                 : {"address": 0x00D8, "range": {"min": 0,     "max": 0x3FF_FFFF},    "readonly": False, "bits_pos": {"LSB":  0, "LEN": 26}, "additionalValue": None},
    "DG_MODE"                       : {"address": 0x00D8, "range": {"min": 0,     "max": 2},             "readonly": False, "bits_pos": {"LSB":  0, "LEN":  4}, "additionalValue": None},
    "TG_MODE"                       : {"address": 0x00D8, "range": {"min": 0,     "max": 2},             "readonly": False, "bits_pos": {"LSB":  4, "LEN":  4}, "additionalValue": None},
    "RESET_ORBIT_SYNC"              : {"address": 0x00D8, "range": {"min": 0,     "max": 1},             "readonly": False, "bits_pos": {"LSB":  8, "LEN":  1}, "additionalValue": None},
    "RESET_DROPPING_HIT_COUNTERS"   : {"address": 0x00D8, "range": {"min": 0,     "max": 1},             "readonly": False, "bits_pos": {"LSB":  9, "LEN":  1}, "additionalValue": None},
    "RESET_GEN_BUNCH_OFFSET"        : {"address": 0x00D8, "range": {"min": 0,     "max": 1},             "readonly": False, "bits_pos": {"LSB": 10, "LEN":  1}, "additionalValue": None},
    "RESET_GBT_ERRORS"              : {"address": 0x00D8, "range": {"min": 0,     "max": 1},             "readonly": False, "bits_pos": {"LSB": 11, "LEN":  1}, "additionalValue": None},
    "RESET_GBT"                     : {"address": 0x00D8, "range": {"min": 0,     "max": 1},             "readonly": False, "bits_pos": {"LSB": 12, "LEN":  1}, "additionalValue": None},
    "RESET_RX_PHASE_ERROR"          : {"address": 0x00D8, "range": {"min": 0,     "max": 1},             "readonly": False, "bits_pos": {"LSB": 13, "LEN":  1}, "additionalValue": None},
    "TG_CTP_EMUL_MODE"              : {"address": 0x00D8, "range": {"min": 0,     "max": 2},             "readonly": False, "bits_pos": {"LSB": 16, "LEN":  4}, "additionalValue": None},
    "HB_RESPONSE"                   : {"address": 0x00D8, "range": {"min": 0,     "max": 1},             "readonly": False, "bits_pos": {"LSB": 20, "LEN":  1}, "additionalValue": None},
    "BYPASS_MODE"                   : {"address": 0x00D8, "range": {"min": 0,     "max": 1},             "readonly": False, "bits_pos": {"LSB": 21, "LEN":  1}, "additionalValue": None},
    "READOUT_LOCK"                  : {"address": 0x00D8, "range": {"min": 0,     "max": 1},             "readonly": False, "bits_pos": {"LSB": 23, "LEN":  1}, "additionalValue": None},
    "DG_TRG_RESPOND_MASK"           : {"address": 0x00D9, "range": {"min": 0,     "max": 4294967295},    "readonly": False, "bits_pos": {"LSB":  0, "LEN": 32}, "additionalValue": None},
    "DG_BUNCH_PATTERN"              : {"address": 0x00DA, "range": {"min": 0,     "max": 4294967295},    "readonly": False, "bits_pos": {"LSB":  0, "LEN": 32}, "additionalValue": None},
    "TG_PATTERN_1"                  : {"address": 0x00DC, "range": {"min": 0,     "max": 4294967295},    "readonly": False, "bits_pos": {"LSB":  0, "LEN": 32}, "additionalValue": None},
    "TG_PATTERN_0"                  : {"address": 0x00DD, "range": {"min": 0,     "max": 4294967295},    "readonly": False, "bits_pos": {"LSB":  0, "LEN": 32}, "additionalValue": None},
    "TG_CONT_VALUE"                 : {"address": 0x00DE, "range": {"min": 0,     "max": 4294967295},    "readonly": False, "bits_pos": {"LSB":  0, "LEN": 32}, "additionalValue": None},
    "DG_BUNCH_FREQ"                 : {"address": 0x00DF, "range": {"min": 0,     "max": 65535},         "readonly": False, "bits_pos": {"LSB":  0, "LEN": 16}, "additionalValue": None},
    "TG_BUNCH_FREQ"                 : {"address": 0x00DF, "range": {"min": 0,     "max": 65535},         "readonly": False, "bits_pos": {"LSB": 16, "LEN": 16}, "additionalValue": None},
    "DG_FREQ_OFFSET"                : {"address": 0x00E0, "range": {"min": 0,     "max": 268435455},     "readonly": False, "bits_pos": {"LSB":  0, "LEN": 28}, "additionalValue": None},
    "TG_FREQ_OFFSET"                : {"address": 0x00E0, "range": {"min": 0,     "max": 15},            "readonly": False, "bits_pos": {"LSB": 28, "LEN":  4}, "additionalValue": None},
    "RDH_FIELDS"                    : {"address": 0x00E1, "range": {"min": 0,     "max": 4294967295},    "readonly": True,  "bits_pos": {"LSB":  0, "LEN": 32}, "additionalValue": None},
    "RDH_PAR"                       : {"address": 0x00E1, "range": {"min": 0,     "max": 65535},         "readonly": True,  "bits_pos": {"LSB":  0, "LEN": 16}, "additionalValue": None},
    "RDH_FEE_ID"                    : {"address": 0x00E1, "range": {"min": 0,     "max": 255},           "readonly": False, "bits_pos": {"LSB": 24, "LEN":  8}, "additionalValue": None},
    "BCID_OFFSET"                   : {"address": 0x00E3, "range": {"min": 0,     "max": 3563},          "readonly": False, "bits_pos": {"LSB":  0, "LEN": 12}, "additionalValue": None},
    "DATA_SEL_TRG_MASK"             : {"address": 0x00E4, "range": {"min": 0,     "max": 4294967295},    "readonly": False, "bits_pos": {"LSB":  0, "LEN": 32}, "additionalValue": None},
    "STATUS"                        : {"address": 0x00E8, "range": {"min": 0,     "max": 268435455},     "readonly": True,  "bits_pos": {"LSB":  0, "LEN": 28}, "additionalValue": None},
    "READOUT_MODE"                  : {"address": 0x00E8, "range": {"min": 0,     "max":  2},            "readonly": True,  "bits_pos": {"LSB": 16, "LEN":  4}, "additionalValue": None},
    "BCID_SYNC_MODE"                : {"address": 0x00E8, "range": {"min": 0,     "max":  2},            "readonly": True,  "bits_pos": {"LSB": 20, "LEN":  4}, "additionalValue": None},
    "RX_PHASE"                      : {"address": 0x00E8, "range": {"min": 0,     "max": 15},            "readonly": True,  "bits_pos": {"LSB": 24, "LEN":  4}, "additionalValue": None},
    "CRU_READOUT_MODE"              : {"address": 0x00E8, "range": {"min": 0,     "max":  2},            "readonly": True,  "bits_pos": {"LSB": 28, "LEN":  4}, "additionalValue": None},
    "CRU_ORBIT"                     : {"address": 0x00E9, "range": {"min": 0,     "max": 4294967295},    "readonly": True,  "bits_pos": {"LSB":  0, "LEN": 32}, "additionalValue": None},
    "CRU_BC"                        : {"address": 0x00EA, "range": {"min": 0,     "max": 3563},          "readonly": True,  "bits_pos": {"LSB":  0, "LEN": 12}, "additionalValue": None},
    "RAW_FIFO"                      : {"address": 0x00EB, "range": {"min": 0,     "max": 65535},         "readonly": True,  "bits_pos": {"LSB":  0, "LEN": 16}, "additionalValue": None},
    "SEL_FIFO"                      : {"address": 0x00EB, "range": {"min": 0,     "max": 65535},         "readonly": True,  "bits_pos": {"LSB": 16, "LEN": 16}, "additionalValue": None},
    "SEL_FIRST_HIT_DROPPED_ORBIT"   : {"address": 0x00EC, "range": {"min": 0,     "max": 4294967295},    "readonly": True,  "bits_pos": {"LSB":  0, "LEN": 32}, "additionalValue": None},
    "SEL_LAST_HIT_DROPPED_ORBIT"    : {"address": 0x00ED, "range": {"min": 0,     "max": 4294967295},    "readonly": True,  "bits_pos": {"LSB":  0, "LEN": 32}, "additionalValue": None},
    "SEL_HITS_DROPPED"              : {"address": 0x00EE, "range": {"min": 0,     "max": 4294967295},    "readonly": True,  "bits_pos": {"LSB":  0, "LEN": 32}, "additionalValue": None},
    "READOUT_RATE"                  : {"address": 0x00EF, "range": {"min": 0,     "max": 65535},         "readonly": True,  "bits_pos": {"LSB":  0, "LEN": 16}, "additionalValue": None},
    "MCODE_TIME"                    : {"address": 0x00F7, "range": {"min": 0,     "max": 4294967295},    "readonly": True,  "bits_pos": {"LSB":  0, "LEN": 32}, "additionalValue": None},
    "FPGA_TEMPERATURE"              : {"address": 0x00FC, "range": {"min": 0,     "max": 65535},         "readonly": True,  "bits_pos": {"LSB":  0, "LEN": 16}, "additionalValue": None},
    "1V_POWER"                      : {"address": 0x00FD, "range": {"min": 0,     "max": 65535},         "readonly": True,  "bits_pos": {"LSB":  0, "LEN": 16}, "additionalValue": None},
    "1.8V_POWER"                    : {"address": 0x00FE, "range": {"min": 0,     "max": 65535},         "readonly": True,  "bits_pos": {"LSB":  0, "LEN": 16}, "additionalValue": None},
    "FW_TIME"                       : {"address": 0x00FF, "range": {"min": 0,     "max": 4294967295},    "readonly": True,  "bits_pos": {"LSB":  0, "LEN": 32}, "additionalValue": None},

    "PMA0"                          : {"address": 0x0200, "range": {"min": 0,     "max": 0xFFFF_FFFF},   "readonly": True,  "bits_pos": {"LSB": 0, "LEN": 32}, "additionalValue": PM_REGISTERS},
    "PMA1"                          : {"address": 0x0400, "range": {"min": 0,     "max": 0xFFFF_FFFF},   "readonly": True,  "bits_pos": {"LSB": 0, "LEN": 32}, "additionalValue": PM_REGISTERS},
    "PMA2"                          : {"address": 0x0600, "range": {"min": 0,     "max": 0xFFFF_FFFF},   "readonly": True,  "bits_pos": {"LSB": 0, "LEN": 32}, "additionalValue": PM_REGISTERS},
    "PMA3"                          : {"address": 0x0800, "range": {"min": 0,     "max": 0xFFFF_FFFF},   "readonly": True,  "bits_pos": {"LSB": 0, "LEN": 32}, "additionalValue": PM_REGISTERS},
    "PMA4"                          : {"address": 0x0A00, "range": {"min": 0,     "max": 0xFFFF_FFFF},   "readonly": True,  "bits_pos": {"LSB": 0, "LEN": 32}, "additionalValue": PM_REGISTERS},
    "PMA5"                          : {"address": 0x0C00, "range": {"min": 0,     "max": 0xFFFF_FFFF},   "readonly": True,  "bits_pos": {"LSB": 0, "LEN": 32}, "additionalValue": PM_REGISTERS},
    "PMA6"                          : {"address": 0x0E00, "range": {"min": 0,     "max": 0xFFFF_FFFF},   "readonly": True,  "bits_pos": {"LSB": 0, "LEN": 32}, "additionalValue": PM_REGISTERS},
    "PMA7"                          : {"address": 0x1000, "range": {"min": 0,     "max": 0xFFFF_FFFF},   "readonly": True,  "bits_pos": {"LSB": 0, "LEN": 32}, "additionalValue": PM_REGISTERS},
    "PMA8"                          : {"address": 0x1200, "range": {"min": 0,     "max": 0xFFFF_FFFF},   "readonly": True,  "bits_pos": {"LSB": 0, "LEN": 32}, "additionalValue": PM_REGISTERS},
    "PMA9"                          : {"address": 0x1400, "range": {"min": 0,     "max": 0xFFFF_FFFF},   "readonly": True,  "bits_pos": {"LSB": 0, "LEN": 32}, "additionalValue": PM_REGISTERS},

    "PMC0"                          : {"address": 0x1600, "range": {"min": 0,     "max": 0xFFFF_FFFF},   "readonly": True,  "bits_pos": {"LSB": 0, "LEN": 32}, "additionalValue": PM_REGISTERS},
    "PMC1"                          : {"address": 0x1800, "range": {"min": 0,     "max": 0xFFFF_FFFF},   "readonly": True,  "bits_pos": {"LSB": 0, "LEN": 32}, "additionalValue": PM_REGISTERS},
    "PMC2"                          : {"address": 0x1a00, "range": {"min": 0,     "max": 0xFFFF_FFFF},   "readonly": True,  "bits_pos": {"LSB": 0, "LEN": 32}, "additionalValue": PM_REGISTERS},
    "PMC3"                          : {"address": 0x1c00, "range": {"min": 0,     "max": 0xFFFF_FFFF},   "readonly": True,  "bits_pos": {"LSB": 0, "LEN": 32}, "additionalValue": PM_REGISTERS},
    "PMC4"                          : {"address": 0x1e00, "range": {"min": 0,     "max": 0xFFFF_FFFF},   "readonly": True,  "bits_pos": {"LSB": 0, "LEN": 32}, "additionalValue": PM_REGISTERS},
    "PMC5"                          : {"address": 0x2000, "range": {"min": 0,     "max": 0xFFFF_FFFF},   "readonly": True,  "bits_pos": {"LSB": 0, "LEN": 32}, "additionalValue": PM_REGISTERS},
    "PMC6"                          : {"address": 0x2200, "range": {"min": 0,     "max": 0xFFFF_FFFF},   "readonly": True,  "bits_pos": {"LSB": 0, "LEN": 32}, "additionalValue": PM_REGISTERS},
    "PMC7"                          : {"address": 0x2400, "range": {"min": 0,     "max": 0xFFFF_FFFF},   "readonly": True,  "bits_pos": {"LSB": 0, "LEN": 32}, "additionalValue": PM_REGISTERS},
    "PMC8"                          : {"address": 0x2600, "range": {"min": 0,     "max": 0xFFFF_FFFF},   "readonly": True,  "bits_pos": {"LSB": 0, "LEN": 32}, "additionalValue": PM_REGISTERS},
    "PMC9"                          : {"address": 0x2800, "range": {"min": 0,     "max": 0xFFFF_FFFF},   "readonly": True,  "bits_pos": {"LSB": 0, "LEN": 32}, "additionalValue": PM_REGISTERS},
}   