from tkinter import *
from rumorFunctions import *
from NetworkFrame import *
from Person import *
from tkinter import filedialog

class GUI:

	def __init__(self, master):
		self.infoPanel = Frame(master)
		self.infoPanel.pack(side = LEFT, fill = BOTH, expand = True)
		Label(self.infoPanel, text = "Info:").pack(side = TOP)
		
		self.canvas = NetworkFrame(master)

		self.optionsPanel = Frame(master)
		self.optionsPanel.pack(side = LEFT, fill = BOTH, expand = True)
		Label(self.optionsPanel, text = "Options:").pack(side = TOP)
		Button(self.optionsPanel, text = "New Node", command = self.canvas.newNode).pack()
		Button(self.optionsPanel, text = "Load", command = self.load).pack()
		Button(self.optionsPanel, text = "Run", command = self.update).pack()

	def update(self):
		update(self.canvas.people, self.canvas.network)
		self.canvas.updateColors()

	def load(self):
		file = filedialog.askopenfile("r")
		people, self.canvas.network = loadNetwork(file)
		for p in people:
			self.canvas.newNode(p.name())
		self.canvas.update()

root = Tk()
app = GUI(root)
root.mainloop()