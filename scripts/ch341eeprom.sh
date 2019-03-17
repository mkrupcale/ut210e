#!/usr/bin/sh

# SPDX-License-Identifier: MIT
# Copyright 2019 Matthew Krupcale <mkrupcale@matthewkrupcale.com>

function print_usage ()
{
    echo "Usage: "
    echo "${BASH_SOURCE} [--help] <command> <options>"
    echo ""
    echo "Options"
    echo "  -h,--help"
    echo "    Prints help"
    echo "  -f,--file <file>"
    echo "    Input or output binary flash EEPROM file"
    echo "  -o,--output <file>"
    echo "    Output log file"
    echo ""
    echo "Commands"
    echo "  read"
    echo "    Read the flash EEPROM"
    echo "  write"
    echo "    Write the flash EEPROM"
}

function ch341eeprom_read () # <file> <output>
{
    local file="$1";
    local output="$2";
    confirm_current_mode
    if [ "x${output}" != "x" ]; then
	ch341eeprom -v -s 24c02 -r "${file}" &> "${output}"
    else
	ch341eeprom -v -s 24c02 -r "${file}"
    fi
}

function ch341eeprom_write () # <file> <output>
{
    local file="$1";
    local output="$2";
    confirm_current_mode
    if [ "x${output}" != "x" ]; then
	ch341eeprom -v -s 24c02 -w "${file}" &> "${output}"
    else
	ch341eeprom -v -s 24c02 -w "${file}"
    fi
}

function confirm_current_mode ()
{
    read -p "WARNING: Press [Enter] to confirm UT210E is in curret mode."
}

positional=()
while [ $# -gt 0 ]; do
    case "$1" in
	-h|--help)
	    print_usage
	    exit 0
	    ;;
	-f|--file)
	    f="$2";
	    shift 2
	    ;;
	-o|--output)
	    output="$2";
	    shift 2
	    ;;
	*)
	    positional+=("$1")
	    shift
	    ;;
    esac
done
set -- "${positional[@]}" # restore positional parameters

if [ $# -lt 1 ]; then
    echo "ERROR: Must specify command to run."
    print_usage
    exit 1
fi
command="$1"; shift

case "${command}" in
    read)
	ch341eeprom_read "${f}" "${output}"
	;;
    write)
	ch341eeprom_write "${f}" "${output}"
	;;
    *)
	echo "ERROR: Invalid command specified"
	print_usage
	exit 1
esac
