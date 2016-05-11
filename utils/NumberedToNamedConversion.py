import sys, io, re, os

lvlNumPattern = re.compile('[0-9][0-9][0-9][0-9].lvl')

def IsMatchingLvlFile(_path, _fileName):
	return lvlNumPattern.match(_fileName) and os.path.isfile(os.path.join(_path, _fileName))

def GetLvlNumber(_fileName):
	return _fileName[:4]

def GetLvlName(_path, _fileName):
	fileName = os.path.join(_path, _fileName)
	with io.open(_fileName, 'rb') as file:
		fileData = file.read()
		if fileData[0] == '\x00':
			return fileData[0x07E0:0x0800].strip()
		elif fileData[0] < '\x04':
			return fileData[0x0040:0x0060].strip()
		elif fileData[0] == '\x04':
			return fileData[0x0050:0x0070].strip()
	return None

def FindLevelFilesToConvert(_path):
	toConvert=[]
	for fileName in os.listdir(_path):
		if IsMatchingLvlFile(_path, fileName):
			name = SanitiseName(GetLvlName(_path, fileName))
			if name is not None:
				number = GetLvlNumber(fileName)
				toConvert.append((fileName, name, number))
	
	return sorted(toConvert, key=lambda x: int(x[2]))

def SanitiseName(_name):
	if _name is not None:
		validChars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_ '
		newName = ''.join(c for c in _name if c in validChars)
		if len(newName) > 0:
			return newName
	return None

def RenameLevelsInFolder(_path):
	print('Searching in path: ' + _path + '\n')
	if os.path.isdir(_path):
		with io.open(os.path.join(_path,'levels.ini'), 'wb') as file:
			for oldFileName, levelName, number in FindLevelFilesToConvert(_path):
				fullOldName = os.path.join(_path, oldFileName)
				fullNewName = os.path.join(_path, levelName + '.lvl') 
				os.rename(fullOldName, fullNewName)
				file.write(number + '=' + levelName + '.lvl\n')
				print('Renamed: ' + oldFileName + ' To: ' + levelName + '\n')
		print('All done :)\n')
	else:
		print('Path not found: ' + _path+ '\n')

if len(sys.argv) == 2:
	RenameLevelsInFolder(os.path.join(os.getcwd(),sys.argv[1]))
else:
	RenameLevelsInFolder(os.getcwd())
