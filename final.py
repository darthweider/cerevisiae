import MySQLdb

scdb = MySQLdb.connect (
	host = "localhost",
	user = "tg225",
	passwd = "39XJPT",
	db = "TG225_db")


c = scdb.cursor()

c.execute('CREATE TABLE scgenes (' +
		'taxon CHAR(6),' +
		'entrezID CHAR(10) PRIMARY KEY NOT NULL,' +
		'nameRead VARCHAR(10),' +
		'orf VARCHAR(10),' +
		'aliases TEXT(50000),' +
		'sgd VARCHAR(14),' +
		'chromosome VARCHAR(5),' +
		'protein VARCHAR(10),' +
		'description TEXT(500000),' +
		'proteintype VARCHAR(30)' +
		') ;')

c.execute('create table scint (' +
		'orfA VARCHAR(10),' +
		'orfB VARCHAR(10),' +
		'geneA VARCHAR(10),' +
		'geneB VARCHAR(10),' +
		'proof TEXT(50000000)' +
		') ;')

#n is the number of fields expected
def data_from(path, n):
	return [l.strip().split('\t', n-1) for l in open('path')]


for e in data_from('CervBinaryHQ.txt', 5):
	c.execute('INSERT INTO scint VALUES("%s", "%s", "%s", "%s", "%s");'
		% (e[0], e[1], e[2]. e[3], e[4]) )


#consider cleaning all - values into NULL
for gene in data_from('Yeastgeneinfo.txt', 14):
	prot, desc = '',''
	if len(gene[8]) > len(gene[13]):
		prot = gene[13]
		desc = gene[8]
	else:
		prott = gene[8]
		desc = gene[13]

	c.execute('INSERT INTO scgenes VALUES("%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s");'
		% (gene[0], gene[1], gene[2], gene[3], gene[4], gene[5], gene[6], prot, desc, gene[9]) )