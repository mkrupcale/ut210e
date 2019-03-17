#!/usr/bin/python3
# -*- coding: utf-8 -*-

# SPDX-License-Identifier: MIT
# Copyright 2019 Matthew Krupcale <mkrupcale@matthewkrupcale.com>

from argparse import ArgumentParser, RawTextHelpFormatter
from itertools import chain

HEX_BYTE_FORMAT_STRING = "0x%02x"

C24C02_NUM_BYTES = 2*2**10 / 8 # 2 Kbit EEPROM

# bytes are stored little-endian
DM1106EN_BYTE_ORDER = 'little'

MAX_CURRENT_ADDRESS_LOWER_BOUND                                    = 0x07
MAX_CURRENT_ADDRESS_UPPER_BOUND                                    = 0x08
FULL_RANGE_COUNTS_ADDRESS_LOWER_BOUND                              = 0x10
FULL_RANGE_COUNTS_ADDRESS_UPPER_BOUND                              = 0x11
RANGE_SWITCH_UPPER_LIMIT_ADDRESS_LOWER_BOUND                       = 0x12
RANGE_SWITCH_UPPER_LIMIT_ADDRESS_UPPER_BOUND                       = 0x13
RANGE_SWITCH_LOWER_LIMIT_ADDRESS_LOWER_BOUND                       = 0x14
RANGE_SWITCH_LOWER_LIMIT_ADDRESS_UPPER_BOUND                       = 0x15
DC_VOLTAGE_OVERLIMIT_THRESHOLD_ADDRESS                             = 0x16
AC_VOLTAGE_OVERLIMIT_THRESHOLD_ADDRESS                             = 0x17
DC_VOLTAGE_OVERLIMIT_ALARM_THRESHOLD_ADDRESS                       = 0x18
AC_VOLTAGE_OVERLIMIT_ALARM_THRESHOLD_ADDRESS                       = 0x19
MILLIAMP_LEVEL_HIGH_CURRENT_ALARM_THRESHOLD_ADDRESS                = 0x1b
AMP_LEVEL_HIGH_CURRENT_ALARM_THRESHOLD_ADDRESS                     = 0x1c
LOW_CURRENT_CALIBRATION_ADJUSTMENT_RATIO_ADDRESS_LOWER_BOUND       = 0x50
LOW_CURRENT_CALIBRATION_ADJUSTMENT_RATIO_ADDRESS_UPPER_BOUND       = 0x51
MED_CURRENT_CALIBRATION_ADJUSTMENT_RATIO_ADDRESS_LOWER_BOUND       = 0x52
MED_CURRENT_CALIBRATION_ADJUSTMENT_RATIO_ADDRESS_UPPER_BOUND       = 0x53
HIGH_CURRENT_CALIBRATION_ADJUSTMENT_RATIO_ADDRESS_LOWER_BOUND      = 0x54
HIGH_CURRENT_CALIBRATION_ADJUSTMENT_RATIO_ADDRESS_UPPER_BOUND      = 0x55
VERY_HIGH_CURRENT_CALIBRATION_ADJUSTMENT_RATIO_ADDRESS_LOWER_BOUND = 0x56
VERY_HIGH_CURRENT_CALIBRATION_ADJUSTMENT_RATIO_ADDRESS_UPPER_BOUND = 0x57
NON_CONTACT_VOLTAGE_VOLT_LEVEL_ADDRESS                             = 0x9c
NON_CONTACT_VOLTAGE_MILLIVOLT_LEVEL_ADDRESS                        = 0xac

OEM_VALID_IMAGE = dict()

