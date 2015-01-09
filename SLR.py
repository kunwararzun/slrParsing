#SLR parsing in Python 
#Compiler Construction Mini Project 
'''
@Author : Arjun Kunwar 
'''
goto_sn = 1
next_state_sn = 1
def main():
	global goto_sn
	global next_state_sn
	print "\nSLR Parsing\n"
	print "Augmented Grammar"
	print "S'>S"
	print "S>L=R"
	print "S>R"
	print "L>*R"
	print "L>i"
	print "R>L \n"
	augmented = {1:"S'>S",2:"S>L=R",3:"S>R",4:"L>*R",5:"L>i",6:"R>L"} #dictionary for given augmented grammar
	
	follow = {} 	#dictionary follow                         
	follow.update({1:["S'",['$']]})
	follow.update({2:['S',['$']]})
	follow.update({3:['L',['$','=']]})
	follow.update({4:['R',['$','=']]})
	
	print "Closure"
	closure = {}
	closure = compute_closure(augmented,closure)  # for computing closure ,adding dot

	print "\nNon terminals"	
	nonterminals = []
	nonterminals = compute_nonterminals(augmented,nonterminals)#Finding the nonterminals in the grammar
	print nonterminals	

	
	print "\nTerminals"
	terminals = ['$']		
	terminals = compute_terminals(augmented,terminals,nonterminals) #Finding the terminals in the grammar
	print terminals
	
	goto = {}	# goto dictionary
	print "\nGOTO"
	goto = goto_closure(goto,closure,terminals,nonterminals) #Operating on closure and constructing goto - initial state, symbol, grammar, next state
	goto = goto_next(goto,closure,terminals,nonterminals)	#Operating on the states computed by the above function and constructing goto - initial state, symbol, grammar, next state	
	display_goto(goto)  #displaying the contentes of goto
	
	slr_table = {} 				# constructing the slr table
	ruleA(goto,slr_table,terminals) 	# shift operation
	ruleB(goto,slr_table)			# accept operation				
	ruleC(augmented,goto,slr_table,follow)	# reduce operation
	ruleD(goto,slr_table,nonterminals)	# goto operation
	print "---------------------SLR parsing table-----------------------"
	for key in slr_table.keys():            #displaying the contents of slr table
		print key, " ", slr_table[key],"\n"
	
	input_string = "i=i*i"
	input_string = input_string+"$"
	check_input("0",input_string, slr_table,augmented) #checking the input string

def compute_closure(augmented,closure):	# Closure Operation adding dot in each rule after > sign 
	key = 1
	while(key<=len(augmented)): 
		temp = augmented[key]
		j = 0
		while(temp[j] != ">"):
			j = j+1
		new = temp[0:j+1]+"."+temp[j+1:]
		closure[key] = new
		print closure[key]
		key = key + 1
	return closure

def compute_nonterminals(augmented,nonterminals):#Finding the nonterminals in the grammar	
	key = 1
	while(key<=len(augmented)): 
		temp = augmented[key]
		j = 0
		while(temp[j] != ">"):
			j = j+1
		if(len(temp[0:j]) == 1 and temp[0:j] not in nonterminals):
			nonterminals = nonterminals + [temp[0:j]]
		key = key + 1			
	return nonterminals

def compute_terminals(augmented,terminals,nonterminals): #Finding the terminals in the grammar
	key = 2	
	while(key<=len(augmented)): 
		temp = augmented[key]
		j = 0
		while(j<=len(temp)-1):
			if( temp[j] != ">" and temp[j] not in nonterminals and temp[j] not in terminals):
				terminals = terminals + [temp[j]]
			j = j+1
		key = key + 1			
	return terminals

