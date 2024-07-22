# does not work.
# alpha has no rsync, Can you believe that?


michel_pub.html: /mount/aux_papa/vdbergh/TEX/LATEXMACROS/papers.bib
	genbib -h > michel_pub.html

view:
	konqueror michel_pub.html


put: michel_pub.html 
	scp -r * lucg5281@alpha.luc.ac.be:/usr/local/etc/httpd/htdocs/Research/Algebra/Publications 


sync: get put

