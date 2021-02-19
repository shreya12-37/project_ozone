from ozone import *
from runprogram import *
import re

class Program:
	def compile(self):
		if os.path.isfile(self.name):
			os.remove(self.name)

		if not os.path.isfile(self.fileName):
			return 404, 'Missing file'

		cmd = None 
		if self.language == 'java':
			cmd = 'javac {}'.format(self.fileName)
		elif self.language == 'java':
			cmd = 'gcc -o {0} {1}'.format(self.name, self.fileName)
		elif self.language == 'cpp':
			cmd = 'g++ -o {0} {1}'.format(self.name, self.fileName)
		else:
			return 200, None

		if cmd is None:
			return 403, 'File is of invalid type'

		try:
			proc = subprocess.run(
				cmd,
				stdout=subprocess.PIPE,
				stderr=subprocess.PIPE,
				universal_newlines=True
				)

			if proc.returncode != 0:
				return 401, proc.stderr
			else:
				return 200, None

		except CalledProcessError as e:
			print(e.output)
			