def goto_closure(goto,closure,terminals,nonterminals):#Operating on closure and constructing goto - initial state, symbol, grammar, next state
	global goto_sn
	global next_state_sn
	key = 1
	while(key<=len(closure)):		
		temp = closure[key]
		j = temp.index('.') 		#position of dot
		temp = list(temp)
	   	after_dot = temp[j+1] 		#dot swap
		temp[j] = after_dot
		temp[j+1] = "."
		dot_shifted = ''.join(temp)
		if search_dict(goto,0, after_dot) == 0:  		#for non repeated symbols
			if(len(dot_shifted)-1 == dot_shifted.index('.') or dot_shifted[dot_shifted.index('.')+1] in terminals): #when the dot reaches end of the grammar or when terminals comes after the dot
				grammar_list = []
				grammar_list.append(dot_shifted)			
				goto[goto_sn] = [0,after_dot,grammar_list,next_state_sn] 
				goto_sn = goto_sn + 1		
				next_state_sn = next_state_sn + 1
			else:	# when non terminals comes after the dot
				grammar_list = []
				grammar_list.append(dot_shifted)
				for values in expand_nonterminals(closure,nonterminals, dot_shifted[dot_shifted.index('.')+1]):
					if(values not in grammar_list):
						grammar_list.append(values)	
				goto[goto_sn] = [0,after_dot,grammar_list,next_state_sn] 
				goto_sn = goto_sn + 1		
				next_state_sn = next_state_sn + 1
		else:  						#for repeated symbols		
			if(len(dot_shifted)-1 == dot_shifted.index('.') or dot_shifted[dot_shifted.index('.')+1] in terminals): #when the dot reaches the end of grammar or when terminals comes after the dot
				if(dot_shifted not in goto[search_dict(goto,0, after_dot)][2]):  			
					goto[search_dict(goto,0, after_dot)][2].append(dot_shifted) #duplication may occur
				
			else:	# when non terminals comes after the dot	
				if(dot_shifted not in goto[search_dict(goto,0, after_dot)][2]): 	
					goto[search_dict(goto,0, after_dot)][2].append(dot_shifted) 
				for values in expand_nonterminals(closure,nonterminals, dot_shifted[dot_shifted.index('.')+1]):
					if(values not in goto[search_dict(goto,0, after_dot)][2]):
						goto[search_dict(goto,0, after_dot)][2].append(values)					 
		key = key + 1
	
	return goto 


def goto_next(goto,closure,terminals,nonterminals):
	global goto_sn
	global next_state_sn
	i = 1
	while(i <=len(goto)):	# closure operation  ..displaying the contents of goto
		grammar_list = goto[i][2]
		for temp in grammar_list:
			if (not (len(temp)-1 == temp.index('.'))): 		#if dot is not in last  position of the grammar
				j = temp.index('.') 		#position of dot
				temp = list(temp)
	   			after_dot = temp[j+1] 		#dot swap
				temp[j] = after_dot
				temp[j+1] = "."
				dot_shifted = ''.join(temp)
				if search_dict(goto, goto[i][3], after_dot) == 0:  		#for non repeated symbols
					if(len(dot_shifted)-1 == dot_shifted.index('.') or dot_shifted[dot_shifted.index('.')+1] in terminals): #when the dot reaches end of the grammar or when terminals comes after the dot
						grammar_list = []
						grammar_list.append(dot_shifted)			
						check = check_grammar(goto, grammar_list)
						if (check == 0):
							goto[goto_sn] = [goto[i][3],after_dot,grammar_list,next_state_sn]
							next_state_sn = next_state_sn + 1
						else:
							goto[goto_sn] = [goto[i][3],after_dot,grammar_list,goto[check][3]]
						goto_sn = goto_sn + 1
								
					else:	# when non terminals comes after the dot
						grammar_list = []
						grammar_list.append(dot_shifted)
						for values in expand_nonterminals(closure,nonterminals, dot_shifted[dot_shifted.index('.')+1]):
							if(values not in grammar_list):
								grammar_list.append(values)	
						check = check_grammar(goto, grammar_list)		
						if (check == 0):
							goto[goto_sn] = [goto[i][3],after_dot,grammar_list,next_state_sn]
							next_state_sn = next_state_sn + 1
						else:
							goto[goto_sn] = [goto[i][3],after_dot,grammar_list,goto[check][3]]
						goto_sn = goto_sn + 1
							
				else:  #for repeated symbols		
					if not (len(dot_shifted)-1 == dot_shifted.index('.') or dot_shifted[dot_shifted.index('.')+1] in terminals):# when non terminals comes after the dot	
						if(dot_shifted not in goto[search_dict(goto,goto[i][0], after_dot)][2]): 	
							goto[search_dict(goto,goto[i][0], after_dot)][2].append(dot_shifted) 
						for values in expand_nonterminals(closure,nonterminals, dot_shifted[dot_shifted.index('.')+1]):
							if(values not in goto[search_dict(goto,goto[i][0], after_dot)][2]):
								goto[search_dict(goto,goto[i][0], after_dot)][2].append(values)	 									
		i = i + 1
	return goto

