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


# This is the NIPALS algorithm, the core of the whole program.
# All the calculations were implemented "by hand", instead of using a module
# that can do all the matrix multiplications. I did that because I needed to be
# sure that missing values are treated the correct way, since missing values
# are quite common in social data.
# 
# I will not explain the math behind the calculations performed here.
# please look up NIPALS and all associated stuff yourself.

import numpy as np
from scipy import linalg as SLA
from math import sqrt
from copy import deepcopy
import plotting as pl

# Returned are the loadings, scores, the Hotelling's T^2, the square prediction 
# error per variable (SPE), the variance per column (R_k^2) and how much
# of the variance is explained by each component (R_2)
def nipals_pca(data, rawdata, number_of_components):
	# Later I want the Loading- and Score-vectors all in an array.
	# Due to how numpy works when just line/column-vectors are involved
	# I have to work a bit to get this array.
	# In short: I will store each score/loading in a list and later add
	# the elements of this list to the array I create at the end.
	# r are the correlation loadings.
	P_s = []
	Z_s = []
	r_s = []
	Z_Eigenvalues = []

	# This is for the variance after each Z is found.
	# This shows how much of the data the cumulative Z's explain.
	R_2 = [0]

	# This is for the variance of each column after each Z is found
	R_k_2 = []

	# This is for the square prediction error.
	SPE = []

	# This is for the Hotelling's T_2 value.
	T_2 = []

	variance_rawdata, column_variance_rawdata = raw_data_variances(rawdata)

	for i in range(number_of_components):
		first_Z, length_Z = get_first_score(data)

		Z, P, r, length_Z = nipals_iteration(data, first_Z, length_Z)

		P_s.append(P)
		Z_s.append(Z)
		r_s.append(r)
		Z_Eigenvalues.append(length_Z)
		print "Eigenvalue of %s. component: %s" % ((i + 1), Z_Eigenvalues[i])
		print "=================="

		# Now get the residual E by substracting from the original data the 
		# data constructed from the Score and load vector that were calculated 
		# above.
		# This will be the new data.
		data = data - np.dot(Z.T, P)

		# Get R_2 for this component.
		R_2.append(calculate_R_2(data, variance_rawdata))

		# Get R_k_2 for this component.
		R_k_2.append(calculate_R_k_2(data, column_variance_rawdata))

		# Get the SPE for this component.
		SPE.append(calculate_SPE(data))

		# Get the T_2 for this component.
		T_2.append(calculate_T_2(Z, T_2))

	# When all components are found, merge all the Load- and Score-vectors 
	# into the respective matrix.
	Z_merged, P_merged, r_merged = create_matrices(Z_s, P_s, r_s, \
														number_of_components)

	# The end result of the whole shebang.
	return Z_merged, P_merged, r_merged, R_2, R_k_2, SPE, T_2



# To calculate the residuals/errors I need to know the variance of the raw data.
# This is mainly to keep nipals_pca() more tidy.
def raw_data_variances(rawdata):
	variance_rawdata = np.nansum(rawdata*rawdata)

	column_variance_rawdata = []
	for i in range(rawdata.shape[1]):
		column_variance_rawdata.append(np.nansum(rawdata[:,i]*rawdata[:,i]))

	return variance_rawdata, column_variance_rawdata



# For each iteration I need a first score vector to start with.
# This could be (almost) everything, but I've heard that the method used here 
# get's closer to the final vector and, well, why not ;) .
def get_first_score(data):
	# Compute the summed squares.
	# This is the matrix in which each element is squared
	squared = data*data
	# Now sum up all elements in each column.
	summed = np.nansum(squared, axis=0)

	# Since this is a line-vector, argmax returns the index 
	# of the maximum value. Which is good, because this will 
	# be the column I need first.
	index = np.argmax(summed)

	# The first score for the very first iteration.
	Z = data[:,index]
	# Later I have to divide by np.dot(Z.T, Z). This however does not 
	# work with NaN's.
	# Since Z is a vector I can also use the sum of the squared elements.
	# This is how I can make it work with NaN's
	length_Z = np.nansum(Z**2)

	return Z, length_Z



