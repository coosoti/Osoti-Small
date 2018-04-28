"""Menu Class
"""
from api.models.database import Database

class Menu():
	"""Menu model
	"""

	def __init__(self):
		"""Initializes this class
		"""
		
	@classmethod
	def set_menu(cls, date, data):
		"""Set menu and store it into the main database
		"""
		Database.save_menu(date, data)
