import MySQLdb
import sys

query = (sys.argv[1]).strip()

scdb = MySQLdb.connect (
	host = "localhost",
	user = "tg225",
	passwd = "39XJPT",
	db = "TG225_db")


c = scdb.cursor()

#support yest gene names, ORF names, and entrezIDs

c.execute('SELECT orf,gene FROM scgenes WHERE entrezID = %s OR orf = %s OR gene = %s ;' % (query, query, query))

result = c.fetchall()

if result == []:
	raise KeyError('The query could not be found in our yeast database.')

qorf, qgene = result[0][0], result[0][1]

#hits is a list of orfs that interact with the query
c.execute('SELECT orfB FROM scint WHERE orfA = %s OR geneA = %s ;' % (qorf, qgene))

hits = c.fetchall()

c.execute('SELECT orfA FROM scint WHERE orfB = %s OR geneB = %s ;' % (qorf, qgene))

hits = hits + c.fetchall()

#=============IF NO HITS RETURN
if hits = []:
	

#hit_data is a list of interactors of the query, with extensive information on each interactor
search_str = 'orf = ' + " OR orf = ".join(hits)
print search_str

c.execute('SELECT * FROM scgenes WHERE %s ;' % (search_str))
hit_data = c.fetchall()

