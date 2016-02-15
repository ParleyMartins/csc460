import random


def randsat(n, k, m):
	cnf = [] #m elements
	for i in range(0, m):
		clause = [] #This will have k elements from 1 to n
		for j in range(0, k):
			random.seed()
			literal = random.randint(1, n)
			literal = literal * random.choice([1, -1])
			clause.append(literal)
		cnf.append(clause)
	return cnf


def satcom(cnf):
	assign = {0: 0, }
	cnf_length = len(cnf)
	for i in range(0, cnf_length):
		clause_len = len(cnf[i])
		if(clause_len > 0):
			for j in range(0, clause_len):
				primitive = cnf[i][j]
				if(primitive < 0):
					primitive = primitive * -1;
				assign[primitive] = 0
		else:
			assign = None
			break
	if(assign != None):
		cnf_copy = cnf
		primitive = 0
		for i in range(0, len(cnf_copy)):
			primitive = cnf_copy[i][0]
			if(primitive > 0):
				primitive = primitive * -1
			if(primitive in cnf_copy[i]):
				cnf_copy.remove(cnf_copy[i])
		for i in range(0, len(cnf_copy)):
			primitive = primitive * -1
			assign[primitive] = 1
			if(primitive in cnf_copy[i]):
				cnf_copy[i].remove(primitive)
		satcom(cnf_copy)
	return assign


print(satcom([[1, 2],[-1, 4]]))
# pick any primitive proposition i that occurs in C
# assign[i] := −1
# r := satcom(assign i false in C)
# if r = NULL
# assign[i] := 1
# r := satcom(assign i true in C)
# endif
# if r = NULL
# return NULL
# else
# return assign
# function“assign i false in C”
# Temporarily remove all clauses from C that contain −i
# Temporarily remove i from remaining clauses
# function“assign i true in C”
# Temporarily remove all clauses from C that contain i
# Temporarily remove −i from remaining clauses
# Note: all clauses and literals removed from C have to be restored to their previous state after
# each backtrack.