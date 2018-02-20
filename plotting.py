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

# Some functions that are all very similar but are supposed to plot
# different aspects of the PCA.

from matplotlib import pyplot as plt
from matplotlib import text as txt
from matplotlib.patches import Ellipse
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d import proj3d
import numpy as np
from math import sqrt
import pylab
import my_globals as mg

# Plotting the input data as it was read.
def plot_data(data, variables):
	# Plot the data.
	# Many lines shall be plotted in one picture.
	# 
	# I need a figure instance
	fig = plt.figure()

	# Everytime I call ax add a subplot to the figure 
	# => make 1 row and 1 column with subplots => make one picture the 
	# last "1" is the ordering
	ax = fig.add_subplot(111)

	# I want the labels/variables on the x-axis and not just numbers
	# This is be done a bit complicated in matplotlib by defining the x-axis
	# ticks (see below). This however, corralates the tick at position x 
	# with a given label.
	# The number of ticks on a respective axis does not change, so i calculate it 
	# here and use the name throughout the program.

	plt.xticks(range(len(variables)), variables)
	for i in range(len(data)):
		ax.plot(range(len(variables)), data[i])

	plt.show()



# Plot explained variance.
def plot_explained_variance(R_2, graphtitle):
	# Without plt.close() in each loop I'm having some problems when 
	# plotting the figures. Either the labels don't appear or that an 
	# additional plot window appears. This happens even if no plot was shown before. 
	# plt.close() takes care of this.
	plt.close()

	plt.xlabel('Components')
	plt.ylabel('Explained Variance R^2')
	plt.title(graphtitle)
	plt.plot(range(len(R_2)), R_2, '.', markersize = 23, color='blue')

	plt.show()



# Plot Scores
# colours is for the case that the points shall be coloured according to a 
# specified colour scheme.
def plot_scores(plot_this, R_2, graphtitle, observations, Z_merged, \
					colours = False, legend = None, height = None):
	plt.close()

	if colours:
		fig = plt.figure()
		ax = fig.add_subplot(111)

	percentage = int((R_2[plot_this] - R_2[plot_this - 1]) * 100)
	plt.xlabel('Score PC-%s (%s %%)' % (plot_this, percentage))
	plt.ylabel('')
	plt.title(graphtitle)

	plt.xticks(range(len(observations)), observations)

	# If I don't have colours I don't consider it important to add
	# a legend.
	if colours:
		# ATTENTION: plot_this is is the actual principal component,  however, 
		# the indexing in array's (as Z_merged is one) starts at zero
		# ATTENTION: This is not the case for R_2 above, since there 
		# the index corresponds to the number of the principal component
		# and element zero is just zero.
		# 
		# ax.scatter takes by itself care of making a scatterplot.
		# s is the size of the dots, c is the list with the colours
		# for each point (see also comment above).
		ax.scatter(range(len(observations)), Z_merged[plot_this - 1], \
														c = colours, s = 100)
	else:
		plt.plot(range(len(observations)), Z_merged[plot_this - 1], '.', \
													markersize = 23, color='blue')

	# For the data the program was originally created for, the legend was rather
	# complicated and I added it to the graph via an image. I left this in, in
	# case anybody needs it, but it is switched off by default and the 
	# legend-image needs to be provided in "AA_PCA_Metal.py" and added there
	# in all the relevant functions.
	if legend != None:
		fig.figimage(legend, 0, fig.bbox.ymax - height, zorder = 10)

	plt.show()



# Plot Loadings.
def plot_loadings(plot_this, R_2, graphtitle, variables, P_merged):
	plt.close()

	percentage = int((R_2[plot_this] - R_2[plot_this - 1]) * 100)
	plt.xlabel('Loading PC-%s (%s %%)' % (plot_this, percentage))
	plt.ylabel('')
	plt.title(graphtitle)

	plt.xticks(range(len(variables)), variables)
	plt.plot(range(len(variables)), P_merged[plot_this - 1], '.', \
											markersize = 23, color='blue')

	plt.show()



