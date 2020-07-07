class IntroToPython:
	def lesson(self):
		return f"""
			Hello {self.student}. define two variables, 
			an integer named with value 1 and string named b 
			with value 'hello'

		"""

	def check(self, code):
		return code == "a = 1/nb = 'hello'"


# starting with abstract base class 
class Assignment(metaclass=abc.ABCMeta):
	@abc.abstractmethod
	def lesson(self, student):
		pass 

	@abc.abstractmethod
	def check(self, code):
		pass 

	@classmethod 
	def __subclasshook__(cls,C):
		if cls is Assignment:
			attrs = set(dir(C))
			if set(cls.__abstractmethods__) <= attrs:
				return True 

		return NotImplemented


class Statistics(Assignment):
	def lesson(self):
		return (
			"Good work so far, "
			+ self.student
			+ ". Now calculate the average of the numbers "
			+ " 1, 5, 18, -3 and assign to a variable named ' avg'"
			)

	def check(self, code):
		import statistics

		code = "import statistics\n" + code

		local_vars = {}
		global_vars = {}

		return local_vars.get("avg") == statistics.mean([1,15,18,-3])


# class manages how many attempts student should make 
class AssignmentGrader:
	def __init__(self, student, AssignmentClass):
		self.assignment = AssignmentClass()
		self.assignment.student = student 
		self.attempts = 0 
		self.correct_attempts = 0

	def check(self, code):
		self.attempts += 1
		results = self.assignment.check(code) 
		if results:
			self.correct_attempts += 1

		return results 

	def lesson(self):
		return self.assignment.lesson()

import uuid
class Grader:
	def __init__(self):
		self.student_graders = {}
		self.assignment_classes = {}

	def register(self, assignment_classes):
		if not issubclass(assignment_class, Assignment):
			raise RuntimeError(
				"Your class does not have the right method"
				)
		id = uuid.uuid4() 
		self.assignment_classes[id] = assignment_class
		return id 


# main file 
from grader import Grader 
from lessons import IntroToPython, Statistics

grader = Grader()
itp_id = grader.register(IntroToPython) 