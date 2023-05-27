import wikipedia
import re, sys, datetime
import preprocessor

wikiurl = sys.argv[1]

page = wikipedia.page(wikiurl, auto_suggest=False)
title = re.sub ( "_", " ", wikiurl )
stringtoread=page.content
#print (stringtoread)
sentences = preprocessor.preprocess ( stringtoread )

date = datetime.datetime.now()

tokenstring="This is the Wikipedia article on " + title + " read by a text to speech voice on " + date.strftime("%B %d, %Y") + ". |\n"

    #TODO: need to further tokenize these based on parens (long parens only?), dashes (n and m), semicolons, quotes
for sen in sentences:
    tokenstring+=sen + "|\n"
    if (len(sen) > 360): print ("******ERROR: string over 360 characters: " + sen + "\n", file=sys.stderr )

tokenstring+="This concludes the Wikipedia article on " + title + "| This recording and the underlying text are licensed under the Creative Commons Attribution Share Alike 3 point 0 Unported License|except for copyrighted excerpts and quotations which are used on the basis of fair use." 

print ( tokenstring )
