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

# The data needs to be pre-processed.
# This involves almost always mean centering the data.
# And very often normalizing.
# If other stuff has to be done, that can be added here.

import numpy as np

# these_processes can be "no input" (actually it is '') if the user 
# presses just enter. In this case everything will be done.
# If it is '1' just mean centering will take place.
# If it is '0' nothing will be done.
def preprocess_data(these_processes, data, rawdata):
	if these_processes == '' or these_processes == '1':
		# data.mean(axis=0) gives the mean along one variable.
		# np.nanmean(data, axis=0) does the same, just ignoring NaN's.
		# A line vector is returned. So data.mean(axis=0).shape is (5,) => the second 
		# indice is missing.
		# Thus I have to transfer the line-vector into an array to be able to plot it.
		mean_data = np.array([np.nanmean(data, axis=0)])

		# Center the raw data.
		# 
		# This confuses me.
		# data is an e.g. 50 x 5 array, while mean_data is a 1 x 5 array.
		# it seems to be as if numpy interprets it in a way that from each
		# row in data mean_data is substracted.
		data -= mean_data
		rawdata -= mean_data

	if these_processes == '':
		# Scale the centered data.
		# Same issue as above
		# ddof: "Delta Degrees of Freedom". By default, this is 0. Set it to 1 
		# to get the LibreOffice result.
		# More context here: http://stackoverflow.com/questions/27600207/ ...
		# ... why-does-numpy-std-give-a-different-result-to-matlab-std
		standard_deviation = np.array([np.nanstd(data, axis = 0, ddof = 1)])

		data /= standard_deviation
		rawdata /= standard_deviation

	return data, rawdata



# If the influence of one variable is known, one can put the influence of
# this variable into one component by multiplying this column with 1000.
# Then the other components "don't" contain this variable any longer.
def boost_variables(enhance_these, data, rawdata):
	if enhance_these != '':
		enhance_these_variables = enhance_these.split(',')

# ATTENTION: HERE IS NO CHECK IF I ACTUALLY HAVE CORRECT NUMBERS!
		for variable in enhance_these_variables:
			number = int(variable) - 1
			data[:,number] *= 1000
			rawdata[:,number] *= 1000

	return data, rawdata