def display_goto(goto):		#displaying the contents of goto
	i = 1
	while(i <=len(goto)):	
		print goto[i],"\n"
		i = i + 1

def ruleA(goto,slr_table,terminals): #Shift Operation
	i = 1
	print "\nAction: Shift Operations"
	while(i <=len(goto)):
		if goto[i][1] in terminals:
			a =  goto[i][0] 
			b =  str(goto[i][1])
			c =  "S"+str(goto[i][3])
			print "Action[",a,",",b,"]=  Shift ",c
			if a in slr_table.keys():
				slr_table[a].append([b,c]) 
			else:
				slr_table.update({a:[[b,c]]})
		i = i + 1
	print "\n"

def ruleB(goto,slr_table): #Accept Operation
	a =  goto[1][3] 
	b = "$"
	c =  "Accept"
	print "\nAction: Accept Operation"
	print "action[",a,",",b,"]= ",c
	slr_table.update({a:[[b,c]]})
	print "\n"
			
def ruleC(augmented,goto,slr_table,follow):#reduction Operation
	print "\nAction: Reduce Operations"
	print "Follow = ",follow
	key = 2
	temp = []
	while(key<=len(goto)):
		for item in goto[key][2]:
			i = item.index('.')
			if (i == len(item)-1 and [item,goto[key][3]] not in temp):
				temp = temp + [[item,goto[key][3]]]
				reduce = "R"+ str(augmented.keys()[augmented.values().index(item[0:len(item)-1])]-1)
				a = 2
				while(a <= len(follow)):
					if(item[0:1] == follow[a][0]):
						for follow_values in follow[a][1]:
							print "Action[",goto[key][3],",",follow_values,"]=  Reduce",item[0:len(item)-1],"\t",reduce
							if goto[key][3] in slr_table.keys():
								slr_table[goto[key][3]].append([follow_values,reduce])
							else:
								slr_table.update({goto[key][3]:[[follow_values,reduce]]})
					a = a + 1
		key = key + 1
	print "\n"

def ruleD(goto,slr_table,nonterminals): #goto Operation
	i = 1
	print "\nGoto Operations"
	while(i <=len(goto)):
		if goto[i][1] in nonterminals:
			a =  goto[i][0] 
			b =  str(goto[i][1])
			c =  goto[i][3]
			print "GOTO(",a,",",b,")= ", c
			if a in slr_table.keys():
				slr_table[a].append([b,c]) 
			else:
				slr_table.update({a:[[b,c]]})
		i = i + 1
	print "\n"

		
def check_input(stack,input,slr_table,augmented): 
		sptr = 0
		iptr = 0
		while(iptr <= len(input)-1):
			ichar = input[iptr]
			i = 0
			for values in slr_table[int(stack[sptr])]:
				if(values[0] == ichar):
					i = i + 1			
			if(i == 0):
				print "Unaccepted"
				break
			elif(i == 1):
				for values in slr_table[int(stack[sptr])]:
					if(values[0] == ichar):
						if(values[1][0] == 'S'):
							print "Stack\t",stack,"\tInput\t",input[iptr:] ,"\tAction Shift Operation\t",values[1]
							stack = stack + input[iptr]
							iptr = iptr + 1
							stack = stack + values[1][1]
							sptr = sptr + 2
						elif(values[1][0] == 'R'):
							print "Stack\t",stack,"\tInput\t",input[iptr:] ,"\tAction Reduce Operation\t",values[1]
							aug_grm = augmented[int(values[1][1])+1]
							trunc = ''.join(aug_grm)
							indx = trunc.index(">")							
							after_eq_length =len(trunc[indx+1:])
							a = len(stack)- 2 * after_eq_length
							stack = stack[0:a]
							add = augmented[int(values[1][1])+1][0][0]
							stack = stack + add
							state = int(stack[len(stack)-2])							
							for values in slr_table[state]:
								if (values[0] == add):
									stack = stack + str(values[1])
									sptr = sptr - 2 * after_eq_length+2
						else:
							print "Stack	",stack,"\tInput	",input[iptr:] ,"\tAccepted"
							iptr = iptr + 1
							
			else:
				print "Stack\t",stack,"\tInput\t",input[iptr:] ,"\tOperation?\t"
				for values in slr_table[int(stack[sptr])]:
					if(values[0] == ichar):
						print values[1]
				print "Confict"
				break



	
