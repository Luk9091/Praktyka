#! /usr/bin/bash

python3 cli.py status
python3 cli.py ip

python3 cli.py read 1004
python3 cli.py read 1005

python3 cli.py write 1004 1
python3 cli.py read 1004

python3 cli.py write 1004 10 20
python3 cli.py read 1004 -n 2
python3 cli.py read 1004 -n 2


python3 cli.py write 1004 FFFF0000
python3 cli.py RMWbits 1004 FF000000 000000FF
python3 cli.py read 1004

python3 cli.py write 1005 0
python3 cli.py RMWsum 1005 10
python3 cli.py read 1005