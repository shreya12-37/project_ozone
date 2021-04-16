import tempfile 
import os 
from Flask import flask,jsonify 
from db_query import *
from codechecker import *

d1={"status":200, "msg":"OK"}
d2={"status":420, "msg":"ERROR"}

@app.route('/problems/<username>/<problem_id>', methods=['get'])
def userSolvedProblem(username, problem_id):
	data = request.get_json()
	source_code=data['source_code'] 
	language = data['language']
	file = "source_code.json"
	#converting source code of user to respective text files
	with open(file,'r') as fi:
		pre=fi.read()
		lines=pre.split('\n')
		if language=="python":
			new_file = file.split('.')[0]+".py"
        elif language=="java":
        	new_file = file.split('.')[0]+".java"
        elif language=="c":
        	new_file = file.split('.')[0]+".c"
        elif language=="cpp":
        	new_file = file.split('.')[0]+".cpp"
		with open(new_file, "a") as nf:
			nf.write("\n".join(lines))
    
    #coverting input output data into temporary text file 
	code,res=allTestcase(problem_id)
	if code==200:
		for test in res:
			inputf=test[2]
		    outputf=test[3]
	        tempi = tempfile.TemporaryFile(mode='w+t')
		    tempo = tempfile.TemporaryFile(mode='w+t')
		    codeno,msg=None

		    try:
			    tempi.writelines(inputf)
			    tempo.writelines(outputf)
			    tempi.seek(0)
			    tempo.seek(0)
			    verdict = codechecker(
				    filename='new_file',
				    inputfile='tempi.txt',
				    expectedoutput='tempo.txt',
				    timeout=5,
				    check=True
				    )
			    d = {'username': username, 'problem_id':problem_id, 'verdict':verdict}
			    codeno,msg = insertingInsolve(d)
			except:
				return 420, "some error"
			#closing temporary files 
		    finally:
			    tempi.close()
			    tempo.close()

			if codeno==200:
				d1['msg']="verdict added to solve table"
				return jsonify(d1)
			else:
				return jsonify(d2)

	else:
		return jsonify(d2)





	
	

