import argparse
from Person import *
from random import randint
from rumorFunctions import *

#Move to rumor functions:
RUMOR_SIZE = 8
RUMOR_MAX_VALUE = (2 ** RUMOR_SIZE) - 1
DEFAULT_MODIFICATION_PROB = 0.1
RUN_TO_COMPLETION = 0


def validateProbability(prob):
	"""Called by the argument parser to validate the modification probability"""
	prob = float(prob)
	if not 0 <= prob <= 1:
		raise argparse.ArgumentTypeError("Probability must be bound by [0; 1]")
	return prob

def main():
	# Configure the argument parser
	parser = argparse.ArgumentParser()

	# Add filename
	parser.add_argument(dest = "networkFile",
						type = argparse.FileType("r"),
						help = "Text file to load the network from")

	parser.add_argument("-s", dest = "initiator", action = "store",
						type = str,
						help = "Name of the person initiating the rumor")
	
	parser.add_argument("-r", dest = "rumor", action = "store",
						type = int,
						default = randint(0, RUMOR_MAX_VALUE),
						help = "Value of the initial rumor")

	parser.add_argument("-t", dest = "steps", action = "store",
						type = int,
						default = RUN_TO_COMPLETION,
						help = "Number of steps in to simulate")

	parser.add_argument("-d", dest = "notAgain", action = "store_false",
						help = "Determines whether the rumor can be repeated to someone who already knows a version of it")
	# Add choice
	parser.add_argument("-m", dest = "modificationMode", action = "store",
						help = "Determines how the rumor is modified")

	parser.add_argument("-p", dest = "modificationProbablity", action = "store",
						type = validateProbability,
						default = DEFAULT_MODIFICATION_PROB,
						help = "Probability that the rumor will be modified when shared")
	# Add choice
	parser.add_argument("-u", dest = "updateMode", action = "store",
					   help = "Determines how a rumor is overwritten")

	args = parser.parse_args()

	# Load network and initialize the program
	people, network = loadNetwork(args.networkFile)
	
	# Inform the initiator of his version of the rumor
	next((p for p in people if p.name() == args.initiator)).setRumor(args.rumor)
	
	# Initialise modes and probability
	Person.setModificationMode(args.modificationMode)
	Person.setUpdateMode(args.updateMode)
	Person.setModificationProbability(args.modificationProbablity)
	update.notAgain = args.notAgain

	# Initial overview:
	print("Initial state of the network:")
	printState(people)

	# Main loop
	for i in range(args.steps):
		print("Step {}".format(i))
		learned = update(people, network)
		print("{} {} learned the rumor".format(learned, ("person" if learned == 1 else "people")))
		printState(people)

main()