# 1000 ( * 100 mA ) = 0x03e8
OEM_MAX_CURRENT_LOW_BYTE                             = {MAX_CURRENT_ADDRESS_LOWER_BOUND: 0xe8}
OEM_MAX_CURRENT_HIGH_BYTE                            = {MAX_CURRENT_ADDRESS_UPPER_BOUND: 0x03}
# 6000 = 0x1770
OEM_FULL_RANGE_COUNTS_LOW_BYTE                       = {FULL_RANGE_COUNTS_ADDRESS_LOWER_BOUND: 0x70}
OEM_FULL_RANGE_COUNTS_HIGH_BYTE                      = {FULL_RANGE_COUNTS_ADDRESS_UPPER_BOUND: 0x17}
# 2200 = 0x0898
OEM_RANGE_SWITCH_UPPER_LIMIT_LOW_BYTE                = {RANGE_SWITCH_UPPER_LIMIT_ADDRESS_LOWER_BOUND: 0x98}
OEM_RANGE_SWITCH_UPPER_LIMIT_HIGH_BYTE               = {RANGE_SWITCH_UPPER_LIMIT_ADDRESS_UPPER_BOUND: 0x08}
# 190 = 0x00be
OEM_RANGE_SWITCH_LOWER_LIMIT_LOW_BYTE                = {RANGE_SWITCH_LOWER_LIMIT_ADDRESS_LOWER_BOUND: 0xbe}
OEM_RANGE_SWITCH_LOWER_LIMIT_HIGH_BYTE               = {RANGE_SWITCH_LOWER_LIMIT_ADDRESS_UPPER_BOUND: 0x00}

# 61 ( * 10 V) = 0x3d
OEM_DC_VOLTAGE_OVERLIMIT_THRESHOLD_BYTE              = {DC_VOLTAGE_OVERLIMIT_THRESHOLD_ADDRESS: 0x3d}
# 61 ( * 10 V) = 0x3d
OEM_AC_VOLTAGE_OVERLIMIT_THRESHOLD_BYTE              = {AC_VOLTAGE_OVERLIMIT_THRESHOLD_ADDRESS: 0x3d}
# 60 ( * 10 V) = 0x3c
OEM_DC_VOLTAGE_OVERLIMIT_ALARM_THRESHOLD_BYTE        = {DC_VOLTAGE_OVERLIMIT_ALARM_THRESHOLD_ADDRESS: 0x3c}
# 60 ( * 10 V) = 0x3c
OEM_AC_VOLTAGE_OVERLIMIT_ALARM_THRESHOLD_BYTE        = {AC_VOLTAGE_OVERLIMIT_ALARM_THRESHOLD_ADDRESS: 0x3c}

# 255 ( * 100 mA ) = 0xff
OEM_MILLIAMP_LEVEL_HIGH_CURRENT_ALARM_THRESHOLD_BYTE = {MILLIAMP_LEVEL_HIGH_CURRENT_ALARM_THRESHOLD_ADDRESS: 0xff}
# 10 ( * 1 A ) = 0x0a
OEM_AMP_LEVEL_HIGH_CURRENT_ALARM_THRESHOLD_BYTE      = {AMP_LEVEL_HIGH_CURRENT_ALARM_THRESHOLD_ADDRESS: 0x0a}

OEM_NON_CONTACT_VOLTAGE_VOLT_BYTE                    = {NON_CONTACT_VOLTAGE_VOLT_LEVEL_ADDRESS: 0x00}
OEM_NON_CONTACT_VOLTAGE_MILLIVOLT_BYTE               = {NON_CONTACT_VOLTAGE_MILLIVOLT_LEVEL_ADDRESS: 0x00}

