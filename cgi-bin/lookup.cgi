#!/usr/bin/python
#-------------------------------------
print "Content-type: text/html"
print
#-------------------------------------
import MySQLdb
import sys
sys.stderr = sys.stdout
from cgi import escape, FieldStorage

import cgitb
cgitb.enable()
#cgitb.enable(display=0, logdir="lookup_cgi.log")




header ='''<!DOCTYPE html>
<head>
	<META http-equiv="Content-Style-Type" content="text/css">
	<link rel="stylesheet" type="text/css" href="../style.css">
</head>
<body>'''
print header


back = '<p><button onclick="window.location=\'../index.html\';">Search again</button>'


form = FieldStorage()
query = form.getfirst("query", '')

conn = MySQLdb.connect (
	host = "localhost",
	user = "tg225",
	passwd = "39XJPT",
	db = "TG225_db")
c = conn.cursor()
dc = conn.cursor(MySQLdb.cursors.DictCursor)


# returns the orf and gene name for an inputed gene
# supports query of yeast gene names, ORF names, and entrezIDs
# returns an empty tuple if no entry found
def find_identifiers (query) :
	clean_query = query.strip().upper().lstrip('SGD:')
	select_query = 'SELECT orf,gene,entrezID FROM scgenes WHERE UPPER (entrezID) = "%s" OR UPPER (orf) = "%s" OR UPPER (gene) = "%s" OR UPPER (sgd) = "%s";' % (clean_query, clean_query, clean_query, clean_query)
	c.execute(select_query)
	return c.fetchall()

qid = find_identifiers (query)

#query not found in scgenes
if qid == ():
	print '<h2>Error</h2>'
	print '<p><em>%s</em> was not found in our database.' % (query)
	print '<p>Please make sure this is a valid Entrez ID, gene name, or ORF name.'
	print '<p>See our <a href="about.html">help page</a> for more details.'
	print back

elif len(qid) > 1:		
	print '<h2>RESULTS</h2>'
	print '<p>The following matches were found for your query <em>%s</em> in the yeast genome.' % (query)
	for hit in qid:
		qorf, qgene, qentrez = hit
		print '<p><a href="lookup.cgi?query=%s">%s</a> (Entrez ID %s)' % (qentrez, qgene, qentrez)
	print '<p>Please select from the genes listed above,'
	print ' or specify your gene using another criteria, such as Entrez ID or ORF name.'
	print back

else:
	qorf, qgene, qentrez = qid[0]

	#hits is a list of orfs that interact with the query
	c.execute('SELECT orfB, evidence FROM scint WHERE orfA = "%s" OR geneA = "%s" ;' % (qorf, qgene))
	hits = frozenset (c.fetchall())
	c.execute('SELECT orfA, evidence FROM scint WHERE orfB = "%s" OR geneB = "%s" ;' % (qorf, qgene))
	hits2 = hits.union ( frozenset (c.fetchall()) )
	evidence_dict = {} 
	for hit in hits2:
		orf, evidence = hit
		evidence_dict[orf] = evidence


	print '<h1>RESULTS</h1>'

	#interactors not found in scint
	#hits is the empty set
	if hits2 == frozenset():
		print '<p>No interactors found for %s' % (query)
		print back

	else:
		# hit_data is a list of interactors of the query, with extensive information on each interactor
		# if an interactor present in the interaction db is not found in the gene information db,
		# the interactor is not included in the results 
		search_str = 'orf = "' + '" OR orf = "'.join(evidence_dict.keys()) + '"'
		dc.execute('SELECT * FROM scgenes WHERE %s ;' % (search_str))
		hit_data = dc.fetchall()

		print '<div class="main">'
		print '<p>You searched for %s.' % (query)
		if query != qgene:
			print 'This matches our record for %s.' % (qgene)

		print '<p>The following genes interact with your query.'
		print '<p>'
		for hit in hit_data:
			entrez = hit['entrezID']
			name = hit['gene']
			print '<a href="#%s"> %s</a>    ' % ( entrez, name )
		print '</div>'

		print '<h2>Interactor Details</h2>'
		for hit in hit_data:
			entrez = hit['entrezID']
			name = hit['gene']

			print '<div class="details">'
			print '<a id="%s"><h3>%s</h3></a> ' % ( entrez, name )
			print '<p><b>Alternative names</b> %s' % ( hit['aliases'] )
			print '<br><b>Entrez ID</b> %s ' % (entrez)
			print '[<a href="http://www.ncbi.nlm.nih.gov/gene/%s">NCBI entry</a>]' % ( entrez )
			print '<br><b>Taxon</b> %s ' % (hit['taxon'])
			print '<b>Chromosome</b> %s ' % ( hit['chromosome'] )
			print '<b>Type</b> %s' % ( hit['proteintype'] )
			print '<br>'
			if hit['protein'] != '-' and hit['protein'] != '':
				print hit['protein'] + '. '
			if hit['description'] != '-' and hit['description'] != '':
				print hit['description'] + '.'
			print '<br><b>Interaction evidence code</b> %s' % (evidence_dict[hit['orf']])
			print '[<a href="../codes.html">code definitions</a>]'
			print '<br><a href="lookup.cgi?query=%s">Search for interactors</a>' % ( entrez )
			print '</div>'
		print '<p>'
		print back


		print  '''<ul>
	<a href="../index.html">Home</a> | <a href="../about.html">About</a>
</ul>'''

print '</body>'