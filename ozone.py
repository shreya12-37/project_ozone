from flask import Flask , render_template
import sys
import os
import re
import filecmp
import subprocess 
from subprocess import CalledProcessError, TimeoutExpired 

app = Flask(__name__)

STATUS_CODES = {
	200: 'OK',
	201: 'ACCEPTED',
	400: 'WRONG ANSWER',
	401: 'COMPILATION ERROR',
	402: 'RUNTIME ERROR',
	403: 'INVALID FILE',
	404: 'FILE NOT FOUND',
	408: 'TIME LIMIT EXCEEDED'
}

@app.route("/practice_problem")
class Program:

	def __init__(self, filename, inputfile, timelimit, expectedoutput):
		self.filename = filename
		self.language = None
		self.name = None
		self.inputfile = inputfile
		self.expectedoutput = expectedoutput
		self.actualOutput = "calculatedoutput.txt"
		self.timelimit = timelimit

	def isvalidfile(self):
		validfile = re.compile("^(\\S+)\\.(java|cpp|c|py)$")
		matches = validfile.match(self.filename)
		if matches:
			self.name, self.language = matches.groups()
			if self.language == 'py':
				self.language = 'python'
			return True
		return False


	def compile(slef):

		

