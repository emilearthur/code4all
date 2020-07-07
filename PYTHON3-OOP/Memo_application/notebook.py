import datetime 

# store the next available id for all new notes 
last_id = 0 

class Note:
	"""Represent a note in the notebook. Match against 
	a string in searches and store tags for each note. """

	def __init__(self, memo, tags=""):
		"""initialize a note with memo and optinal
		space-separated tags. Auto. set the note's 
		created date and unqiue id. """
		self.memo = memo
		self.tags = tags
		self.created_date = datetime.date.today()
		global last_id 
		last_id += 1
		self.id = last_id

	def match(self, filter):
		"""Determine if this note matches the filter 
		text. Return True if it matches, otherwise False.

		Seach is case senstive and matches noth text and 
		tags. """
		return filter in self.memo or filter in self.tags

class Notebook:
	"""Represent a collection of notes that can be tagged, 
	modified, and searched."""

	def __init__(self):
		"""Initialize a notebook with an empty list."""
		self.notes = []

	def new_note(self, memo, tags=""):
		"""Create a new note and add it to the list."""
		self.notes.append(Note(memo, tags))


	def _find_note(self, note_id):
		"""Locate the note with the given id."""
		for note in self.notes:
			if str(note.id) == str(note_id):
				return note 
		return None 

	def modify_memo(self,note_id, memo):
		"""Find the notes with the given id and change its 
		memo to the giveb value."""
		self._find_note(note_id).memo = memo
		if note:
			note.memo = memo 
			return True 
		return False 

	def modify_tags(self,note_id, tags):
		"""Find the notes with a given id and change its 
		tags to the give value."""
		self._find_note(note_id).tags = tags
		if note:
			note.tags = tags
			return True 
		return False

	def search(self, filter):
		"""Find all the ntoes that match the given filter
		string."""
		return [note for note in self.notes if note.match(filter)]




