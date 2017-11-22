from tkinter import *
from rumorFunctions import *
from random import randint
import tkinter.simpledialog as simpleDialog
from math import sin, cos
from tkinter.colorchooser import *

class NetworkFrame:
	def __init__(self, master):
		self.canvas = Canvas(master)
		self.canvas.pack(side = LEFT, fill = BOTH, expand = True)
		self.canvas.config(bg = "lightblue")
		self.radius = 20
		self.people= []
		self.network = []

	def newNode(self, n = None):
		x = randint(0, self.canvas.winfo_width() - self.radius)
		y = randint(0, self.canvas.winfo_height() - self.radius)

		self.canvas.create_oval(x,
					y,
					x + self.radius * 2,
					y + self.radius * 2,
					width = 3,
					fill = "black",
					disableddash = (5, 5),
					state = DISABLED,
					activeoutline = "red",
					activewidth = 2,
					tags = "cur")

		name = simpleDialog.askstring("New Node", "Name:") if not n else n
		if name == None:
			name = ""
		p = Person(name, len(self.people))
		p.setRumor(0)
		self.people.append(p)
		self.canvas.addtag_withtag(name, "cur")
		self.canvas.dtag(name, "cur")
		self.canvas.itemconfig(name, state = NORMAL)
		self.canvas.tag_bind(name, "<Double-Button-1>", self.deleteNode)
		self.canvas.tag_bind(name, "<Button-3>", self.setColor)
		self.canvas.delete("cur")
		if not n:
			self.update()

	def deleteNode(self, event):
		name = self.canvas.gettags(CURRENT)[0]
		print(name)
		self.canvas.delete(CURRENT)
		person = next((p for p in self.people if p.name() == name))
		self.people.remove(person)
		self.update()

	def setColor(self, event):
		name = self.canvas.gettags(CURRENT)[0]
		color = askcolor()[1]
		rumor = int(color[1:], 16)
		print(color)
		person = next((p for p in self.people if p.name() == name))
		person.setRumor(rumor)
		self.canvas.itemconfig(name, fill = color)

	def update(self):
		nbNodes = len(self.people)
		if nbNodes > 0:
			incr = 360 / nbNodes

			for i, p in enumerate(self.people):
				x = (self.canvas.winfo_width() / 2)  + (cos(i*incr) * 150)
				y = (self.canvas.winfo_height() / 2) + (sin(i*incr) * 150)
				r = self.radius
				self.canvas.coords(p.name(), x-r, y+r, x+r, y-r)

	def updateColors(self):
		for p in self.people:
			color = hex(p.rumor())
			color = color[2:]
			color = "#" + color
			color = format(p.rumor(), '06x')
			color = "#" + color
			self.canvas.itemconfig(p.name(), fill = color)