# Plot Scores over Scores.
def plot_scores_vs_scores(plot_this, R_2, graphtitle, observations, Z_merged, \
									colours = False, legend = None, height = None):
	plt.close()

	plot_these = plot_this.split(',')
	plot_a = int(plot_these[0]) - 1
	plot_b = int(plot_these[1]) - 1

	# If in the input a third thing is given, it is interpreted as to 
	# draw the labels onto each point.
	try:
		if plot_these[2] != 'risimif':
			plot_label = True
	except IndexError:
		plot_label = False

	percentage_a = int((R_2[plot_a + 1] - R_2[plot_a]) * 100)
	percentage_b = int((R_2[plot_b + 1] - R_2[plot_b]) * 100)

	fig = plt.figure()
	ax = fig.add_subplot(111)
	plt.xlabel('Score PC-%s (%s %%)' % (plot_a + 1, percentage_a))
	plt.ylabel('Score PC-%s (%s %%)' % (plot_b + 1, percentage_b))
	plt.title(graphtitle)

	# These are just two lines to indicate 0.
	max_in_x = max(Z_merged[plot_b])
	max_in_y = max(Z_merged[plot_a])
	min_in_x = min(Z_merged[plot_b])
	min_in_y = min(Z_merged[plot_a])
	ax.plot((0, 0), (min_in_x, max_in_x), color='red')
	ax.plot((min_in_y, max_in_y), (0, 0), color='red')

	if colours:
		ax.scatter(Z_merged[plot_a], Z_merged[plot_b], c = colours, s = 100)
	else:
		ax.scatter(Z_merged[plot_a], Z_merged[plot_b], c = 'blue', s = 100)

	if plot_label:
		for i, text in enumerate(observations):
			ax.annotate(text, (Z_merged[plot_a][i], Z_merged[plot_b][i]))

	if legend != None:
		fig.figimage(legend, 0, fig.bbox.ymax - height, zorder = 10)

	plt.show()



# Plot Loadings over Loadings.
def plot_loadings_vs_loadings(plot_this, R_2, graphtitle, variables, P_merged, \
			colours = False, legend = None, height = None, correlation_loading = False):
	plt.close()

	plot_these = plot_this.split(',')
	plot_a = int(plot_these[0]) - 1
	plot_b = int(plot_these[1]) - 1

	percentage_a = int((R_2[plot_a + 1] - R_2[plot_a]) * 100)
	percentage_b = int((R_2[plot_b + 1] - R_2[plot_b]) * 100)

	fig = plt.figure()
	ax = fig.add_subplot(111)
	plt.xlabel('Loading PC-%s (%s %%)' % (plot_a + 1, percentage_a))
	plt.ylabel('Loading PC-%s (%s %%)' % (plot_b + 1, percentage_b))
	plt.title(graphtitle)

	if correlation_loading:
		max_in_x = 1
		max_in_y = 1
		min_in_x = -1
		min_in_y = -1
		ellipse_1 = Ellipse(xy = (0, 0), width = 2, height = 2, angle = 360)
		ellipse_1.set_facecolor('none')
		# The ellipse equation is r^2 = width^2 + height^2.
		# ellipse_2 shall be for r^2 = 0.5 ( = 50 %).
		ellipse_2 = Ellipse(xy = (0, 0), width = 2*sqrt(0.5), \
											height = 2*sqrt(0.5), angle = 360)
		ellipse_2.set_facecolor('none')

		ax.add_artist(ellipse_1)
		ax.add_artist(ellipse_2)
	else:
		max_in_x = max(P_merged[plot_b])
		max_in_y = max(P_merged[plot_a])
		min_in_x = min(P_merged[plot_b])
		min_in_y = min(P_merged[plot_a])

	ax.plot((0, 0), (min_in_x, max_in_x), color='red')
	ax.plot((min_in_y, max_in_y), (0, 0), color='red')


	for i, text in enumerate(variables):
		ax.plot(P_merged[plot_a], P_merged[plot_b], '.', markersize=13, color='blue')
		ax.annotate(text, (P_merged[plot_a][i], P_merged[plot_b][i]))

	plt.show()



# Plot Residuals over Hotelling's T_2.
def plot_spe_over_t_2(plot_this, T_2, SPE, graphtitle, observations):
	plt.close()

	plot_a = int(plot_this.split(',')[0]) - 1

	max_x = np.percentile(T_2[plot_a], 95)
	max_y = np.percentile(SPE[plot_a], 95)

	max_in_x = max(SPE[plot_a])
	max_in_y = max(T_2[plot_a])

	fig = plt.figure()
	ax = fig.add_subplot(111)
	plt.xlabel('Hotelling T^2 (PC-%s)' % (plot_a + 1))
	plt.ylabel('SPE (PC-%s)' % (plot_a + 1))
	plt.title(graphtitle)

	# These are just two lines indicating the 95% percentiles.
	ax.plot((max_x, max_x), (0, max_in_x), color='red')
	ax.plot((0, max_in_y), (max_y, max_y), color='red')

	for i, text in enumerate(observations):
		ax.plot(T_2[plot_a], SPE[plot_a], '.', markersize = 23, color = 'blue')
		ax.annotate(text, (T_2[plot_a][i], SPE[plot_a][i]))

	plt.show()



