from Person import *
from random import choice

def loadNetwork(file):
	"""
	Initializes the network from a text file
	"""
	people, friends = [], []
	for i, line in enumerate(file):
		people.append(Person(line.split(':')[0].strip(), i))
		friends.append([n.strip() for n in line.split(':')[1].split(",")])
		
	l = len(people)
	network = [[(True if people[i].name() in friends[j] else False) for i in range(l)] for j in range(l)]
	
	return (people, network)

def printState(people):
	"""
	Prints the state of the rumor's propagation
	"""
	print("{0:15}{1:10}{2:5}".format("NAME","BIN","DEC"))
	for p in people:
		if p.isInformed():
			s = "{0:15}{1:0>8b}{1:5}".format(p.name(), p.rumor())
		else:
			s = "{0:15}-- Not informed --".format(p.name())
		print(s)

def update(people, network):
	"""
	Runs one step of the simulation. Each informed member of the network choses and informs
	one friend of the rumor.
	Returns the number of people who learned the rumor for th first time
	"""
	informed = 0
	for p in (p for p in people if p.isInformed()):
		friends = [people[i] for i in range(len(network)) if network[p.index()][i]]
		if update.notAgain:
			friends = [f for f in friends if not f.isInformed()]
		if friends:
			friendToInform = choice(friends)
			if not friendToInform.isInformed():
				informed += 1
			p.tell(friendToInform)
		return informed
update.notAgain = False