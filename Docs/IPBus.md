# General description of IPBus communication library

### Table of content
1. [IPBus general description](#1-ipbus-general-description)
2. [Packet Header](#2-packer-header)
3. [Transaction Header](#3-transaction-header)


## 1. IPBus general description
IPBus python module is little communication library with IP device.
Function list:
1. [`IPBus(IP address: str | None, IP port: int | None) -> IPBus`](#11-ipbusipbusip-address-ip-port)
2. [`statusRequest() -> int`](#12-ipbusstatusrequest)
3. [`statusResponse() -> int`](#13-ipbusstatusresponse)
4. [`read(start address: int, nWord: int, FIFO: bool, signed: bool) -> tuple[int, list[int]]`](#14-ipbusreadstart-register-nword-fifo-signed)
5. [`write(start address: int, data: list[int], FIFO: bool) -> int`](#15-ipbuswritestart-register-data-fifo)
6. [`readModifyWriteBites(register address: int, ANDmask: int, ORmask: int) -> int`](#16-ipbusreadmodifywritebitesregister-address-and-mask-or-mask)
7. [`readModifyWriteSum(register address: int, addend: int, signed read: bool) -> int`](#17-ipbusreadmodifywritesumregister-address-addend-singed-read)

#### Transaction info code:
Error code returned by any read/write function.
| Info Code |  Description  |
| :-------: | :-----------: |
| 0x0 | Successful request  |
| 0x1 | Bad header          |
| 0x4 | IPbus read error    |
| 0x5 | IPbus write error   |
| 0x6 | IPbus read timeout  |
| 0x7 | IPbus write timeout |
| 0xf | outbound request    |
| -1  | unknown Info Code   |

### 1.1. IPBus.IPBus(IP address, IP port)
Runs any read command, may throw **socket.TimeoutError** after a default timeout of 1 second.

`@params`:
1. `IP address`: `str` — string destination address, default: *"localhost"*
2. `IP port`: `int` — port number, default: *50001*


### 1.2 IPBus.statusRequest()
Sends a status request to the device.

`@param`:
    `None`

`@return`:
1. `int`: error code:\
    0 if success\
    1 if failed

### 1.3 IPBus.statusResponse()
Reads the answer from the device when a status request is sent by `statusRequest` function.\
On success, the response message is stored in the ***status*** variable in IPBus class.

`@param`:
    `None`

`@return`:
1. `int`: ``packetHeader.packetType``

| Error code | Description |
|:---:|:---:|
| -1| Error transaction |
| 0 | Control Packet |
| 1 | Status Packet |
| 2 | Resend Packet |

### 1.4 IPBus.read(start register, nWord, FIFO, signed)
The function reads data from the device starting from the `start register` address. The data can be read from one register or sequentially from multiple registers. The `FIFO` parameter is used to select the read mode.\
<u>Maximum read size is 255 of 32-bits words.</u>

`@param`:
1. start register: `int` — address first register to read data
2. nWord: `int` — number of read words | default = 1, max = 255
3. FIFO: `bool` — read data from one address | default = False — reading sequence starts at `start register`
4. signed: `bool` — convert read data from <u>unsigned</u> int 32 to signed int 32 | **default: *False***

`@return`: `tuple[int, list[list]]`
1. [transaction info code: `int`](#transaction-info-code)
2. list of read words: `list[int]`

### 1.5 IPBus.write(start register, data, FIFO)
The function writes data to the device starting from the `start register` address. The data can be written to one register or sequentially to multiple registers. The `FIFO` parameter is used to select the write mode.\
<u>Maximum write size is 255 of 32-bits words.</u>

`@param`:
1. start register: `int` — address first register write to
2. data: `list[int] | int` — data to write to the device starting from `start register address`
3. FIFO: `bool` — select if data should be written to one register or sequentially

`@return`: `int`
1. [transaction info code: `int`](#transaction-info-code)

### 1.6 IPBus.readModifyWriteBits(register address, AND mask, OR mask)
The function reads the value from the register, performs the bitwise AND operation with the `AND mask`, then performs the bitwise OR operation with the `OR mask`, and finally writes the result back to the register.
```
    Y <= (X & ANDmask) | ORmask
```

X - value stored in register\
Y - new value written into register


`@param`:
1. register address: `int`
2. AND mask: `int`
3. OR mask: `int`

`@return`: `tuple[int, int]`
1. [transaction info code: `int`](#transaction-info-code)
2. read value before modification: `unsigned int`


### 1.7 IPBus.readModifyWriteSum(register address, addend, signed read)
Read value from `register address`, display it and the next step add `addend` and store it in `register`
```
    Y <= X + addend
```
X - value stored in register\
Y - new value written into register

`@param`:
1. register address: int 
2. addend: int
3. signed read: bool — information on how to interpret the read value, False - as unsigned, True - as signed | **default: *False***

`@return`: `tuple[int, int]`
1. [transaction info code: `int`](#transaction-info-code)
2. read value before modification

---
## 2. Packet Header
The request and reply of an IPbus packet always begins with a 32-­‐bit header. This header has been added in version 2.0 of the protocol in order to support the reliability mechanism. The header contains the packet type, the byte order, the packet ID, a reserved field, and the protocol version.

**Variable**
| Name | Type | Size in bits | Default value |
| :--: | :--: | :----------: | :-----------: |
| packetType      | int |  4 | |
| byteOrder       | int |  4 | 0xF |
| packetID        | int | 16 | |
| rsvd            | int |  4 | 0x0 |
| protocolVersion | int |  4 | 2 |

**Functions**
1. `PacketHeader(packetType: int, id: int = 0)`
    - `@params`
        - packetType:
            | Code | Description |
            |:---:|:---:|
            | 0 | Control Packet |
            | 1 | Status Packet |
            | 2 | Resend Packet |
        - id — number of send packet
2. `toBytesArray(endian: str)`
    - `@params`
        - endian — type of order bytes ("little" or "big") | default: "little"
    - `@return`
        - `bytearray`— bytearray of packet header
3. `fromBytesArray(byteArray: bytearray)`
    - `@params`
        - `byteArray` — bytearray of packet header
    - `@return`
        - None


## 3. Transaction Header
Each IPbus request and reply transaction must start with a 32-­‐bit header. This header contains the transaction type, the number of 32-­‐bit words in the transaction, and an information code.

**Variable**
| Name | Type | Size in bits | Default value |
| :--: | :--: | :----------: | :-----------: |
| protocolVersion | int | 4 | 2 |
| transactionID | int | 16 | |
| words | int | 8 |  |
| typeID | int | 4 |  |
| infoCode | int | 8 | 0xF |

**Functions**
1. `TransactionHeader(transactionType: int, nWords: int, id: int = 0)`
    - `@params`
        - transactionType:
            | Info Code |  Description  |
            | :-------: | :-----------: |
            | 0x0 | Successful request  |
            | 0x1 | Bad header          |
            | 0x4 | IPbus read error    |
            | 0x5 | IPbus write error   |
            | 0x6 | IPbus read timeout  |
            | 0x7 | IPbus write timeout |
            | 0xf | outbound request    |
            | -1  | unknown Info Code   |
        - nWords — number of words in transaction, maximum: <u>255</u>
        - id — number of send packet
2. `toBytesArray(endian: str)`
    - `@params`
        - endian — type of order bytes ("little" or "big") | default: "little"
    - `@return`
        - `bytearray`— bytearray of transaction header
3. `fromBytesArray(byteArray: bytearray)`
    - `@params`
        - `byteArray` — bytearray of transaction header
    - `@return`
        - None

## 4. Status Packet
This packet is send to device to check if it is still alive. See in protocol documentation for more information.

