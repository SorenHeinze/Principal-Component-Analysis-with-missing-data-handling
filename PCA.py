#    "PCA" (v0.7)
#    Copyright 2016 Soren Heinze
#    soerenheinze@gmx.de
#    5B1C 1897 560A EF50 F1EB 2579 2297 FAE4 D9B5 2A35
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.


import numpy as np
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d import proj3d
from math import sqrt
from scipy import linalg as SLA
from copy import deepcopy
import read_data as rd
import colourcode as cc
import plotting as pl
import data_preprocessing as dp
import nipals_algorithm as na
import Image


# The user has to provide some information
def get_information():
	# First the user needs to provide some information.
	folder = raw_input('\nFolder with the file (e.g. "/home/<user>/data/"): ')
	this_file = raw_input('Filename (incl. file-extension, if applicable; e.f. "foo.txt"): ')
	infile = folder + this_file

	text = "Number of components to analyze (Needs to be an integer > 1): "
	number_of_components = int(raw_input(text))

	graphtitle = raw_input("Title for all graphs: ")

	return infile, number_of_components, graphtitle



# Looking at and pre-processing the data.
def look_at_and_pre_process_data(data, rawdata, variables):
	# Now plot the input data.
	show_data = raw_input("Show the raw-data? (1 = YES): ")
	if show_data == '1':
		pl.plot_data(data, variables)

	# Preprocess the data (mean-centering, normalization).
	text_1 = "Pre-process the data (ENTER = normalization AND mean centering, "
	text_2 = "1 = JUST mean centering, 0 = None): "
	these_processes = raw_input(text_1 + text_2)
	data, rawdata = dp.preprocess_data(these_processes, data, rawdata)

	# "Enhance" certain variables to put all their influence into one component.
	text = "Enhance variables? As integers: Variable_1, Variable_2, ... ; ENTER = none): "
	enhance_these = raw_input(text)
	data, rawdata = dp.boost_variables(enhance_these, data, rawdata)



# Get the colour-coding (if applicable).
def get_colours(observations):
	# This is just for colouring the data if the user provides the specific 
	# information in the colourcode.py-file.
	text = "Have you provided a colour-code in the colourcode.py file (1 = YES): "
	if raw_input(text) == '1':
		return cc.colourcode(observations)
	else:
		return None




# This wil be called when the program is called.
# It is just to keep it a bit more tidy.
def main():
	# Get the basic information.
	infile, number_of_components, graphtitle = get_information()

	# Here the data is finally read from the file.
	data, rawdata, variables, observations = rd.read_data(infile)

	# Look at and pre-process the data.
	look_at_and_pre_process_data(data, rawdata, variables)

	# Get the colour-coding (if applicable).
	colours = get_colours(observations)

	# Here the actual NIPALS algorithm is executed.
	print "\nBe patient. The NIPALS-algorithm may need some time ...\n"
	Z_merged, P_merged, r_merged, R_2, R_k_2, SPE, T_2 = na.nipals_pca(data, \
														rawdata, number_of_components)

	# Plotting basic information.
	pl.plotting_the_basics(number_of_components, R_2, graphtitle, observations, \
					variables, Z_merged, P_merged, colours = None)

	# Plotting the "versus-graphs".
	pl.plotting_more_complicated_graphs(number_of_components, R_2, T_2, graphtitle, \
									SPE, observations, variables, Z_merged, \
									P_merged, r_merged, colours)

	print "\nThank you for using this program\n"





if __name__ == '__main__':
	main()