def check_grammar(goto, grammar_list): #to check whether the grammar is repeated or not in the goto table
	check = 1					
	while (check <= len(goto)):
		if(goto[check][2] == grammar_list):
			return check
			break		
		check = check + 1
	return 0

def search_dict(dict_name,state, value): #Search for the operated symbol which is repeated and returns its key
	key = 1
	while(key<len(dict_name)+1):
		if(dict_name[key][0] == state and dict_name[key][1] == value):
			return key
			break		
		key = key + 1
	return 0

def expand_nonterminals(closure_grammar,nonterminals_list, non_term): # for expanding non terminals
	key = 2
	new_list = []
	while(key<= len(closure_grammar)):
		temp = closure_grammar[key]
		if(non_term == temp[0:1]):
			new_list = new_list + [temp]
		key = key + 1
	l = 0
	save = []
	while(l < len(new_list)):
		nt = new_list[l].index('.') + 1		
		if(new_list[l][nt] in nonterminals_list and new_list[l][nt] not in save ):
				key = 2
				save.append(new_list[l][nt])
				while(key<= len(closure_grammar)):
					temp = closure_grammar[key]
					if(new_list[l][nt] == temp[0:1]):
						new_list = new_list + [temp]
					key = key + 1	
		l = l + 1
	unique_list = []
	for sublist in new_list:
		if sublist not in unique_list:
			unique_list.append(sublist)
	return unique_list	

'''	
def follow(aug,ter,non_ter):
	follow = {}
	follow.update({1:[aug[1][0:2],['$']]})
	key = 1
	i = 1
	while(i<=len(aug)):
		temp = aug[i]
		j = temp.index('>') + 1
		while(j <= len(temp)-1):
			if(temp[j] in non_ter): # for non terminals in rhs of the grammar
				if(j != len(temp)-1): #if the nonterminal is not at last of the grammar
					print "In grammar :",temp, ",",temp[j],"follows",temp[j+1]
					if( check_follow(follow,temp[j],0) != 0):
						if temp[j+1] not in follow[check_follow(follow,temp[j],0)][1]:
							follow[check_follow(follow,temp[j],0)][1].append(temp[j+1])
					else:
						key = key + 1
						follow.update({key:[temp[j],[temp[j+1]]]})
				else: #if non terminal is at the last of grammar
					print "In grammar :",temp, ",",temp[j],"follows",temp[0:temp.index('>')]
					if( check_follow(follow,temp[j],0) != 0):
						if temp[0:temp.index('>')] not in follow[check_follow(follow,temp[j],0)][1]:
							follow[check_follow(follow,temp[j],0)][1].append(temp[0:temp.index('>')])
					else:
						key = key + 1
						follow.update({key:[temp[j],[temp[0:temp.index('>')]]]})		
			j = j + 1
		i = i + 1
	print follow
	key = 2
	while(key <= len(follow)):
		i = 0
		for item in follow[key][1]:
			if(item == follow[1][0]):
				follow[key][1][i] = ''.join(follow[1][1])
			elif (item in non_ter):
				a = 2
				while(follow[a][0] != item):
					a = a + 1
				if(item != follow[key][0]):
					follow[key][1].append(follow[a][1])
			i = i + 1
		key = key + 1
	print follow
	key = 2
	while(key <= len(follow)):
		temp = []
		print follow[key][1]		
		for value in ter:
			print "............"
			#print next(subl for subl in follow[key][1] if value in subl,None)
			#if (next(subl for subl in follow[key][1] if value in subl) != None):
			#temp = temp + [value]
		print "temp",temp	
		key = key + 1

def check_follow(follow,item,index): #check follow dict whether the non terminal is already added or not
	i = 1
	while(i<=len(follow)):
		if(item == follow[i][index]):
			return i
			break
		i = i + 1
	return 0
#def check_follow_terminal(terminals,)		
'''
	
	
if __name__ == "__main__":
	main()
	
