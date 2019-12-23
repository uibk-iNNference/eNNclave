from tensorflow.keras.models import load_model

from utils import get_all_layers
from enclave_layer import EnclaveLayer
from enclave_model import Enclave

import numpy as np
import pandas as pd

import sys
import json

def _texify_number(num):
    "uses a-j instead of 0-9 to work with tex"
    ret = ''
    num_digits = int(np.ceil(np.log10(num)))

    # TODO: ugly hacks for edge cases that I don't want to deal with right now
    if num_digits == 0:
        return 'a'
    if num == 10:
        return 'ba'
    
    for i in range(num_digits):
        int_val = ord('a') + (num % 10)
        ret += chr(int_val)
        num //= 10
    return ret[::-1]

def _calc_log_coord(lin_coord):
    scale_bottom = -2.5 #value of -2.5 shall at 0
    scale_top = 4.7 #value of 4.7 shall be at y_max

    return (np.log(lin_coord)-scale_bottom)/(scale_top-scale_bottom)

def net_summary(model):
    start_x = 0
    width = 1.8
    height = 0.4
    node_distance = 0.5
    space_between = node_distance - height

    ret = ''
    ret += '\\newcommand{\\startx}{%f}\n' % (start_x)
    ret += '\\newcommand{\\nodedistance}{%f}\n' % (node_distance)
    ret += '\\newcommand{\\spacebetween}{%f}\n' % (space_between)
    ret += '\\newcommand{\\layerheight}{%f}\n' % (height)
    
    x_ticks = '\\newcommand{\\xticks}{'
    
    layers = get_all_layers(model)
    ret += '\n\\newcommand{\\netsummary}[1]{\n'
    for i,l in enumerate(layers):
        cleaned_name = l.name.replace('_','\_')
        current_x = start_x + node_distance*i
        ret += "\\node[draw=black,minimum width=%fcm,minimum height=%fcm,rotate=-90, anchor=south west] at (%f,#1) {\\tiny %s};" \
            % (width, height, current_x, cleaned_name)
        ret += "\n"

        if i > 0:
            if i > 1:
                x_ticks += ','
            x_ticks += '%f' % (current_x - space_between/2)

    x_ticks += '}\n'
    ret += '}\n'

    ret += x_ticks
    ret += '\\newcommand{\\netwidth}{%f}\n' % (current_x + height)

    return ret

def time_rectangles(times):
    y_max = 5
    y_ticks = np.concatenate([np.arange(0.1, 1, 0.1), np.arange(1, 10, 1), np.arange(10, 110, 10)])
    rectangle_width = 0.2

    ret = ''
    ret += '\\newcommand{\\ymax}{%f}\n' % y_max
    ret += '\\newcommand{\\yticks}{'
    for i,y in enumerate(y_ticks):
        coordinate = _calc_log_coord(y)
        
        if i > 0:
            ret += ','
        ret += '%f' % (coordinate*y_max)
    ret += '}\n'

    for i, row in times.iterrows():
        gpu_time = row['gpu_time']
        enclave_time = row['combined_enclave_time']
        native_time = row['native_time']
        split = int(row['layers_in_enclave'])
        
        left_coordinate = '\\netwidth-\\layerheight-%d*\\nodedistance-\\spacebetween/2-%f' % (split-1, rectangle_width/2)
        right_coordinate = left_coordinate + ("+%f" % rectangle_width)
        
        gpu_north = _calc_log_coord(gpu_time)*y_max
        native_north = _calc_log_coord(gpu_time+native_time)*y_max
        enclave_north = _calc_log_coord(gpu_time+enclave_time)*y_max
        
        node = '\\draw (%s, 0) rectangle (%s, %f);\n' % (left_coordinate, right_coordinate, gpu_north)
        node += '\\draw[pattern=north east lines] (%s, %f) rectangle (%s, %f);\n' % (left_coordinate, gpu_north, right_coordinate, native_north)
        node += '\\draw[pattern=north west lines] (%s, %f) rectangle (%s, %f);\n' % (left_coordinate, native_north, right_coordinate, enclave_north)

        ret += '\\newcommand{\\split%s}{%s}\n' % (_texify_number(split), node)
        
    return ret

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: {} model_file".format(sys.argv[0]))
        sys.exit(1)
    
    model_file = sys.argv[1]
    model = load_model(model_file, custom_objects={
                       "Enclave": Enclave, "EnclaveLayer": EnclaveLayer})

    tikz = net_summary(model)
    print(tikz)

    time_file = 'timing_logs/mit67_times.csv'
    times = pd.read_csv(time_file)
    print(time_rectangles(times))
