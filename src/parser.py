#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 22 08:51:01 2026

@author: asullivan
"""

# functions which are used to parse an input file

def parse_value(value_str):
    """Parse a value that could be: number, bool, string, or array"""
    value_str = value_str.strip()
    
    # Remove brackets if present
    if value_str.startswith('[') and value_str.endswith(']'):
        value_str = value_str[1:-1]
    
    # Check if it contains commas or multiple spaces (array)
    if ',' in value_str or len(value_str.split()) > 1:
        # Split by comma first, then by whitespace
        if ',' in value_str:
            items = [item.strip() for item in value_str.split(',')]
        else:
            items = value_str.split()
        
        # Try to convert to numbers
        array = []
        for item in items:
            if not item:  # skip empty strings
                continue
            try:
                array.append(int(item))
            except ValueError:
                try:
                    array.append(float(item))
                except ValueError:
                    array.append(item)  # keep as string
        return array
    
    # Single value - bool, int, float, or string
    if value_str.lower() in ('true', 'false'):
        return value_str.lower() == 'true'
    
    try:
        return int(value_str)
    except ValueError:
        try:
            return float(value_str)
        except ValueError:
            return value_str  # string

def parse_params(filename):
    params = {}
    current_section = "general"
    
    with open(filename, 'r') as f:
        for line in f:
            line = line.strip()
            
            if not line:
                continue
            
            # Section header
            if line.startswith('#'):
                current_section = line[1:].strip()
                params[current_section] = {}
            
            # Key = value
            elif '=' in line:
                key, value = line.split('=', 1)
                key = key.strip()
                value = value.strip()
                
                params[current_section][key] = parse_value(value)
    
    return params