OEM_VALID_IMAGE.update(OEM_MAX_CURRENT_LOW_BYTE)
OEM_VALID_IMAGE.update(OEM_MAX_CURRENT_HIGH_BYTE)
OEM_VALID_IMAGE.update(OEM_FULL_RANGE_COUNTS_LOW_BYTE)
OEM_VALID_IMAGE.update(OEM_FULL_RANGE_COUNTS_HIGH_BYTE)
OEM_VALID_IMAGE.update(OEM_RANGE_SWITCH_UPPER_LIMIT_LOW_BYTE)
OEM_VALID_IMAGE.update(OEM_RANGE_SWITCH_UPPER_LIMIT_HIGH_BYTE)
OEM_VALID_IMAGE.update(OEM_RANGE_SWITCH_LOWER_LIMIT_LOW_BYTE)
OEM_VALID_IMAGE.update(OEM_RANGE_SWITCH_LOWER_LIMIT_HIGH_BYTE)
OEM_VALID_IMAGE.update(OEM_DC_VOLTAGE_OVERLIMIT_THRESHOLD_BYTE)
OEM_VALID_IMAGE.update(OEM_AC_VOLTAGE_OVERLIMIT_THRESHOLD_BYTE)
OEM_VALID_IMAGE.update(OEM_DC_VOLTAGE_OVERLIMIT_ALARM_THRESHOLD_BYTE)
OEM_VALID_IMAGE.update(OEM_AC_VOLTAGE_OVERLIMIT_ALARM_THRESHOLD_BYTE)
OEM_VALID_IMAGE.update(OEM_MILLIAMP_LEVEL_HIGH_CURRENT_ALARM_THRESHOLD_BYTE)
OEM_VALID_IMAGE.update(OEM_AMP_LEVEL_HIGH_CURRENT_ALARM_THRESHOLD_BYTE)
OEM_VALID_IMAGE.update(OEM_NON_CONTACT_VOLTAGE_VOLT_BYTE)
OEM_VALID_IMAGE.update(OEM_NON_CONTACT_VOLTAGE_MILLIVOLT_BYTE)

# mode selection

SELECT_MODE_BASE_ADDRESS = 0x80
NUM_SELECT_MODES = 4
SELECT_BUTTON_BASE_ADDRESSES = [SELECT_MODE_BASE_ADDRESS + (x << 4) for x in range(0, NUM_SELECT_MODES)]
LOW_CURRENT_MODE = '2A'
MED_CURRENT_MODE = '20A'
HIGH_CURRENT_MODE = '100A'
NON_CONTACT_VOLTAGE_MODE = 'NCV'
VOLTAGE_MODE = 'V'
MISC_MODE = 'misc'
MODE_SELECTOR_ADDRESS_OFFSET = {
    LOW_CURRENT_MODE: 0x07,
    MED_CURRENT_MODE: 0x0b,
    NON_CONTACT_VOLTAGE_MODE: 0x0c,
    HIGH_CURRENT_MODE: 0x0d,
    VOLTAGE_MODE: 0x0e,
    MISC_MODE: 0x0f
}

for select in SELECT_BUTTON_BASE_ADDRESSES[0:2]:
    for mode in chain(range(0x00, MODE_SELECTOR_ADDRESS_OFFSET[LOW_CURRENT_MODE]), range(MODE_SELECTOR_ADDRESS_OFFSET[LOW_CURRENT_MODE]+1, MODE_SELECTOR_ADDRESS_OFFSET[MED_CURRENT_MODE])):
        OEM_VALID_IMAGE.update({select+mode: 0x00})
for select in SELECT_BUTTON_BASE_ADDRESSES[2:]:
    for mode in range(0x00, MODE_SELECTOR_ADDRESS_OFFSET[MISC_MODE]):
        OEM_VALID_IMAGE.update({select+mode: 0x00})

MEASUREMENT_FUNCTION_CODES = {
    'ACmV': 0x02,
    'DCV without mV': 0x03,
    'ACV without mV': 0x04,
    'DCV with mV': 0x05,
    'ACV with mV': 0x06,
    'R': 0x07,
    'continuity': 0x09,
    'diode': 0x0a,
    'capacitance': 0x0b,
    'DCA 6.000A': 0x16,
    'ACA 6.000A': 0x17,
    'DCA 60.00A': 0x18,
    'ACA 60.00A': 0x19,
    'DCA 600.0A': 0x1a,
    'ACA 600.0A': 0x1b,
    'DCA 6000A': 0x1c,
    'ACA 6000A': 0x1d,
    'NCV': 0x1e
}