# Sometimes specific user input is needed to plot the correct
# stuff. This input can be wrong and the program shall not crash.
# This function checks if the data can be used to do what it is
# supposed to do.
# To keep the plotting functions in the main progran 
# more tidy I created this function
def false_input(what_to_check, number_of_components, vs = False, three_d = False):
	so_many = len(what_to_check.split(','))
	# I try to take care of as much less smart user input as possible.
	if what_to_check == '':
		return True
	elif vs:
		if so_many == 2 or so_many == 3:
			if components_out_of_range(what_to_check, number_of_components, \
																	vs, three_d):
				return True
			else:
				return False
		#elif so_many == 3:
			#if components_out_of_range(what_to_check, number_of_components, \
																	#vs, three_d):
				#return True
			#else:
				#return False
		elif so_many == 4 and three_d:
			if components_out_of_range(what_to_check, number_of_components, \
																	vs, three_d):
				return True
			else:
				return False
		else:
			return True
	elif not vs and so_many > 1:
		return True
	elif components_out_of_range(what_to_check, number_of_components, \
																vs, three_d):
		return True
	else:
		return False



# The input may contain more then just one number.
# This function takes care that false_input() can still be used in this case. 
# Just the first two numbers matter
def components_out_of_range(what_to_check, number_of_components, \
											vs = False, three_d = False):
	components = what_to_check.split(',')
	if vs and three_d:
		number_of_numbers = 3
	elif vs:
		number_of_numbers = 2
	else:
		number_of_numbers = 1

	for i in range(number_of_numbers):
		try:
			if int(components[i]) not in range(1, (number_of_components + 1)):
				return True
		except ValueError:
			return True

	return False


# The function name says it all.
def plot_one_components_scores(number_of_components, R_2, graphtitle, \
												observations, Z_merged, colours):
	while True:
		text = "Which SCORE (input as integer) shall be plotted (ENTER go to Loadings): "
		plot_this = raw_input(text)
		if false_input(plot_this, number_of_components):
			return

		plot_scores(int(plot_this), R_2, graphtitle, observations, Z_merged, \
																colours = colours)


# The function name says it all.
def plot_one_components_loadings(number_of_components, R_2, graphtitle, \
															variables, P_merged):
	while True:
		text_1 = "Which LOADING (input as integer) shall be plotted "
		text_2 = "(ENTER go to Score vs Score): "
		plot_this = raw_input(text_1 + text_2)
		if false_input(plot_this, number_of_components):
			return

		plot_loadings(int(plot_this), R_2, graphtitle, variables, P_merged)



# Plotting of basic information.
def plotting_the_basics(number_of_components, R_2, graphtitle, observations, \
					variables, Z_merged, P_merged, colours = None):
	# Plot explained variance.
	show_explained_variance = raw_input("\nShow explained variance (1 = YES): ")
	if show_explained_variance == '1':
		plot_explained_variance(R_2, graphtitle)

	# Plot Scores.
	plot_one_components_scores(number_of_components, R_2, graphtitle, \
												observations, Z_merged, colours)

	# Plot Loadings.
	plot_one_components_loadings(number_of_components, R_2, graphtitle, \
															variables, P_merged)


# Dito
def score_vs_score(number_of_components, R_2, graphtitle, \
										observations, Z_merged, colours):
	while True:
		text_1 = '\nWhich SCORE vs SCORE (input as integers) shall be plotted?\n'
		text_2 = '=> "A, B, (C)" (C = with labels, ENTER go to Loading vs Loading): '
		plot_this = raw_input(text_1 + text_2)
		if false_input(plot_this, number_of_components, True):
			return

		plot_scores_vs_scores(plot_this, R_2, graphtitle, \
							observations, Z_merged, colours = colours)



