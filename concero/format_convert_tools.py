#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec 21 10:39:13 2017

@author: Lyle Collins
@email: Lyle.Collins@csiro.au
"""
import os
import yaml

import concero.conf

def read_yaml(filename):
    # filename = concero.conf.find_file(filename)
    # filename = os.path.normpath(filename)
    with open(filename, 'r') as inFile:
        conf = yaml.load(inFile)
    return conf

