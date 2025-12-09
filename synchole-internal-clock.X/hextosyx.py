#!/usr/bin/env python3
"""
HexToSyx - Convert Intel HEX files to SysEx format for MIDI bootloader
Python port for Mac/Linux compatibility
Based on original C++ version by hotchk155/Jason
"""

import sys
import struct

# SysEx protocol constants
SYSEX_START = 0xF0
SYSEX_ID0 = 0x00
SYSEX_ID1 = 0x7F
SYSEX_END = 0xF7

MEMORY_SIZE = 8 * 2 * 1024

# Product configurations
PRODUCTS = {
    'a': {'name': 'CV.OCD', 'id': 0x12, 'block_size': 32},
    'b': {'name': 'Synchole', 'id': 0x14, 'block_size': 16},
    'c': {'name': 'Orange Squeeze', 'id': 0x13, 'block_size': 32},
    'd': {'name': 'MIDI Switcher (Original)', 'id': 0x16, 'block_size': 32},
    'e': {'name': 'MIDI Hub', 'id': 0x17, 'block_size': 32},
    'f': {'name': 'Mini MIDI Switcher (SMT)', 'id': 0x20, 'block_size': 32},
    'g': {'name': 'MIDIWALL', 'id': 0x22, 'block_size': 16},
    'h': {'name': 'Relay Switcher', 'id': 0x23, 'block_size': 32},
    'i': {'name': 'MIDI NUBBIN', 'id': 0x25, 'block_size': 32},
}


def from_hex(c):
    """Convert hex character to integer"""
    c = c.upper()
    if '0' <= c <= '9':
        return ord(c) - ord('0')
    elif 'A' <= c <= 'F':
        return ord(c) - ord('A') + 10
    return 0


def read_hex(infile):
    """Read Intel HEX file and return memory array and max address"""
    memory = bytearray([0xFF] * MEMORY_SIZE)
    max_addr = 0
    offset = 0
    line_num = 0
    
    for line in infile:
        line_num += 1
        line = line.strip()
        
        if not line or not line.startswith(':'):
            continue
        
        # Parse line length
        if len(line) < 11:
            print(f"Error: Line {line_num} too short")
            return None, 0
        
        # Get data length
        data_len = 16 * from_hex(line[1]) + from_hex(line[2])
        
        # Check line length matches data length
        if 2 * data_len + 11 != len(line):
            print(f"Error: Line {line_num} length mismatch")
            return None, 0
        
        # Get record type
        rec_type = 16 * from_hex(line[7]) + from_hex(line[8])
        
        if rec_type == 1:  # END OF FILE
            break
        elif rec_type == 4:  # EXTENDED LINEAR ADDRESS
            if len(line) != 15:
                print(f"Error: Invalid extended address at line {line_num}")
                return None, 0
            offset = (from_hex(line[9]) << 12 |
                     from_hex(line[10]) << 8 |
                     from_hex(line[11]) << 4 |
                     from_hex(line[12])) << 16
            print(f"Linear address offset 0x{offset:x} from line {line_num}")
        elif rec_type == 0:  # DATA
            # Get base address
            addr = (from_hex(line[3]) << 12 |
                   from_hex(line[4]) << 8 |
                   from_hex(line[5]) << 4 |
                   from_hex(line[6]))
            addr += offset
            
            if addr + 2 * data_len >= MEMORY_SIZE:
                print(f"Warning: Address 0x{addr:x} out of range at line {line_num}")
                continue
            
            # Copy data into memory buffer
            data_pos = 9
            for i in range(data_len):
                data = from_hex(line[data_pos]) << 4 | from_hex(line[data_pos + 1])
                memory[addr] = data
                addr += 1
                data_pos += 2
                if max_addr < addr:
                    max_addr = addr
        else:
            print(f"Warning: Unsupported record type {rec_type} at line {line_num}")
    
    return memory, max_addr


def reformat_reset_vec(memory):
    """Handle MPLABX double reset vector"""
    if (memory[0] == 0x80 and memory[1] == 0x31 and
        memory[2] == 0x02 and memory[3] == 0x28):
        memory[0] = memory[4]
        memory[1] = memory[5]
        memory[2] = memory[6]
        memory[3] = memory[7]
        print("*** REFORMATTED 4 WORD RESET VECTOR ***")


def write_sysex(outfile, memory, max_addr, product_id, block_size):
    """Write memory to SysEx file"""
    msg_sequence = 1
    addr = 0
    
    while addr < max_addr:
        # Write SysEx message
        outfile.write(bytes([SYSEX_START, SYSEX_ID0, SYSEX_ID1, product_id, msg_sequence]))
        
        for i in range(block_size):
            # Read word (little endian) and mask to 14 bits
            word = (memory[addr + 1] << 8 | memory[addr]) & 0x3FFF
            # Split into two 7-bit bytes
            outfile.write(bytes([word >> 7, word & 0x7F]))
            addr += 2
        
        outfile.write(bytes([SYSEX_END]))
        
        # Increment sequence number (1-127)
        msg_sequence += 1
        if msg_sequence > 0x7F:
            msg_sequence = 1
    
    # Write end marker (sequence 0)
    outfile.write(bytes([SYSEX_START, SYSEX_ID0, SYSEX_ID1, product_id, 0x00]))
    for i in range(block_size):
        outfile.write(bytes([0x00, 0x00]))
    outfile.write(bytes([SYSEX_END]))


def main():
    if len(sys.argv) != 4:
        print("HEX2SYX - Convert Intel HEX to SysEx for MIDI bootloader")
        print(f"Usage: {sys.argv[0]} <product_id> <input.hex> <output.syx>")
        print("\nAvailable products:")
        for key, prod in sorted(PRODUCTS.items()):
            print(f"  [{key}] {prod['name']}")
        sys.exit(1)
    
    product_key = sys.argv[1].lower()
    input_file = sys.argv[2]
    output_file = sys.argv[3]
    
    if product_key not in PRODUCTS:
        print(f"Error: Invalid product ID '{product_key}'")
        sys.exit(2)
    
    product = PRODUCTS[product_key]
    print(f"Converting for {product['name']}")
    
    try:
        with open(input_file, 'r') as infile:
            memory, max_addr = read_hex(infile)
            if memory is None:
                print("Error reading HEX file")
                sys.exit(3)
    except FileNotFoundError:
        print(f"Error: Input file '{input_file}' not found")
        sys.exit(3)
    except Exception as e:
        print(f"Error reading input file: {e}")
        sys.exit(3)
    
    reformat_reset_vec(memory)
    
    try:
        with open(output_file, 'wb') as outfile:
            write_sysex(outfile, memory, max_addr, product['id'], product['block_size'])
    except Exception as e:
        print(f"Error writing output file: {e}")
        sys.exit(4)
    
    print(f"Successfully converted {input_file} to {output_file}")
    print("Done!")


if __name__ == '__main__':
    main()
