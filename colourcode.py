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

# ATTENTION: This is just an example.
# The colours of the dots in the scatterplots of the data the code was originally 
# programmed for, should have a certain colour according to sex and group. 
# This was encoded in the variable names (e.g. FB23 or MM42) but the list was 
# unordered.
# Hence, I look up just the "name" for each "sample/experiment" and made the 
# colours according to that information.

def colourcode(observations):
	colours = []
	for entry in observations:
		if entry[0] == 'F' and entry[1] == 'C':
			colours.append('blue')
		elif entry[0] == 'M' and entry[1] == 'C':
			colours.append('lightblue')
		elif entry[0] == 'F' and entry[1] == 'F':
			colours.append('black')
		elif entry[0] == 'M' and entry[1] == 'F':
			colours.append('grey')
		elif entry[0] == 'F' and entry[1] == 'B':
			colours.append('indigo')
		elif entry[0] == 'M' and entry[1] == 'B':
			colours.append('violet')
		elif entry[0] == 'F' and entry[1] == 'M':
			colours.append('green')
		elif entry[0] == 'M' and entry[1] == 'M':
			colours.append('lightgreen')
		elif entry[0] == 'F' and entry[1] == 'G':
			colours.append('red')
		else:
			colours.append('orange')

	return colours









