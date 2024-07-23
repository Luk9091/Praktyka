# It a simple script to easier add new registers.
# New register are stored in reg_address.txt file.

def str_to_int(string: str):
    if string == "max":
        return 0xFFFF_FFFF

    if string.startswith("0x"):
        return int(string[2:], 16)
    elif string.startswith("0b"):
        return int(string[2:], 2)
    return int(string)


try:
    while True:
        name = input("Enter the name: ").upper()
        address = str_to_int(input("Enter the address: "))
        minimum = str_to_int(input("Enter the minimum value: "))
        maximum = str_to_int(input("Enter the maximum value: "))
        readonly = input("Is it read only? (y/N): ").lower() == "y"
        LSB = str_to_int(input("Enter the LSB: "))
        LEN = str_to_int(input("Enter the LEN: "))
        additionalValue = input("Enter additional value (None | PM | CHANNEL [number]): ")
        if additionalValue == "" or additionalValue.lower() == "none":
            additionalValue = "None"
        elif additionalValue.isnumeric():
            additionalValue = f"CHANNELS_{additionalValue}"
        elif additionalValue.lower() == "pm":
            additionalValue = "PM_REGISTERS"
        else:
            additionalValue = "None"

        out = """"%s"     : {"address": 0x%04X, "range": {"min": %10i,     "max": %10i},    "readonly": %s, "bits_pos": {"LSB": %2i, "LEN": %2i}, "additionalValue": %s},\n""" % (name, address, minimum, maximum, readonly, LSB, LEN, additionalValue)
        with open("reg_address.txt", "a") as f:
            f.write(out)
        print(out)
        print()
except KeyboardInterrupt:
    print("Goodbye")