# This is the actual NIPALS iteration.
def nipals_iteration(data, Z, length_Z):
	# The difference in scores between iterations.
	# if this is sufficiently small, the next iteration will start.
	difference = 1
	iteration = 0

	# This is an arbitrary value. It can be larger to speed up the process
	# but this will lead to the loss of accuracy.
	while difference > 0.000000001:
		iteration += 1

		# Calculate the elements of the first loading vector approximation.
		p_s_per_column = calculate_p_s_per_column(data, Z, length_Z)
		# Now make the correct load line vector out of the many p's 
		# calculated above.
		P = np.array(p_s_per_column)
		# ATTENTION: P gets normalized in calculate_p_s_per_column

		# Now the same for the next (new) score vector.
		z_s_per_row = calculate_z_s_per_row(data, P)
		new_Z = np.array(z_s_per_row)
		length_new_Z = np.nansum(new_Z**2)

		difference = abs(length_Z - length_new_Z)

		# Why is this here?
		# Well, I've seen in the missing value case, that some few 
		# datapoints in the score-vector have extreme values compared to most
		# of the data. This leads to a logarithmically slow converging 
		# algorithm. Leaving out these few points solved the issue.
		# Since I don't want to plot all of these manually I take care
		# of it by automatically showing the Scores when NIPALS 
		# needs more then 299 iterations.
		if iteration == 300:
			print "\n 300 iterations have passed, please check the "
			print "data for extreme outliers. And take these out if "
			print "after 300 more iteration NIPALs still doesn't converge."
			pl.plot_scores(1, [1,1], 'foo', range(1, (len(Z) + 1)), [Z])


		# The new_Z is the Z to start with in the next iteration.
		Z = new_Z
		length_Z = length_new_Z

		# This is an arbitrary number and will halt the whole process if too 
		# many iterations have to be undertaken.
		if iteration > 600:
			break

	# Once the Z's and P's are know, calculate the correlation loading r.
	r_s_per_column = calculate_r_s_per_column(data, Z, P)
	r = np.array(r_s_per_column)

	# Once the correct load- and score vector for a component is found,
	# build a correct numpy array which can then be appended to the
	# P_s / Z_s to be able to construct the correct Load and Score Matrix 
	# later.
	# 
	# My P and first_Z-vectors are not recognised as line- or column
	# matrix. By doing the next two things I take care of that.
	P = np.array([P])
	Z = np.array([Z])
	r = np.array([r])

	print "So many iterations undertaken:", iteration

	return Z, P, r, length_Z



# Just to keep nipals_iteration() a bit more tidy.
def calculate_r_s_per_column(data, Z, P):
	r_s_per_column = []
	for o in range(P.shape[0]):
		upper_sum = 0
		first_lower_sum = 0
		second_lower_sum = 0

		no_number_here = []
		modified_Z = deepcopy(Z)
		# data could contain nan's. I need to know where these are
		# because at these positions I also need to omit the
		# Z-component.
		no_number_here = np.argwhere(np.isnan(data[:,o]))
		modified_Z = remove_elements(modified_Z, no_number_here)

		# This is all taken from here: 
		# https://en.wikipedia.org/wiki/ ...
		# ... Pearson_product-moment_correlation_coefficient#For_a_sample
		# taking into account that the sum is not to be executed over missing 
		# values.
		x_dash = np.nansum(data[:,o]) / (len(data[:,o]) - len(no_number_here))
		# np.nansum() is mot necessary here, but I keep it for
		# consistency reasons.
		z_dash = np.nansum(modified_Z) / len(modified_Z)

		for i in range(len(modified_Z)):
			if np.isnan(data[:,o][i]):
				pass
			else:
				first_factor = data[:,o][i] - x_dash
				second_factor = modified_Z[i] - z_dash

				upper_sum += first_factor * second_factor
				first_lower_sum += first_factor**2
				second_lower_sum += second_factor**2

		divisor = sqrt(first_lower_sum) * sqrt(second_lower_sum)

		r = upper_sum / divisor

		r_s_per_column.append(r)

	return r_s_per_column



# Just to keep calculate_r_s_per_column() a bit more tidy.
# no_number_here is an array.
def remove_elements(modified_Z, no_number_here):
	this_array = deepcopy(modified_Z)
	i = 0
	for element in no_number_here:
		# Due to the nature of what np.argwhere returns, I can
		# not just use the element itself but need to address to zero
		# to get the index.
		index = element[0] - i
		# The index is for the old, UNmodified Z-vector. Since I remove
		# elements from this vector, the index of all vector-elements 
		# behind the removed position change. Thus I have to comppensate
		# for this.
		i += 1
		# Now delete the elements from modified_Z that correspond
		# to nan's in data[:,o]
		# YES, this will make a new array all the time for each missing
		# value. WHOA ... this may take a long time for large arrays. 
		# On the other hand, it's assumed that missing values actually 
		# are NOT plenty. 
		this_array = np.delete(this_array, index)

	return this_array



