# IPBus CLI
The IPBus CLI is a command line interface that allows users to interact with the IPBus system.
The CLI is a Python script that can be run from the command line.
The CLI is used to send commands to the IPBus system and to receive responses from the IPBus system.
The CLI is used to configure the IPBus system, to read and write registers, and to perform other tasks.

Register name could be find in [this file](https://onedrive.live.com/view.aspx?resid=7E7CBC355FE4EA69%21128&authkey=!AIHkXzLSmyeY43E), column: ***C***, sheet: ***TCM*** and ***PM***.\
If you wand add register use **reg_adder.py** script. Copy display value to **register.py** file in correct dictionary.

# Table of contents
- [Usage](#usage)
- [Commands](#commands)
    - [IP](#ip)
    - [Status](#status)
    - [Read](#read)
    - [Write](#write)
    - [RMWBits](#rmwbits)
    - [RMWSum](#rmwsum)
    - [SetBits and ClearBits](#setbits-and-clearbits)
- [Run parameters](#run-parameters)
    - [Read data from file](#read-data-from-file)
    - [Write data to file](#write-data-to-file)
- [FAQ](#faq)
    - [How enabled PM module?](#how-enabled-pm-module)


## Usage
The IPBus CLI is a Python script that can be run from the command line.
```bash
    python cli.py
```



## Commands:
- `help ([command])` - display help information,
    - `--help` - display help information,
- `exit` - exit the CLI, its posile to use `Ctrl+C` or `Ctrl+D` to exit,
- [`ip [ip] ([port])`](#ip) - set the IP address and port of the IPBus system,
- [`status`](#status) - send status request to the IPBus system and read the response,
- [`read [address | name]`](#read) - read the register value from the IPBus system, additional parameters:
    - `([-n] [value])` - number of registers to read, start reding from `[address | name]`,
    - `([--FIFO])` - read from the FIFO buffer,
    - `([-s])` - display read value as signed integer,
    - `([-H])` or `([-B])` - display read value as hex or binary,
- [`write [address | name] [value] ([value]...)`](#write) - write the register value to the IPBus system, additional parameters:
    - `([-n] [value])` - number of registers to write, start writing from `[address | name]`,
    - `([--FIFO])` - write to the FIFO buffer,
- [`RMWBits [address | name] [ANDmask] [ORmask]`](#rmwbits) - read-modify-write-bits operation, additional parameters:
    - `([-H])` or `([-B])` - display read value as hex or binary,
- [`RMWSum [address | name] [value]`](#rmwsum) - read-modify-write-sum operation, additional parameters:
    - `([-s])` - display read value as signed integer,
    - `([-H])` or `([-B])` - display read value as hex or binary,
- [`setBits [name] [bit]`](#setbits-and-clearbits) - set the bit in the register,
- [`clearBits [name] [bit]`](#setbits-and-clearbits) - clear the bit in the register,


## Run parameters:
- `--help` - display help information,
- `--ip [ip]` - set the IP address and port of the IPBus system, additional param:
    - `([port])` - out IP port, default: *50001*,
- [`-i [file]`](#read-data-from-file) - read commands from the file,
- [`-o [file]`](#write-data-to-file) - write output to the file.

Additionally any command can be passed as a parameter to the shell script, for example:
```bash
    python cli.py read 0x0F --ip 172.20.75.180

# output:
    # Read register 0x0F: xxxxxxxx
```

**Legend:**
- `[arg]` - obligatory arguments,
- `([arg])`- optional arguments,
- `[arg]...` - multiple arguments allowed,
- `[--PARAM]` - full world parameter,
- `[-P]` - short parameter,
- `[-P] [value]` - short parameter with value.


    if len(args) == 0:
# Examples:
## IP
Run the CLI and set the IP address and port of the IPBus system:
```bash
    python cli.py --ip 172.20.75.180
    172.20.75.180 << [command]
#   ^^^^^^^^^^^^^  | ^^^^^^^^^
#   IP address of  | command to
#      device      | the device
```

In previous example, the IP address was set by program parameter, but it is possible to set it by command:
```bash
    python cli.py 
    localhost << ip 172.20.75.180
# Output
    IP address set to 172.20.75.180:50001
```

If you want to set the IP address and port, you need to specify the port:
```bash
    python cli.py --ip 172.20.75.180 80
```
Pure `ip` command display current IP address and port:
```bash
    172.20.75.180 << ip
# Output:
    Current IP: 172.20.75.180:50001
```

## Status
Send status request to the IPBus system and read the response:
```bash
    172.20.75.180 << status
# Output:
    Status OK
```

## Read
Read the register 0x0F from the IPBus system:
By default, the read value is displayed as an unsigned decimal.
```bash
    172.20.75.180 << read 0x0F
# Output:
    xxxxxxxx
    # Read register 0x0F: xxxxxxxx
```

Params `[-H]` or `[-B]` change the display format to hex or binary:
```bash
    172.20.180 << read 0x0F -H
# Output:
    0xXXXXXXXX
    # Read register 0x0F: 0xXXXXXXXX
```
```bash
    172.20.180 << read 0x0F -B
# Output:
    0bXXXXXXXX
    # Read register 0x0F: 0bXXXXXXXX

```

The seconds option is to read the register by its name:\
**Note:** When the register name is used, signed value is automatically detected.
```bash
    172.20.75.180 << read BOARD_STATUS
# Output:
    xxxxxxxx
    # Read register BOARD_STATUS: xxxxxxxx
```

Read multiple register:\
The `[-n]` parameter is used to specify the number of registers to read.\
**Note:** The `[-s]` parameters are used to display every read value as a signed integer. Also `[-H]` and `[-B]` set every read value as hex or binary.
```bash
    172.20.75.180 << read BOARD_STATUS -n 3
# Output: 
    xxxxxxx1, xxxxxxx2, xxxxxxx3
    # Read register BOARD_STATUS    : xxxxxxx1
    # Read register BOARD_STATUS + 1: xxxxxxx2
    # Read register BOARD_STATUS + 2: xxxxxxx3
```

Read from the FIFO buffer:
```bash
    172.20.75.180 << read 0x100 --FIFO -n 3
# Output: xxxxxxx1, xxxxxxx2, xxxxxxx3
    # Read FIFO register
```

In default register name are from **TCM**, if you want to read from **PM** and **channel 2**, you need to specify the register name:
```bash
    172.20.75.180 << read PMA0 ADC0_BASELINE CH02
#                         ^^^^ ^^^^^^^^^^^^^ ^^^^
#                         |    |            Channel
#                         |    Register in PMA0
#                         PM module
# Output:
    # Read register PMA0 ADC0_BASELINE CH02: xxxxxxxx
    # This means PMA0 ADC0_BASELINE CH01 is translate in address 0x20F
```

## Write
Write the value 0x1234 to the register 0x0F:
```bash
    172.20.75.180 << write 0x0F 0x1234
# Output:
    Write successful
```

Write the value 0x1234 to the register by its name:
```bash
    172.20.75.180 << write BOARD_STATUS 0x1234
# Output:
    Write successful
```

Write multiple registers:
```bash
    172.20.75.180 << write BOARD_STATUS 0x01 0x02 0x03
# Output:
    Write successful
```
In register it was write in order: 
- BOARD_STATUS        : 0x01,
- BOARD_STATUS + 1    : 0x02,
- BOARD_STATUS + 2    : 0x03

Also is possible to write to the FIFO buffer:
```bash
    172.20.75.180 << write 0x100 0x01 0x02 0x03 --FIFO
# Output:
    Write successful
```

Signed value is automatically detected, it posable to mixed signed, unsigned, hex and bin value:
```bash
    172.20.75.180 << write -100 0x20, 0b1001
# Output:
    Write successful
```


In default register name are from **TCM**, if you want to write to **PM** and channel 1, you need to specify the register name:
```bash
    172.20.75.180 << write PMA0 CFD_THRESHOLD CH12 300
#                          ^^^^ ^^^^^^^^^^^^^ ^^^^ ^^^
#                          |    |             |    Value
#                          |    |             Channel 12
#                          |    Register in PMA0 
#                          PM module
# Output:
    Write successful
```


## RMWBits
Read-Modify-Write-bits operation and display <u>old</u> value.
Next modify read value and store new value in register.
```
    Y <= X & ANDmask | ORmask
```


```bash
    172.20.75.180 << RMWBits 0x0F 0x0F 0x10
# Output:
    xxxxxxxx
    # Old date from: 0x0F: xxxxxxxx
    # New data in register: 0x1X
```
```bash
    172.20.75.180 << RMWBits BOARD_STATUS 0x0F 0x10
# Output:
    xxxxxxxx
    # Old date from: 0x0F: xxxxxxxx
    # New data in register: 0x1X
```
**Note:** The `[-H]`, `[-B]` parameters are used to display read value as hex or binary.

## RMWSum
Read-Modify-Write-sum operation and display old value.
Next add addend to old value and store new value in register.
```
    Y <= X + addend
```

Similar to RWMBits, but the addend is added to the read value.
```bash
    172.20.75.180 << RMWBits 0x0F 0x0F
# Output:
    xxxxxxxx
    # Old date from: 0x0F: xxxxxxxx
    # New data in register: xxxxxxxx + 0xF
```
```bash
    172.20.75.180 << RMWBits BOARD_STATUS 0x0F
# Output:
    xxxxxxxx
    # Old date from: BOARD_STATUS: xxxxxxxx
    # New data in register: xxxxxxxx + 0xF
```

**Note:** The `[-H]`, `[-B]` parameters are used to display read value as hex or binary.\
**Note:** The `[-s]` similar to **read** command, display read value as signed integer also is optional if get address by name.


## SetBits and ClearBits
Set or clear the bit in the register. In both cases, 
if do not specified bit number, program in default set or clear the first bit.

```bash
    172.20.75.180 << setBits STATUS_OPTIONCODE (0)
# Output:
    Old data from ORA_enable: X
```
```bash
    172.20.75.180 << clearBits STATUS_OPTIONCODE (0)
# Output:
    Old data from ORA_enable: X
```

---
If read register by name, value is moved to only useful bits.
For example register ***ORA_ENABLED***, is only ones bit of ***STATUS_OPTIONCODE*** registers.
So when you read ***ORA_ENABLED***, you get only one bit on output.
```bash
    172.20.75.180 << read ORA_ENABLED
# Output:
    0 or 1
```

**NOT RECOMMENDED**\
Similar behavior is in *write* operation. But when you write to register by name, you set only predefine bits and **<u>other are set to 0</u>**.
```bash
    172.20.75.180 << write ORA_ENABLED 1
# Output:
    Write successful
    # Value in register STATUS_OPTIONCODE: 0x00000004
```

Better way is to use ***setBits*** and ***clearBits*** commands if you want to set or clear only one bit. Or use ***RMWBits*** command if you want to set or clear more than one bit.
```bash
    172.20.25.180 << setBits ORA_enable 0
# Output:
    X
    # Old data from ORA_enable: X
    # New data in register: 0b... X1XX
```
---


# Read data from file
Write a short function that reads data from a file and sends it to the IPBus system is relatively simple.
All upper described commands can be used in the program.

To run command from file, you need to use `-i` parameter:
```bash
    python cli.py -i file.txt
```

Example:
```bash
    read SIDE_A_STATUS
# Output:
#   xxxxxxxx
    setBit CH_MASK_A 0 # allows PM01 exclusion from trigger production
# Output:
#   xxxx
    read SIDE_A_STATUS
# Output:
#   0b... XXX1
```

**Comments**\
As you can see, the comments are also allowed in the file.\
```bash
    # This is comment
    read SIDE_A_STATUS # <- this is function
```

# Write data to file
Store output from the IPBus system to the file is also possible. To do this, you need to use `-o` parameter:
```bash
    python cli.py -o file.txt
```

Example:
```bash
    172.20.75.180 << read SIDE_A_STATUS
# Output
    xxxxxxxx
```
On stdout you get normal output, and in file you get:
```bash
172.20.75.180, read SIDE_A_STATUS, xxxxxxxx
#^^^^^^^^^^^^  ^^^^^^^^^^^^^^^^^^  ^^^^^^^^
# IP address   command             return value
```

Multiple reads are saved in one line.
For example:
```bash
    172.20.75.180 << read SIDE_A_STATUS -n 3
```
Output:
```bash
172.20.75.180, read SIDE_A_STATUS, xxxxxxx1, xxxxxxx2, xxxxxxx3
```

---
As said upper, its possible to use multiple params in one run:
```bash
    python cli.py -i input.txt -o out.csv --ip 172.20.75.180
```
In this case, the program reads commands from `input.txt` file, 
sends them to the IPBus system, and saves the output to `out.csv` file
with additional information.


For example:
input.txt
```bash
read CH_MASK_A
read BOARD_STATUS -n 3
```

out.csv
```bash
172.20.75.180, read CH_MASK_A, 26
172.20.75.180, read BOARD_STATUS -n 3, 15, 16, 17
```



# FAQ:
## How enabled PM module?
For A side:
```bash
172.20.75.180 << setBit SPI_MASK [PM_number]
172.20.75.180 << setBit CH_MASK_A [PM_number]
```

For C side:
```bash
172.20.75.180 << setBit SPI_MASK [PM_number + 10]
172.20.75.180 << setBit CH_MASK_C [PM_number]
```