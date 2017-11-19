'''
If type is a instruction 
If there is instruction_var then format string with the instruction var
then show the instruction and move to next,
Do not wait for input

If type is a text
then show text and wait for input
assign it to var

If type is text with options
then show options for quick selection in response
and then wait for selection

If type is conditions then process the conditions
If condition is true then show text and wait for input else next

If type is caculated variable then run formula and save output of formula in var

If type is list_var and true
then format instruction with instruction var and show it in range(list_length)
'''

from . import views

class Interpreter:
	def instruction(self,question,index):
		res = {}
		res['index']=index
		if 'instruction_var' in question.keys():
			res['text']=question['instruction']%tuple(question['instruction_var'])
		else:
			res['text']=question['instruction']
		return res
	
	def text(self,question,index):
		res = {}
		res['index'] = index
		if 'options' in question.keys():
			res['quick_replies']=[]
			for i in question['options']:
				res['quick_replies'].append({'payload':i,'title':i.capitalize(),'content_type':'text'})
		res['text']=question['text']
		res['var_name'] = question['var']
		return res
	
	def condition(self,question,index):
		res = {}
		res['index'] = int(index)-1
		# Evaluate conditions
		lst = []
		for i in question['conditions']:
			lst.append(all([views.eval_condition(j) for j in i]))
		bool = any(lst)
		if bool is False:
			return None
		else:
			res['text'] = question['text']
			res['var_name'] = question['var']
			return res

def sample_text_function(question,data):
	index = data.index(question)
	type = list(question.ke
	ys())[0]
	instance = Interpreter()
	res = []
	if type == "instruction":
		res.append(instance.instruction(question,str(index)))
		if index != len(data):
			res.append(instance.text(data[index+1],str(index+1)))
	elif type == "text":
		res.append(instance.text(question,str(index)))
	elif type == "conditions":
		cond = instance.condition(question,str(index))
		if cond is not None:
			res.append(cond)
		else:
			res.append(instance.instruction(data[index+1],str(index+1)))
	return res
		
		
		
	
	
	
		
	