# Dito
def loading_vs_loading(number_of_components, R_2, graphtitle, variables, \
															P_merged, colours):
	while True:
		text_1 = '\nWhich LOADING vs LOADING (input as integers) shall be plotted?\n'
		text_2 = ' => "A, B" (will always be with labels, '
		text_3 = 'ENTER go to Residuals over Hotellings T^2): '
		plot_this = raw_input(text_1 + text_2 + text_3)
		if false_input(plot_this, number_of_components, True):
			return

		plot_loadings_vs_loadings(plot_this, R_2, graphtitle, variables, \
														P_merged, colours = colours)


# Dito
def spe_vs_t_2(number_of_components, T_2, SPE, graphtitle, observations):
	while True:
		text_1 = '\nWhich T^2 (input as integer) shall be plotted '
		text_2 = '(ENTER go to CORRELATION LOADINGS): '
		plot_this = raw_input(text_1 + text_2)
		if false_input(plot_this, number_of_components):
			return

		plot_spe_over_t_2(plot_this, T_2, SPE, graphtitle, observations)



# Dito
def correlation_loadings(number_of_components, R_2, graphtitle, variables, \
															r_merged, colours):
	while True:
		text_1 = '\nWhich CORRELATION LOADINGS (input as integers) shall be plotted?\n'
		text_2 = '=> "A, B, (C)" (C = with labels, ENTER go to Loading vs Loading): '
		plot_this = raw_input(text_1 + text_2)
		if false_input(plot_this, number_of_components, True):
			return

		plot_loadings_vs_loadings(plot_this, R_2, graphtitle, variables, \
						r_merged, colours = colours, correlation_loading = True)



# Plot Scores over Scores over Scores and Loadings over Loadings over Loadings.
def three_d_plot(number_of_components, R_2, graphtitle, observations, \
										variables, P_merged, Z_merged, colours):
	while True:
		text_1 = '\nWhich SCORE (A) vs SCORE (B) vs SCORE (C) shall be plotted?\n'
		text_2 = '=> "A, B, C, (L)" (L = with labels): '
		plot_this = raw_input(text_1 + text_2)
		if false_input(plot_this, number_of_components, True, True):
			return

		plot_3D(plot_this, R_2, graphtitle, observations, \
						variables, P_merged, Z_merged, colours = colours)
	


# Plotting of the more complicated graphs.
def plotting_more_complicated_graphs(number_of_components, R_2, T_2, graphtitle, \
									SPE, observations, variables, Z_merged, \
									P_merged, r_merged, colours):
	text_1 = '\nWrite "2D" or "3D" to plot either Scores vs Scores etc. for just '
	text_2 = 'two components, \nor to plot three scores against each other in one\n'
	text_3 = 'graph and the three corresponding loadings in another graph at the '
	text_4 = 'same time. \n\nIn 3D you can align the data by "dragging" it around '
	text_5 = '(click and hold on the SCORES-Graph for aligning): '

	three_D_or_two_D = raw_input(text_1 + text_2 + text_3 + text_4 + text_5)

	if three_D_or_two_D == '2D':
		# Plot Scores over Scores.
		score_vs_score(number_of_components, R_2, graphtitle, \
										observations, Z_merged, colours)

		# Plot Loadings over Loadings.
		loading_vs_loading(number_of_components, R_2, graphtitle, variables, \
															P_merged, colours)

		# Plot Residuals over Hotelling's T_2.
		spe_vs_t_2(number_of_components, T_2, SPE, graphtitle, observations)

		# Plot Correlation Loadings.
		# This is the same as plotting loadings vs loadings above just with r_merged.
		correlation_loadings(number_of_components, R_2, graphtitle, variables, \
															r_merged, colours)

	else:
		three_d_plot(number_of_components, R_2, graphtitle, observations, \
										variables, P_merged, Z_merged, colours)




