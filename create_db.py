import MySQLdb

import sys

conn = MySQLdb.connect (
	host = "localhost",
	user = "tg225",
	passwd = "39XJPT",
	db = "TG225_db")


c = conn.cursor()


c.execute(
	'DROP TABLE IF EXISTS scgenes, scint;'
	'CREATE TABLE scgenes ('
		'taxon CHAR(6) NOT NULL,'
		'entrezID CHAR(10) PRIMARY KEY NOT NULL,'
		'gene VARCHAR(10) NOT NULL,'
		'orf VARCHAR(10) NOT NULL,'
		'aliases TEXT(50000) NOT NULL,'
		'sgd VARCHAR(14) NOT NULL,'
		'chromosome VARCHAR(5) NOT NULL,' 
		'protein VARCHAR(10) NOT NULL,' 
		'description TEXT(500000) NOT NULL,' 
		'proteintype VARCHAR(30) NOT NULL ) ;' 
	'CREATE TABLE scint (' 
		'orfA VARCHAR(10),' 
		'orfB VARCHAR(10),' 
		'geneA VARCHAR(10),' 
		'geneB VARCHAR(10),' 
		'evidence TEXT(50000000) ) ;')
#c.close()
#c = conn.cursor()

#n is the number of fields expected
def data_from(path, n):
	return [l.strip().split('\t', n-1) for l in open(path)]

def clean(s):
	return s.strip()

for e in data_from('CervBinaryHQ.txt', 5):
	orfA = clean(e[0])
	orfB = clean(e[1])
	geneA = clean(e[2])
	geneB = clean(e[3])
	evidence = clean(e[4])
	c.execute('INSERT INTO scint VALUES("%s", "%s", "%s", "%s", "%s");'
		% ( orfA, orfB, geneA, geneB, evidence ))

for gene in data_from('Yeastgeneinfo.txt', 14):
	tax = clean(gene[0])
	entrez = clean(gene[1])
	gene = clean(gene[2])
	orf = clean(gene[3])
	aliases = clean(gene[4])
	chromosome = clean(gene[6])
	proteintype = clean(gene[9])

	prot, desc = '',''
	g8, g13 = clean(gene[8]), clean(gene[13])
	if len(g8) > len(g13):
		prot = g13
		desc = g8
	else:
		prot = g8
		desc = g13

	sgd = clean(gene[5]).lstrip('SGD:')

	c.execute('INSERT INTO scgenes VALUES("%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s");'
		% (tax, entrez, gene, orf, aliases, sgd, chromosome, prot, desc, proteintype) )