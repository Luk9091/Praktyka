# IPBus interface and cli
This file describe how work and how use IP cli interface.

## COMMANDS:
- [x] `ip (ADDRESS PORT)`
- [x] `status`
- [x] `read reg value`
    - [x] `--FIFO`
- [x] `write reg`
    - [ ] `--FIFO`
    - [ ] `-n`
- [x] `RMWbits reg AND OR`
- [x] `RMWsum reg ADD`

## File operation:
Example:
```bash
python cli.py ${file} -o ${output_file}
```


## IPBus interface function:
- [x] read status
- [x] read
- [x] write
- [x] fifo read
- [x] fifo write
- [x] read modify write bits
- [x] read modify write sum
- [ ] configuration read
- [ ] configuration write
