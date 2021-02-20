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
		print('Compiling {0}({1})'.format(STATUS_CODES[compileResult], compileResult), flush=True)
		if compileErrors is not None:
			sys.stdout.flush()
			print(compileErrors, file=sys.stderr)
			exit(0)

		runtimeResult, runtimeErrors = newprogram.run()
		print('Running {0}({1})'.format(STATUS_CODES[runtimeResult], runtimeResult), flush=True)
		if runtimeErrors is not None:
			sys.stdout.flush()
			print(runtimeErrors, file=sys.stderr)
			exit(0)

		if check:
			matchResult, matchErrors = newprogram.match()
			print('Verdict  {0}({1})'.format(STATUS_CODES[matchResult], matchResult), flush=True)
			if matchErrors is not None:
				sys.stdout.flush()
				print(matchErrors, file=sys.stderr)
				exit(0)
	else:
		print('FATAL: Invalid file', file=sys.stderr)
