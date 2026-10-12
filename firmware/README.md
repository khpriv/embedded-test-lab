## Details
| Item	| Details |
| --- | --- |
| Board	| NUCLEO-F446RE |
| UART	| USART2, PA2/PA3, 115200 8N1 via ST-LINK VCP |
| OLED	| SSD1306, I²C1, PB8/PB9, address 0x3D |
| Build	| Open CubeIDE project, build, flash using ST-LINK |
| Protocol	| GET_TEMP, SET_TEMP, GET_LIMIT, SET_LIMIT, GET_STATUS, SET_STATUS, RESET |
| Fault injection	| FIT_DELAY command, delayed responses, experimental |

## Status
This firmware is done to support embedded test framework exercise only.
OLED implementation is experimental and should be treated as such.