OEM_VALID_IMAGE.update({SELECT_BUTTON_BASE_ADDRESSES[0]+MODE_SELECTOR_ADDRESS_OFFSET[LOW_CURRENT_MODE]: MEASUREMENT_FUNCTION_CODES['ACA 6.000A']})
OEM_VALID_IMAGE.update({SELECT_BUTTON_BASE_ADDRESSES[1]+MODE_SELECTOR_ADDRESS_OFFSET[LOW_CURRENT_MODE]: MEASUREMENT_FUNCTION_CODES['DCA 6.000A']})
OEM_VALID_IMAGE.update({SELECT_BUTTON_BASE_ADDRESSES[0]+MODE_SELECTOR_ADDRESS_OFFSET[MED_CURRENT_MODE]: MEASUREMENT_FUNCTION_CODES['ACA 60.00A']})
OEM_VALID_IMAGE.update({SELECT_BUTTON_BASE_ADDRESSES[1]+MODE_SELECTOR_ADDRESS_OFFSET[MED_CURRENT_MODE]: MEASUREMENT_FUNCTION_CODES['DCA 60.00A']})
OEM_VALID_IMAGE.update({SELECT_BUTTON_BASE_ADDRESSES[0]+MODE_SELECTOR_ADDRESS_OFFSET[NON_CONTACT_VOLTAGE_MODE]: MEASUREMENT_FUNCTION_CODES['NCV']})
OEM_VALID_IMAGE.update({SELECT_BUTTON_BASE_ADDRESSES[1]+MODE_SELECTOR_ADDRESS_OFFSET[NON_CONTACT_VOLTAGE_MODE]: 0x00})
OEM_VALID_IMAGE.update({SELECT_BUTTON_BASE_ADDRESSES[0]+MODE_SELECTOR_ADDRESS_OFFSET[HIGH_CURRENT_MODE]: MEASUREMENT_FUNCTION_CODES['ACA 600.0A']})
OEM_VALID_IMAGE.update({SELECT_BUTTON_BASE_ADDRESSES[1]+MODE_SELECTOR_ADDRESS_OFFSET[HIGH_CURRENT_MODE]: MEASUREMENT_FUNCTION_CODES['DCA 600.0A']})
OEM_VALID_IMAGE.update({SELECT_BUTTON_BASE_ADDRESSES[0]+MODE_SELECTOR_ADDRESS_OFFSET[VOLTAGE_MODE]: MEASUREMENT_FUNCTION_CODES['ACV without mV']})
OEM_VALID_IMAGE.update({SELECT_BUTTON_BASE_ADDRESSES[1]+MODE_SELECTOR_ADDRESS_OFFSET[VOLTAGE_MODE]: MEASUREMENT_FUNCTION_CODES['DCV with mV']})
OEM_VALID_IMAGE.update({SELECT_BUTTON_BASE_ADDRESSES[0]+MODE_SELECTOR_ADDRESS_OFFSET[MISC_MODE]: MEASUREMENT_FUNCTION_CODES['R']})
OEM_VALID_IMAGE.update({SELECT_BUTTON_BASE_ADDRESSES[1]+MODE_SELECTOR_ADDRESS_OFFSET[MISC_MODE]: MEASUREMENT_FUNCTION_CODES['continuity']})
OEM_VALID_IMAGE.update({SELECT_BUTTON_BASE_ADDRESSES[2]+MODE_SELECTOR_ADDRESS_OFFSET[MISC_MODE]: MEASUREMENT_FUNCTION_CODES['diode']})
OEM_VALID_IMAGE.update({SELECT_BUTTON_BASE_ADDRESSES[3]+MODE_SELECTOR_ADDRESS_OFFSET[MISC_MODE]: MEASUREMENT_FUNCTION_CODES['capacitance']})

MIN_MAX_COUNTS = 2000
MAX_MAX_COUNTS = 10000
DTM0660L_MAX_MAX_COUNTS = 6000
MIN_MAX_CURRENT = 1000  #  1000 * 100 mA = 100 A
MAX_MAX_CURRENT = 10000 # 10000 * 100 mA = 1000 A
DTM0660L_MAX_MAX_CURRENT = 6000 # 6000 * 100 mA = 600 A
MIN_AMP_LEVEL_HIGH_CURRENT_ALARM_THRESHOLD = 0x0a # 10 ( * 1 A) = 0x0a
MAX_AMP_LEVEL_HIGH_CURRENT_ALARM_THRESHOLD = 0xff # 255 ( * 1 A ) = 0xff
DEFAULT_AMP_LEVEL_HIGH_CURRENT_ALARM_THRESHOLD = 0x64 # 100 ( * 1 A ) = 0x64