# Plot Score vs Score vs Score at the side of another graph with the 
# corresponding loadings.
# ATTENTION: This is a messy hack :( ... But I wanted to rotate both plots and
# I wanted the second plot to update when the first is rotated and I wanted 
# labels in the loadings plot. And that turned out to be rather ... well, messy
# in the end.
def plot_3D(plot_this, R_2, graphtitle, observations, variables, \
				P_merged, Z_merged, colours = False, legend = None, height = None):
	# For "linking" the two plots. See comment below.
	def on_click(event):
		# First change the angel of the camera.
		azim, elev = ax.azim, ax.elev
		xa.view_init(elev=elev, azim=azim)

		# Then change the position of the labels.
		# I "brute force" this by simply removing the old labels and 
		# make completely new ones.
		X_, Y_, foo = proj3d.proj_transform(P_merged[plot_a], P_merged[plot_b], \
												P_merged[plot_c], xa.get_proj())
		labels_= []
		for i in range(len(mg.labels)):
			label = mg.labels[i]
			label.remove()

			label_ = txt.Annotation(variables[i], xycoords = 'data', \
															xy = (X_[i], Y_[i]))
			xa.add_artist(label_)
			labels_.append(label_)

		mg.labels = []
		for element in labels_:
			mg.labels.append(element)


	plt.close()

	plot_these = plot_this.split(',')
	plot_a = int(plot_these[0]) - 1
	plot_b = int(plot_these[1]) - 1
	plot_c = int(plot_these[2]) - 1

	# If in the input a fourth thing is given, it is interpreted as to 
	# draw the labels onto each point.
	try:
		if plot_these[3] != 'risimif':
			plot_label = True
	except IndexError:
		plot_label = False

	percentage_a = int((R_2[plot_a + 1] - R_2[plot_a]) * 100)
	percentage_b = int((R_2[plot_b + 1] - R_2[plot_b]) * 100)
	percentage_c = int((R_2[plot_c + 1] - R_2[plot_c]) * 100)

	fig = plt.figure()
	# ax will be the scores.
	ax = fig.add_subplot(121, projection = '3d')
	ax.set_xlabel('Score PC-%s (%s %%)' % (plot_a + 1, percentage_a))
	ax.set_ylabel('Score PC-%s (%s %%)' % (plot_b + 1, percentage_b))
	ax.set_zlabel('Score PC-%s (%s %%)' % (plot_c + 1, percentage_b))

	# xa will be the loadings
	xa = fig.add_subplot(122, projection = '3d')
	xa.set_xlabel('Score PC-%s (%s %%)' % (plot_a + 1, percentage_a))
	xa.set_ylabel('Score PC-%s (%s %%)' % (plot_b + 1, percentage_b))
	xa.set_zlabel('Score PC-%s (%s %%)' % (plot_c + 1, percentage_b))
	text = "\n(Click + hold + drag on Scores-graph \nto align data in both graphs)"
	plt.title(graphtitle + text)

	if colours:
		ax.scatter(Z_merged[plot_a], Z_merged[plot_b], Z_merged[plot_c], \
														c = colours, s = 100)
		xa.scatter(P_merged[plot_a], P_merged[plot_b], P_merged[plot_c], \
														c = 'blue', s = 100)
	else:
		ax.scatter(Z_merged[plot_a], Z_merged[plot_b], Z_merged[plot_c], c = 'blue')
		xa.scatter(P_merged[plot_a], P_merged[plot_b], P_merged[plot_c], c = 'blue')

	if plot_label:
		# How to get labels into 3D-plot and make these updatable when the 
		# plot is rotated, is a bit complicated. I've pieced solutions 
		# together from here: 
		# http://stackoverflow.com/questions/12903538/label-3dplot-points-update
		# and here:
		# http://stackoverflow.com/questions/12222397/ ...
		# ... python-and-remove-annotation-from-figure
		# I also could not make it work without the use of my_globals

		# Transform the coordinates to get the initial 2D-projection
		X_, Y_, foo = proj3d.proj_transform(P_merged[plot_a], P_merged[plot_b], \
												P_merged[plot_c], xa.get_proj())

		mg.labels = []
		for i, text in enumerate(variables):
			# When the position of the label shall be updated, I first
			# remove the old label from the figure. To be able to do so, 
			# this label needs a .remove()-method. A txt.Annotation()-object
			# provides such a function. This works together with add_artist
			# below.
			label = txt.Annotation(text, xycoords = 'data', \
															xy = (X_[i], Y_[i]))
			# To be able to remove the label I need to add it like an 
			# artist to the canvas.
			xa.add_artist(label)

			mg.labels.append(label)
	
	if legend != None:
		fig.figimage(legend, 0, fig.bbox.ymax - height, zorder = 10)

	# Here I "link" the two subplots with each other so that if I 
	# move one plot the other is moved, too.
	# See here: http://stackoverflow.com/questions/23424282/ ...
	# ... how-to-get-azimuth-and-elevation-from-a-matplotlib-figure
	fig.canvas.mpl_connect('motion_notify_event', on_click)
	#fig.canvas.mpl_connect('button_release_event', on_release)

	plt.show()










