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


# This module is mainly for the function that reads the data for PCA 
# analysis and returns numpy-array's.
# It is quite strict regarding how the data has to look like.
# 
# Example (<TAB> is used as a separator, M = Male, F = Female):
# 
# Sample	Age	M	F	Color	...
# X23foo	23	0	1	1		...
# Y23bar	24	1	0	4		...
# Z23oof	1	0	1	7		...
# 
# ATTENTION: In physics the data is mostly displayed the other way around, 
# That means the variables are in the leftmost column the other columns 
# represent e.g. one experiment/sample.
# The program asks for this and will transpose the matrix.
# See also the comment below.

import numpy as np
from copy import deepcopy

# This function is called in read_data() and written just to keep the latter
# more orderly. f is the infile.
def get_the_data(f):
	variables = []
	observations = []
	just_the_data = []

	linecount = 1
	for line in f:
		# The first line contains the descriptors of the variables 
		# (e.g. the wavelength's or attributes investigated).
		# In the else-clause it will be "converted" into the variables.
		if linecount != 1:
			numbers = []
			all_in_line = line.strip().split(',')
			first_entry = all_in_line.pop(0)

			# The first entry in each line contains e.g. the sample- or 
			# measurement number; vulgo: the observations
			try:
				# Try to make numbers if possible.
				observations.append(float(first_entry))
			except ValueError:
				# Otherwise use the given string.
				observations.append(first_entry)

			for number in all_in_line:
				# Everything else should be just numbers
				try:
					numbers.append(float(number))
				# If not, use an appropriate NaN.
				except ValueError:
					numbers.append(np.nan)

			just_the_data.append(numbers)

		else:
			try:
				for number in line.strip().split(','):
					variables.append(float(number))
			except ValueError:
				variables = line.strip().split(',')

		linecount += 1

	return variables, observations, just_the_data


# This is the function to be called. 
def read_data(infile):
	with open(infile, 'r') as f:
		variables, observations, just_the_data = get_the_data(f)

	# The first entry in variables does not belong to the data but is
	# a descriptor like e.g. "Sample" or "Measurement".
	# Hence, it mus tbe removed
	variables.pop(0)

	data = np.array(just_the_data)

	# Usually data is available in the form of variables (e.g. wavelength's) in 
	# horizontal direction and e.g. samples or observations in vertical
	# direction.
	# This program relies on that.
	# However, in physics it's the other way around.
	# Thus I have to switch the labels and transpose the data
	physical_data = raw_input("Is it 'Physics data' (see manual) (1 = YES): ")

	if physical_data == '1':
		foo = deepcopy(variables)
		bar = deepcopy(observations)
		variables = bar
		observations = foo
		data = data.T

	# data will later be changed during the process, but I need
	# the original data for some calculations and one never knows. Hence
	# I copy it here.
	rawdata = deepcopy(data)

	return data, rawdata, variables, observations









