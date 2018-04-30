"""User models
"""

from api.models.database import Database

class User(Database):
	"""User class
	"""

	@classmethod
	def save(cls, data):
		"""This method save user into the main store
		"""
		pass

	@classmethod
	def user_exists(cls, email):
		"""This method checks if user exists in the main store
		"""
		pass
	
	@classmethod
	def get_user(cls, email):
		"""This method checks if the user exists and return the user detail
		"""
		pass
	
	
	@classmethod
	def check_password(cls, user_id, raw_password):
		"""This method is user raw password is similar to the hashed password
		"""
		pass
		
		
	@classmethod
	def change_password(cls, user_id, password):
		"""This method updates the user password
		"""
		pass


	@classmethod
	def is_admin(cls, user_id, designation):
		"""Check is the designation on the user is admin
		""" 
		# for user in Store.users:
		# 	if user['designation'] == caterer:
		# 		return True
		# return False
		pass