# Just to keep nipals_iteration() a bit more tidy.
def calculate_p_s_per_column(data, Z, length_Z):
	p_s_per_column = []

	for m in range(data.shape[1]):
		upper_sum = 0
		lower_sum = 0

		for i in range(len(Z)):
			# Since i just "grab" a column from data as the first
			# Z it is entirely possible that this Z contains NaN's.
			# Thus I also have to check for this.
			# This applies just for the very first Z and is not the case 
			# for the P's and subsequent Z's since these are calculated
			# and should always have a value.
			# 
			# ATTENTION: This is not just for taking care of NaN's 
			# in the data. For this np.nansum() could be used. But
			# lower_sum shall NOT contain the corresponding values if
			# the value is missing in the data.
			if np.isnan(data[:,m][i]) or np.isnan(Z[i]):
				pass
			else:
				upper_sum += Z[i]*data[:,m][i]
				lower_sum += Z[i]*Z[i]

		p = upper_sum / lower_sum

		p_s_per_column.append(p)

	return p_s_per_column



# Just to keep nipals_iteration() a bit more tidy.
def calculate_z_s_per_row(data, P):
	z_s_per_row = []

	for n in range(data.shape[0]):
		upper_sum = 0
		lower_sum = 0

		for i in range(len(P)):
			if np.isnan(data[n,:][i]):
				pass
			else:
				upper_sum += P[i]*data[n,:][i]
				lower_sum += P[i]*P[i]

		z = upper_sum / lower_sum

		z_s_per_row.append(z)

	return z_s_per_row



# Now the R_2 variance for the original data minus the data constructed
# from the Score and load vector that were calculated above. 
# Since the Subtraction was taken care of before, I just need to use data.
def calculate_R_2(data, variance_rawdata):
	variance_new_data = np.nansum(data*data)
	
	return 1 - variance_new_data/variance_rawdata



# Dito for the variance per column.
def calculate_R_k_2(data, column_variance_rawdata):
	new_R_k_2 = []
	for i in range(data.shape[1]):
		column_variance_new_data = np.nansum(data[:,i]*data[:,i])
		new_R_k_2.append(1 - column_variance_new_data/column_variance_rawdata[i])

	return new_R_k_2



# Now the square prediction error per variable.
def calculate_SPE(data):
	new_SPE = []
	for i in range(data.shape[0]):
		foo = sqrt(np.dot(data[i].reshape(data[0].shape[0], 1).T, \
									data[i].reshape(data[0].shape[0], 1)))
		if np.isnan(foo):
			foo = sqrt(np.nansum(data[i]**2))

		new_SPE.append(foo)

	return new_SPE



# And finally Hotelling's T^2.
def calculate_T_2(Z, T_2):
	new_T_2 = []
	if len(T_2) == 0:
		s_a = np.std(Z)
		for i in range(Z.shape[1]):
			new_T_2.append((Z[0][i]/s_a)**2)
	else:
		add_to_this = len(T_2) - 1
		s_a = np.std(Z)
		for i in range(Z.shape[1]):
			new_T_2.append(T_2[add_to_this][i] + (Z[0][i]/s_a)**2)

	return new_T_2



# When all components are found, merge all the Load- and Score-vectors 
# into the respective matrix.
# This function is mainly to keep nipals_pca() more tidy.
def create_matrices(Z_s, P_s, r_s, number_of_components):
	# I need a correct array to begin with, thus these two lines before the 
	# loop.
	P_merged = np.concatenate((P_s[0], P_s[1]), axis=0)
	Z_merged = np.concatenate((Z_s[0], Z_s[1]), axis=0)
	r_merged = np.concatenate((r_s[0], r_s[1]), axis=0)

	for i in range(2, number_of_components):
		P_merged = np.concatenate((P_merged, P_s[i]), axis=0)
		Z_merged = np.concatenate((Z_merged, Z_s[i]), axis=0)
		r_merged = np.concatenate((r_merged, r_s[i]), axis=0)

	return Z_merged, P_merged, r_merged









