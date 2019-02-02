# coding=utf-8
import sys
import inspect

def getFrameArgs(frame):
	arginfo = inspect.getargvalues(frame)

	try:
		if not arginfo.args:
			return '', None
	except AttributeError:
		return '', None

	if arginfo.args[0] == 'self':
		self = arginfo.locals['self']
		classname = self.__class__.__name__

		arginfo.args.pop(0)
		del arginfo.locals['self']
	else:
		classname = None

	args = inspect.formatargvalues(*arginfo)

	return args, classname


#WARNING! Dont use inspect.stack()! its very very very slow.
def getFrames(deep=2):
	if deep is None or deep == 0:
		deep=1
	frames = []
	for x in range(2,3+deep):
		try:
			frames.append(sys._getframe(x))
		except:
			break
	return frames

#printCallSequence(5)
#14:13:01.164 /usr/lib/enigma2/python/Components/TimerSanityCheck.py:9 __init__(Navigation.py:46) --> __init__(RecordTimer.py:958) --> loadTimer(RecordTimer.py:1048) --> record(RecordTimer.py:1184) --> __init__
#printCallSequence(-5)
#14:13:01.166 /usr/lib/enigma2/python/Components/TimerSanityCheck.py:20 check <-- record(RecordTimer.py:1185) <-- loadTimer(RecordTimer.py:1048) <-- __init__(RecordTimer.py:958) <-- __init__(Navigation.py:46)
def printCallSequence(deep=1):
	if deep is None or deep == 0:
		deep=1
	frames = getFrames(abs(deep))
	if deep >= 0:
		for x in range(0,len(frames)):
			args, classname = getFrameArgs(frames[x])
			if not x:
				print "\033[96m%s%s%s\033[36m<%s:%s>\033[0m\n" %(frames[x].f_code.co_name, args, classname, frames[0].f_code.co_filename.split("/")[-1], frames[0].f_code.co_firstlineno),	## das überwachte Objekt
			else:
				print "%s|\n%s+--\033[95m%s%s\033[35m<%s:%s>\033[0m\n" %("   "*(x-1), "   "*(x-1), frames[x].f_code.co_name, args, frames[x].f_code.co_filename.split("/")[-1], frames[x].f_lineno),	## die Aufrufer
	else:
		for x in range(len(frames)-1,-1,-1):
			args, classname = getFrameArgs(frames[x])
			if not x:
				print "\033[96m%s%s" %(frames[x].f_code.co_name, args),
				print "\033[0m",
			else:
				print "\033[95m%s%s<%s:%s> \033[94m-->" %(frames[x].f_code.co_name, args, frames[x].f_code.co_filename.split("/")[-1], frames[x].f_lineno),
				print "\033[0m",
	print "\033[0m"
	del frames

def printCallSequenceRawData(deep=1):
	if deep is None or deep == 0:
		deep=1
	deep = abs(deep)
	frames = getFrames(deep)
	print "\033[36m%s:%s" %(frames[0].f_code.co_filename, frames[0].f_code.co_firstlineno),
	for x in range(0,len(frames)):
		if not x:
			print "\033[96m%s \033[33m%s" %(frames[x].f_code.co_name, inspect.getargvalues(frames[x]))
		else:
			print "\033[94m<-- \033[95m%s<%s:%s>\033[33m%s" %(frames[x].f_code.co_name, frames[x].f_code.co_filename.split("/")[-1], frames[x].f_lineno, inspect.getargvalues(frames[x]))
	print "\033[0m",
	del frames
