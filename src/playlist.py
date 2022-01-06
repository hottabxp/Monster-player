import sqlite3

class Playlist():

	def __init__(self):
		self.connect = sqlite3.connect('pls.db')
		self.cursor = self.connect.cursor()

	def getStations(self):
		self.cursor.execute('SELECT * FROM radio')
		result = self.cursor.fetchall()
		# print(result)
		return result
