# Uni-T UT210E

## Introduction

The Uni-T UT210E[1] is a cost-effective clamp multimeter. It has also been well-studied[2] and can be modified relatively easily, knowing the correct EEPROM memory addresses and corresponding byte values.

## Installation

To install, clone this repo, and run `make`:

```
git clone https://github.com/mkrupcale/ut210e.git
cd ut210e
make
```

This will read the original EEPROM image, `bin/orig.bin`, and produce the modified image, `bin/mod.bin`. To read and write to the EEPROM, ch341eeprom[3] must be present.

### Dependencies

 - Python 3
 - ch341eeprom[3]

## Usage

The CH341A flash programmer is connected to the computer via USB and to the UT210 EEPROM via SOIC8 test clip cable. Once connected, ch341eeprom[3] can read and write the binary flash EEPROM image.

In further detail:

1. Connect and fasten the SOP8 board to the CH341A programmer. The SOP8 board pin 1 should be farthest from the USB connector and adjacent to the fastener.
2. Connect the SOIC8 test clip cable to the SOP8 board. The red wire should be connected to pin 1.
3. Connect the SOIC8 test clip to the UT210E EEPROM. The test clip pin 1, indicated by the red wire, should be connected to EEPROM pin 1, indicated by the dot.
4. Connect the CH341A programmer to the computer USB
5. Read or write the EEPROM image. This can be done easily using `scripts/ch341eeprom.sh`.

## License

The contents of this repository are licensed under the MIT license, except where otherwise noted.

## References

1. [Uni-T UT210E](http://www.uni-trend.com/html/product/General_Meters/digitalclampmeters/UT210_Series/UT210E.html)
2. [bdlow/UT210E](https://github.com/bdlow/UT210E)
3. [plumbum/ch341eeprom](https://github.com/plumbum/ch341eeprom)
