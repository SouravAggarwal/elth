from django.shortcuts import render
from django.contrib.staticfiles.storage import staticfiles_storage
from json import loads,dumps
from json.decoder import JSONDecodeError
from django.http import HttpResponse
from .funcs import sample_text_function
import os
from re import split

func_dict = {
	'sample-text-function':sample_text_function
}

vars = {}

def setVariable(formula, var_name):
	vars[var_name]=eval_condition(formula)

def eval_condition(statement):
	# See if any token is a preExisting variable
	# If yes then replace it in the condition by vars['variable_name']
	# then evaluate condition
	for i in split('[^a-zA-Z0-9_]+',statement):
		if i in vars.keys():
			statement = statement.replace(i,'vars["'+i+'"]')
	return (eval(statement))

def load_json(_path):
	try:
		file = open(_path)
	except FileNotFoundError:
	# If File not found
		return {'File_Res':'NotFound','data':''}
	data = file.read()
	try:
		return {'File_Res':'OK','data':loads(data)}
	except JSONDecodeError:
	# If File data is not JSON
		return {'File_Res':'NoJSON','data':''}
	# Unexpected Behavior
	return {'File_Res':'Unexpected','data':''}

def gen_func():
	data_json = load_json(staticfiles_storage.url("assignment_1_input_2.json"))
	func = func_dict[data_json['data']['function']]
	if data_json['File_Res'] == 'OK':
		return data_json['data']['questions'],func

data,func = gen_func()

def chatter(request):
	if request.method == 'POST':
		keys = list(request.POST.keys())
		for i in keys:
			if i not in ['csrfmiddlewaretoken','last_index']:
				vars[i]= request.POST.get(i)
		last_index = request.POST.getlist('last_index')[-1]
		response =func(data[int(last_index)+1],data)
		return render(request,'index.html',{'message':response})
	elif request.method == "GET":
		response = func(data[0],data)
		return render(request,'index.html',{'message':response})
	


