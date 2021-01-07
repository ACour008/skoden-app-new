def _split(str):
	return str.split("\n\n");

def _addtags(list):
	return ["<p>%s</p>" % x for x in list]

def makehtml(str):
	ya = _addtags(_split(str))
	return ''.join(ya)

def slugify(str):
	li = map(lambda x: x.lower(), str.split())
	return "-".join(li)