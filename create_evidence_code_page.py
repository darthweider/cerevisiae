
text = open('./evidence_codes.txt').readlines()
html_page = open('./codes.html', 'w')

contents = ''

header = '''<html>
	<head>
		<META http-equiv="Content-Style-Type" content="text/css">
		<link rel="stylesheet" type="text/css" href="style.css">
	</head>
<body>
	<h1>About the Yeast Interactome Database </h1>'''

contents = contents + header + '\n'



for line in text:
	if line == '\n':
		contents = contents + '<p>'
	else:
		contents = contents + '<br>' + line

html_page.write(contents)