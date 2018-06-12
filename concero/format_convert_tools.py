#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#      ConCERO - a program to automate data format conversion and the execution of economic modelling software.
#      Copyright (C) 2018  CSIRO Energy Business Unit
#
#     This program is free software: you can redistribute it and/or modify
#     it under the terms of the GNU General Public License as published by
#     the Free Software Foundation, either version 3 of the License, or
#     (at your option) any later version.
#
#     This program is distributed in the hope that it will be useful,
#     but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#     GNU General Public License for more details.
#
#     You should have received a copy of the GNU General Public License
#     along with this program.  If not, see <https://www.gnu.org/licenses/>.

"""
Created on Thu Dec 21 10:39:13 2017

@author: Lyle Collins
@email: Lyle.Collins@csiro.au
"""
import yaml

def read_yaml(filename):
    with open(filename, 'r') as inFile:
        conf = yaml.load(inFile)
    return conf

