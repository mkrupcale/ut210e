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

#### Hardware

 - Uni-T UT210E
 - CH341A programmer
 - SOP8-DIP8 board
 - SOIC8 test clip
 - Computer with USB

#### Software

 - Python 3
 - ch341eeprom[3]
 - CH341 driver (present in e.g. Linux/BSD post-2009)

## Usage

### Hardware setup

The CH341A flash programmer is connected to the computer via USB and to the UT210E EEPROM via SOIC8 test clip cable. Once connected, ch341eeprom[3] can read and write the binary flash EEPROM image.

In further detail:

1. Connect and fasten the SOP8-DIP8 board to the CH341A programmer. The SOP8-DIP8 board pin 1 should be farthest from the USB connector and adjacent to the fastener so as to align with the 24CXX DIP8 outline on the programmer.
2. Connect the SOIC8 test clip cable to the SOP8-DIP8 board. The red wire should be connected to pin 1.
3. Connect the SOIC8 test clip to the UT210E EEPROM. The EEPROM should be a Microchip DM24C02A SOIC8 device located near the crystal oscillator. The test clip pin 1, indicated by the red wire, should be connected to EEPROM pin 1, indicated by the dot on the top of the EEPROM. You may need to move some of the neighboring capacitors out of the way to attach the test clip.
4. Connect the CH341A programmer to the computer USB
5. Read or write the EEPROM image. This can be done easily using `scripts/ch341eeprom.sh`.

### Software setup

To produce the modified EEPROM image, an original EEPROM image is necessary because there is device-specific calibration data contained in the image. An example original EEPROM image is included at `bin/orig.bin`, as well as its default modified image as produced by `make` at `bin/mod.bin`.

If you want to use this for your own device, you should:

1. Read your device's image as described above
2. Run `make` or `scripts/modify_image.py` directly to customize the desired options
3. Write the produced image to your device as described above

## License

The contents of this repository are licensed under the MIT license, except where otherwise noted.

## References

1. [Uni-T UT210E](http://www.uni-trend.com/html/product/General_Meters/digitalclampmeters/UT210_Series/UT210E.html)
2. [bdlow/UT210E](https://github.com/bdlow/UT210E)
3. [plumbum/ch341eeprom](https://github.com/plumbum/ch341eeprom)
