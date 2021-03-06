import sys
from pprint import pprint
import copy
import argparse


def loadgraph(filename):
	""" loads the graph from a file into memory """

	try:
		f = open(filename, 'r')
	except IOError:
		print "Failed to open '" + filename + "'."
		exit()

	graph = {}
	# first line is the number of nodes in the graph. skip it
	next(f)

	for line in f:
		tmp = line.split()
		if len(tmp) != 2:
			print "Malformed line in file."
			f.close()
			exit()
		tail = int(tmp[0])
		head = int(tmp[1])

		if tail not in graph:	# let us add a new node
			graph[tail] = []
		graph[tail].append(head)	# tail can get to head
		if head not in graph:
			graph[head] = []
	f.close()	# close the file
	return graph


def prompt():
	""" prompts user to provide an origin and a destination """
	src = raw_input("\nSource: ")
	dest = raw_input("Destination: ")

	if not src.isdigit() or not dest.isdigit():
		if src == dest == '':
			print "You chose to quit. Bye."
		else:
			print "Invalid input. Need integers."
		exit()

	src = int(src)
	dest = int(dest)
	if src not in graph:
		print "No node " + str(src) + " in graph."
		exit()
	if dest not in graph:
		print "No node " + str(dest) + " in graph."
		exit()
	return (src, dest)


def BFS(graph, src, dest):

	fringe = set([src])
	newfringe = set()
	visited = {}
	dest_found = False

	# all nodes not visited
	for node in graph:
		visited[node] = (False, None)

	# do a BFS to find dest
	while fringe:
		for node in fringe:
			if node == dest:
				dest_found = True
				fringe = set()	# breaks the while loop
				break

			for neighbour in graph[node]:
				if not visited[neighbour][0]:
					newfringe.add(neighbour)
					visited[neighbour] = (True, node)

		fringe = set(newfringe)
		newfringe = set()

	if dest_found:
		path = []
		node = dest
		while node != src:
			path.append(node)
			node = visited[node][1]
		return path + [src]
	return []


def reverse_path(graph, path):

	i = 1
	src = path[-1]
	node = path[0]
	while node != src:
		next = path[i]
		graph[node].append(next)
		graph[next].remove(node)
		i += 1
		node = next


def count_disjoint(graph, src, dest, ret_graph=False): # Edmond Karp

	if src == dest:
		if ret_graph:
			return graph
		return 0

	graph = copy.deepcopy(graph)	# change graph only in this scope

	# all disjoint paths have been found when we can't find dest anymore
	nr_disjoint = -1
	path = True
	while path:
		nr_disjoint += 1
		path = BFS(graph, src, dest)

		# backtrace from dest to scr and invert edges
		if path:
			reverse_path(graph, path)

	if ret_graph:
		return graph
	return nr_disjoint


def statistics(graph):
	
	separated_by = {} # k indexes the dictionary. separated_by[k] = number of pairs of nodes that get separeted if k links fail
		
	for nodeA in graph: 
		for nodeB in graph:
			if nodeA != nodeB: # for each pair of distinct nodes compute the number of disjoint paths
				current_k = count_disjoint(graph, nodeA, nodeB) 
				if current_k != 0: # if the pair has at least k >= 1 disjoint paths, increment the number of pairs that get disconnected by k link failures 
					try:
						separated_by[current_k] += 1
					except KeyError, err:
						separated_by[current_k] = 1 # create new dictionary entries only has needed, instead of initializing a large number of possible indexes

	print_statistics(graph, separated_by)


def print_statistics(graph, separated_by):
	total_connected = 0
	total_pairs = len(graph)*(len(graph)-1)

	try: 
		max_k = max(separated_by)
	except ValueError:
		return # if the graph has only one node this will fail and link_connectivity() already has an apropriate print

	for k in separated_by: # count the total number of connections that exist by adding all the values of the dictionary
		total_connected += separated_by[k]

	print "\n %s  fraction of pairs with at least k link-disjoint paths between them" % "k".rjust(len(str(max_k)))
	for k in range(1, max_k+2): # print all values of k until the maximum one, not only the values that make new connections fail

		nbars = int((total_connected/float(total_pairs))*50)
		print "{0}  {1} {2:.2f}".format(" " + str(k).rjust(len(str(max_k))), '|' * nbars, total_connected/float(total_pairs))

		try:
			total_connected -= separated_by[k]
		except KeyError:
			pass	# if, for example, k=3 added no new failures, separated_by[3] does not exist so we ignore the KeyError
	print


def link_connectivity(graph):
	min_k = None
	for nodeA in graph:
		for nodeB in graph:
			if nodeA != nodeB:
				k = count_disjoint(graph, nodeA, nodeB)
				
				if k == 0: # means at least one pair is already disconnected
					print "This graph is not strongly connected. " + str(nodeA) + " cannot reach " + str(nodeB) + "."
					return
				if k < min_k or min_k == None: # if found a new minimum k or first k computed 
					min_k = k
					exampleA = nodeA
					exampleB = nodeB
	
	if min_k == None: # only happens if there are no pairs, i.e. there's only one node
		print "This graph has only one node."
		return

	print "The graph is " + str(min_k) + "-edge-connected."
	print "example: make " + str(exampleA) + " unable to reach " + str(exampleB) + ". Break the following links"

	new_graph = count_disjoint(graph, exampleA, exampleB, True)

	for peer in [item for item in graph[exampleA] if not item in new_graph[exampleA] or new_graph[exampleA].remove(item)]:
		print " %s -> %s" % (exampleA, peer)


# parse script options
parser = argparse.ArgumentParser()
parser.add_argument("graph_file", help = "path for a graph file")
parser.add_argument("-ds", "--disable-stats", help = "do not compute graph stats", action="store_true")
parser.add_argument("-dp", "--disable-prompt", help = "do not show prompt", action="store_true")
parser.add_argument("-dc", "--disable-connectivity", help = "do not compute link-connectivity", action="store_true")
args = parser.parse_args()


graph = loadgraph(args.graph_file)
#pprint(graph)
if not args.disable_stats:
	statistics(graph)
if not args.disable_connectivity:
	link_connectivity(graph)
if not args.disable_prompt:
	print "\nPress Return twice to exit."
	while True:
		src, dest = prompt()
		print "No. of disjoint paths: " + str(count_disjoint(graph, src, dest))