def _create_parser():
    parser = ArgumentParser(description="""Modifies the given UT210E EEPROM flash image to:\n
  - Increase the number of counts
  - Increase the maximum current range
  - Enable mV voltage output
  - Enable "dotless" low-current mode to increase range of counts in low-current mode with zeroing
  - Enable NVC mode level measurement
""",
    formatter_class=RawTextHelpFormatter)
    parser.add_argument('original',
                        help="Original flash EEPROM image for input")
    parser.add_argument('modified',
                        help="Modified flash EEPROM image for output")
    parser.add_argument('-c', '--counts',
                        type=int,
                        default=MAX_MAX_COUNTS,
                        help="Maximum number of counts to display")
    parser.add_argument('--max-current',
                        type=int,
                        default=MAX_MAX_CURRENT,
                        help="Maximum current in 100 mA units")
    parser.add_argument('--amp-level-high-current-alarm-threshold',
                        type=int,
                        default=DEFAULT_AMP_LEVEL_HIGH_CURRENT_ALARM_THRESHOLD,
                        help="Amp-level high-current alarm threshold in 1 A units")
    parser.add_argument('--no-enable-millivolts',
                        action='store_true',
                        default=False,
                        help="Do not enable the mV voltage output")
    parser.add_argument('--no-enable-dotless-low-current',
                        action='store_true',
                        default=False,
                        help="Do not enable the low-current 'dotless' mode")
    parser.add_argument('--no-enable-non-contact-voltage-level',
                        action='store_true',
                        default=False,
                        help="Do not enable the NVC level measurements")
    parser.add_argument('-V', '--verbose',
                        action='store_true',
                        default=False,
                        help="Enable verbose output")
    return parser

def parse_args():
    return _create_parser().parse_args()

