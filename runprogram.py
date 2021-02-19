from ozone import *

class Program:
	def run(self):

		if not os.path.isfile(self.fileName):
			return 404, 'missing executable file'

		cmd = None
		if self.language == 'java':
			cmd = 'java {}'.format(self.name)
		elif self.language in ['c', 'cpp']:
			cmd = self.name
		elif self.language == 'python':
			cmd = 'python {}.py'.format(self.name)

		if cmd is None:
			return 403, 'File is of invalid type'

		try:
			with open('calculatedoutput.txt', 'w') as fout:
				fin = None
				if self.inputFile and os.path.isfile(self.inputFile):
					fin = open(self.inputFile, 'r')
				proc = subprocess.run(
					cmd,
					stdin=fin,
					stdout=fout,
					stderr=subprocess.PIPE,
					timeout=self.timeLimit,
					universal_newlines=True
					)
			if proc.returncode != 0:
				return 402, proc.stderr
			else:
				return 200, None
		except TimeoutExpired as tle:
			return 408, tle
		except CalledProcessError as e:
			print(e.output)

		if self.language == 'java':
			os.remove('{}.class'.format(self.name))
		elif self.language in ['c', 'cpp']:
			os.remove(self.name)

	def match(self):
		if os.path.isfile(self.actualOutputFile) and os.path.isfile(self.expectedOutputFile):
			result = filecmp.cmp(self.actualoutputFile, self.expectedOutputFile, shallow=False)
			if result:
				return 201, None
			else:
				return 400, None
		else:
			return 404, 'Missing output files'
			