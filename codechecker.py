from ozone import *
from runprogram import *
from compileprogram import *

def codechecker(filename, inputfile=None, expectedoutput=None, timeout=1, check=True):
	newprogram = Program(
		filename=filename,
		inputfile=inputfile,
		timelimit=timeout,
		expectedoutputfile=expectedoutput)

	if newprogram.isvalidfile():
		print('Executing code checker')

		compileResult, compileErrors = newprogram.compile()