def _validate_args(args):
    if args.counts < MIN_MAX_COUNTS or args.counts > MAX_MAX_COUNTS:
        raise ValueError("Maximum counts must be in the range [%d, %d]" % (MIN_MAX_COUNTS, MAX_MAX_COUNTS))
    if args.counts > DTM0660L_MAX_MAX_COUNTS:
        asic = input("Requested counts is greater than supported by DTM0660L ASIC (%d > %d). Confirm is this image for DM1106EN ASIC? (y/n) " % (args.counts, DTM0660L_MAX_MAX_COUNTS))
        if asic.lower()[0] != 'y':
            raise ValueError("Only DM1106EN ASIC supports more than %d counts" % (DTM0660L_MAX_MAX_COUNTS))
    if args.max_current < MIN_MAX_CURRENT or args.max_current > MAX_MAX_CURRENT:
        raise ValueError("Maximum current must be in the range [%d, %d]" % (MIN_MAX_CURRENT, MAX_MAX_CURRENT))
    if args.max_current > DTM0660L_MAX_MAX_CURRENT:
        asic = input("Requested max current is greater than supported by DTM0660L ASIC (%d A > %d A). Confirm is this image for DM1106EN ASIC? (y/n) " % (args.max_current // 10, DTM0660L_MAX_MAX_CURRENT // 10))
        if asic.lower()[0] != 'y':
            raise ValueError("Only DM1106EN ASIC supports more than %d counts" % (DTM0660L_MAX_MAX_COUNTS))
    if args.amp_level_high_current_alarm_threshold < MIN_AMP_LEVEL_HIGH_CURRENT_ALARM_THRESHOLD or args.amp_level_high_current_alarm_threshold > MAX_AMP_LEVEL_HIGH_CURRENT_ALARM_THRESHOLD:
        raise ValueError("Amp-level high-current alarm threshold must be in the range [%d, %d]" % (MIN_AMP_LEVEL_HIGH_CURRENT_ALARM_THRESHOLD, MAX_AMP_LEVEL_HIGH_CURRENT_ALARM_THRESHOLD))

def read_image(infile):
    with open(infile, 'rb') as f:
        return bytearray(f.read())

def _validate_image_size(image):
    if len(image) != C24C02_NUM_BYTES:
        raise ValueError("Image size should be %d bytes" % C24C02_NUM_BYTES)

def _validate_oem_image(image):
    _validate_image_size(image)
    for a in OEM_VALID_IMAGE:
        if image[a] != OEM_VALID_IMAGE[a]:
            format_str = "Image is not a valid OEM image: expected address %s = %s (got %s)" % (HEX_BYTE_FORMAT_STRING, HEX_BYTE_FORMAT_STRING, HEX_BYTE_FORMAT_STRING)
            raise ValueError(format_str % (a, OEM_VALID_IMAGE[a], image[a]))

def modify_counts(image, counts):
    num_bytes = FULL_RANGE_COUNTS_ADDRESS_UPPER_BOUND - FULL_RANGE_COUNTS_ADDRESS_LOWER_BOUND + 1
    image[FULL_RANGE_COUNTS_ADDRESS_LOWER_BOUND:FULL_RANGE_COUNTS_ADDRESS_UPPER_BOUND+1] = counts.to_bytes(num_bytes, DM1106EN_BYTE_ORDER)
    _modify_range_switch_limits(image, counts)

def _modify_range_switch_limits(image, counts):
    def upper_limit(c):
        return c + 200
    def lower_limit(c):
        c = c // 10
        if c >= 600:
            return c - 20
        else:
            return c - 10
    num_bytes = RANGE_SWITCH_UPPER_LIMIT_ADDRESS_UPPER_BOUND - RANGE_SWITCH_UPPER_LIMIT_ADDRESS_LOWER_BOUND + 1
    image[RANGE_SWITCH_UPPER_LIMIT_ADDRESS_LOWER_BOUND:RANGE_SWITCH_UPPER_LIMIT_ADDRESS_UPPER_BOUND+1] = (upper_limit(counts)).to_bytes(num_bytes, DM1106EN_BYTE_ORDER)
    num_bytes = RANGE_SWITCH_LOWER_LIMIT_ADDRESS_UPPER_BOUND - RANGE_SWITCH_LOWER_LIMIT_ADDRESS_LOWER_BOUND + 1
    image[RANGE_SWITCH_LOWER_LIMIT_ADDRESS_LOWER_BOUND:RANGE_SWITCH_LOWER_LIMIT_ADDRESS_UPPER_BOUND+1] = (lower_limit(counts)).to_bytes(num_bytes, DM1106EN_BYTE_ORDER)

def modify_max_current(image, max_current):
    num_bytes = MAX_CURRENT_ADDRESS_UPPER_BOUND - MAX_CURRENT_ADDRESS_LOWER_BOUND + 1
    image[MAX_CURRENT_ADDRESS_LOWER_BOUND:MAX_CURRENT_ADDRESS_UPPER_BOUND+1] = max_current.to_bytes(num_bytes, DM1106EN_BYTE_ORDER)

def enable_millivolts(image):
    image[SELECT_BUTTON_BASE_ADDRESSES[0]+MODE_SELECTOR_ADDRESS_OFFSET[VOLTAGE_MODE]] = MEASUREMENT_FUNCTION_CODES['ACV with mV']

def enable_dotless_low_current(image):
    image[SELECT_BUTTON_BASE_ADDRESSES[0]+MODE_SELECTOR_ADDRESS_OFFSET[LOW_CURRENT_MODE]] = MEASUREMENT_FUNCTION_CODES['ACA 6000A']
    image[SELECT_BUTTON_BASE_ADDRESSES[1]+MODE_SELECTOR_ADDRESS_OFFSET[LOW_CURRENT_MODE]] = MEASUREMENT_FUNCTION_CODES['DCA 6000A']
    image[SELECT_BUTTON_BASE_ADDRESSES[2]+MODE_SELECTOR_ADDRESS_OFFSET[LOW_CURRENT_MODE]] = MEASUREMENT_FUNCTION_CODES['ACA 6.000A']
    image[SELECT_BUTTON_BASE_ADDRESSES[3]+MODE_SELECTOR_ADDRESS_OFFSET[LOW_CURRENT_MODE]] = MEASUREMENT_FUNCTION_CODES['DCA 6.000A']
    _copy_low_current_calibration(image)

def _copy_low_current_calibration(image):
    num_bytes = LOW_CURRENT_CALIBRATION_ADJUSTMENT_RATIO_ADDRESS_UPPER_BOUND - LOW_CURRENT_CALIBRATION_ADJUSTMENT_RATIO_ADDRESS_LOWER_BOUND + 1
    low_current_calibration_adjustment_ratio = int.from_bytes(image[LOW_CURRENT_CALIBRATION_ADJUSTMENT_RATIO_ADDRESS_LOWER_BOUND:LOW_CURRENT_CALIBRATION_ADJUSTMENT_RATIO_ADDRESS_UPPER_BOUND+1], DM1106EN_BYTE_ORDER)
    num_bytes = VERY_HIGH_CURRENT_CALIBRATION_ADJUSTMENT_RATIO_ADDRESS_UPPER_BOUND - VERY_HIGH_CURRENT_CALIBRATION_ADJUSTMENT_RATIO_ADDRESS_LOWER_BOUND + 1
    image[VERY_HIGH_CURRENT_CALIBRATION_ADJUSTMENT_RATIO_ADDRESS_LOWER_BOUND:VERY_HIGH_CURRENT_CALIBRATION_ADJUSTMENT_RATIO_ADDRESS_UPPER_BOUND+1] = low_current_calibration_adjustment_ratio.to_bytes(num_bytes, DM1106EN_BYTE_ORDER)

def set_amp_level_high_current_alarm_threshold(image, threshold):
    image[AMP_LEVEL_HIGH_CURRENT_ALARM_THRESHOLD_ADDRESS] = threshold

def enable_non_contact_voltage_level(image):
    image[SELECT_BUTTON_BASE_ADDRESSES[1]+MODE_SELECTOR_ADDRESS_OFFSET[NON_CONTACT_VOLTAGE_MODE]] = MEASUREMENT_FUNCTION_CODES['ACmV']
    image[SELECT_BUTTON_BASE_ADDRESSES[2]+MODE_SELECTOR_ADDRESS_OFFSET[NON_CONTACT_VOLTAGE_MODE]] = MEASUREMENT_FUNCTION_CODES['ACA 6000A']

def write_image(outfile, image):
    with open(outfile, 'wb') as f:
        b = f.write(image)
        if b != C24C02_NUM_BYTES:
            raise RuntimeError("Image written should be %d bytes: %d bytes written" % (C24C02_NUM_BYTES, b))

def main():
    args = parse_args()
    _validate_args(args)
    if args.verbose:
        print("Reading image '%s'" % args.original)
    image = read_image(args.original)
    if args.verbose:
        print("Validating OEM image '%s'" % args.original)
    _validate_oem_image(image)
    if args.verbose:
        print("Setting display counts to %d" % args.counts)
    modify_counts(image, args.counts)
    if args.verbose:
        print("Setting maximum current to %d A" % (args.max_current // 10))
    modify_max_current(image, args.max_current)
    if args.verbose:
        print("Setting Amp-level high-current alarm threshold to %d A" % args.amp_level_high_current_alarm_threshold)
    set_amp_level_high_current_alarm_threshold(image, args.amp_level_high_current_alarm_threshold)
    if not args.no_enable_millivolts:
        if args.verbose:
            print("Enabling AC/DC millivolts")
        enable_millivolts(image)
    if not args.no_enable_dotless_low_current:
        if args.verbose:
            print("Enabling low-current 'dotless' mode")
        enable_dotless_low_current(image)
    if not args.no_enable_non_contact_voltage_level:
        if args.verbose:
            print("Enabling NCV level measurement")
        enable_non_contact_voltage_level(image)
    if args.verbose:
        print("Validating modified image size")
    _validate_image_size(image)
    if args.verbose:
        print("Writing modified image '%s'" % args.modified)
    write_image(args.modified, image)

if __name__ == '__main__':
    main()
