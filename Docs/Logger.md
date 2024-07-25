# IPBus logger
It a simple program to IPBus sever to log avery data transaction.


## Parameters
Set sever ip address:
- `--eth [ethernet interface]`: Take address from ethernet interface.
- `--ip [ip address]`: Set ip address manually.
- `--port [port]`: Set port number.
Default address is `localhost` and port is `50001`.


## File format:
The log file is a simple cvs text file with the following format:
```
date with hour,sender address, sender port, first register address, data, data, data, ...
```
