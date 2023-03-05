import sys, re
from unidecode import unidecode

#from nemo_text_processing.text_normalization.normalize import Normalizer
#normalizer = Normalizer(input_case='cased', lang='en' )

#TODO: handle long parentheticals

#Notes and lists that tend to appear at the end of an article and are not suitable for reading

pronounced = ['NASA','POTUS','SCOTUS','FLOTUS','WASP','UNICEF','AIDS','FOREX','GIF'];
replace_acronyms = {
    "JPG": "jaypeg",
    "JPEG": "jaypeg",
    "HVAC": "H vack",
    "BBQ": "barbeque",
    "MSDOS" : "M S dos",
    "CD-ROM" : "C D rom",
    "AAA" : "triple a",
    "IEEE" : "I triple e",
    "NATO": "Nayto",
    "ASCII": "Askey",
    "COINTELPRO": "Co intel pro"
}

def remove_boring_end(text):
    dictionary = {"== Honors and awards ==" , "== Speeches and works ==","== Primary sources ==","== External links ==","== References ==","==Notes and References==","== See Also ==","== Honours ==","== Honors ==","== Gallery ==","== See also ==","== Further reading ==","== External links ==","== Works= ="}
    positions=[len(text)]
    for ending in dictionary:
        pos = text.find (ending)
        if ( pos != -1 ): positions.append ( pos ) #if found then add it
    first_pos = min (positions)
    return text[:first_pos]

# makes $1.2 billion into 1.2 billion dollars which TTS handles more gracefully

def money_replace(matchobj):
    moneystr = matchobj.group(0)[1:] # string slice off $
    return moneystr + " dollars "

# spell out common abbreviations
def abbrev_remove (text):
    dictionary = {"...":"-","Rt.Rev":"Right Reverend", "Sr.":"Senior", "Jr.":"junior","Mr.":"Mister", "St.":"Street","Mrs.":"Missus","Ms.":"Miz","Dr.":"Doctor","Prof.":"Professor","Capt.":"Captain", "Dr.":"Drive" ,  "Ave.":"Avenue" , "Blvd.":"Boulevard", "Gen.":"General", " km/h":" kilometers per hour", " kmh": " kilometers per hour", "±":"plus or minus", " km":" kilometers" }
    for key in dictionary.keys():
        text = text.replace(key, dictionary[key])
    return text

# This method from stack exchange https://stackoverflow.com/a/31505798/720763 CC-BY-SA-4.0

alphabets= "([A-Za-z])"
prefixes = "(Mr|St|Mrs|Ms|Dr|Prof|Capt)[.]"
suffixes = "(Inc|Ltd|Jr|Sr|Co)"
starters = "(Mr|Mrs|Ms|Dr|Prof|Capt|Cpt|Lt|He\s|She\s|It\s|They\s|Their\s|Our\s|We\s|But\s|However\s|That\s|This\s|Wherever)"
acronyms = "([A-Z][.][A-Z][.](?:[A-Z][.])?)"
websites = "[.](com|net|org|io|gov|edu|me)"
digits = "([0-9])"

def gh_sentences(text):
    text = " " + text + "  "
    text = re.sub('==*', '.', text) # wikipedia headers
    text = text.replace("\n"," ")
    text = text.replace("-"," ")
    text = re.sub(prefixes,"\\1<prd>",text)
    text = re.sub(websites,"<prd>\\1",text)
    text = re.sub(digits + "[.]" + digits,"\\1<prd>\\2",text)
    if "..." in text: text = text.replace("...","<prd><prd><prd>")
    if "Ph.D" in text: text = text.replace("Ph.D.","Ph<prd>D<prd>")
    text = re.sub("\s" + alphabets + "[.] "," \\1<prd> ",text)
    text = re.sub(acronyms+" "+starters,"\\1<stop> \\2",text)
    text = re.sub(alphabets + "[.]" + alphabets + "[.]" + alphabets + "[.]","\\1<prd>\\2<prd>\\3<prd>",text)
    text = re.sub(alphabets + "[.]" + alphabets + "[.]","\\1<prd>\\2<prd>",text)
    text = re.sub(" "+suffixes+"[.] "+starters," \\1<stop> \\2",text)
    text = re.sub(" "+suffixes+"[.]"," \\1<prd>",text)
    text = re.sub(" " + alphabets + "[.]"," \\1<prd>",text)
    if "”" in text: text = text.replace(".”","”.")
    if "\"" in text: text = text.replace(".\"","\".")
    if "!" in text: text = text.replace("!\"","\"!")
    if "?" in text: text = text.replace("?\"","\"?")
    text = text.replace(".",".<stop>")
    text = text.replace("?","?<stop>")
    text = text.replace("!","!<stop>")
    text = text.replace(": ",":<stop>")
    text = text.replace(";",";<stop>")
    text = text.replace("<prd>",".")
    sentences = text.split("<stop>")
    sentences = sentences[:-1]
    sentences = [s.strip() for s in sentences]
    return sentences

# Makes shorthand ordinals like "1st" into "first" which TTS reads more reliably
def ordinal_replace(matchobj):
    n = matchobj.group(0)[1:]
    n = int(n)
    if 11 <= (n % 100) <= 13:
        suffix = 'th'
    else:
        suffix = ['th', 'st', 'nd', 'rd', 'th'][min(n % 10, 4)]
    return str(n) + suffix

def acronym_split (matchobj):
    text = matchobj.group(0)  
    if text in pronounced: return text
    if text in replace_acronyms: return replace_acronyms[text]
    return " ".join(text)  # the default is split with spaces so each letter spoken see https://stackoverflow.com/a/18221460/

def get_middle_comma (text): # for sentences that are still over 390 chars after splitting
    commas = [ind for ind, ch in enumerate(text) if ch.lower() == ','];
    if commas == []: return text
    return commas [ len ( commas ) // 2 ]

def date_ranges (matchobj):
    text = matchobj.group(0)
    text = text.replace("(","from ")
    text = text.replace(")"," ")
    text = text.replace("-"," to ")
    text = text.replace("—"," to ")
    return text
   
def number_ranges (matchobj):
    text = matchobj.group(0)
    text = text.replace("-"," to ")
    text = text.replace("—"," to ")
    return text
    
#Taking out Nemo for now, it is slow, dependencies are difficult
def normalize_local ( text ):
#    return  normalizer.normalize (text, verbose=False, punct_post_process=True)
    return  text

def spell_out_units ( matchobj ):
    text = matchobj.group(0)
    length_dict = {"km2": "square kilometers",
                   "m2": "square meters",
                   "sq mi": "square miles",
                   "km": "kilometers",
                   "mm": "millimeters",
                   "cm": "centimeters",
                   "ft": "feet",
                   "in": "inches",
                   "lbs": "pounds",
                   "lb": "pounds",
                   "kg": "kilograms",
                   "mi": "miles",
                   "m": "meters",
                   "yd": "yards",
                   "%":" percent"
                   }
    for key, value in length_dict.items():
        if ( key in text):
            return text.replace(key, value) # don't want to do more than on to avoid metersmiles
    return text

def birth_death_dates ( matchobj ):
    text = matchobj.group(0)
    text = text.replace("b."," who was born in ")
    text = text.replace("d."," who died in ")
    text = text.replace(")","")
    text = text.replace("(","")
    return text

#since there will be a lot of these
def replace_decimal_points ( matchobj ):
    text = matchobj.group(0)
    text = re.sub(r'(\d)[.](\d)', r'\1 point \2', text)
    return text

#since there will be a lot of these
def fractions ( matchobj ):
    text = matchobj.group(0)
    text = text.replace("+"," and ")
    text = re.sub(r'1[/]2', r' one half ', text)    
    text = re.sub(r'(\d)[/]4', r'\1 quarters ', text)    
    text = re.sub(r'(\d)[/]8', r'\1 eighths ', text)    
    text = re.sub(r'(\d)[/]16', r'\1 sixtennths ', text)    
    text = re.sub(r'(\d)[/]32', r'\1 thirty seconds ', text)    
    text = re.sub(r'(\d)[/]64', r'\1 sixth fourths ', text)    
    return text

#since there will be a lot of these
def template_method ( matchobj ):
    text = matchobj.group(0)
    return text

def preprocess (text):
    text = remove_boring_end (text)
    text = text.replace("\u2212","minus ")
    text = text.replace("\u2014","-")
    text = unidecode (text)
    text = text.replace("degF"," degrees fahrenheit " )
    text = text.replace("degC"," degrees celsius ")  
    text = abbrev_remove (text) 
    text = text.replace("--","-")
    text = re.sub('\([bd][.] ?[0-9]+\)', birth_death_dates, text)
    text = re.sub('#[0-9][0-9]*', ordinal_replace, text)
    text = re.sub('\$[0-9.]* ?[bmtz]illion', money_replace, text)
    text = re.sub('\([0-9][0-9]?[0-9]?[0-9]?[ADBC ]*[-][0-9][0-9]?[0-9]?[0-9]?[ADBC ]*\)', date_ranges, text) 
    text = re.sub('(\d)[-](\d)', r'\1 to \2' , text) #number ranges, maybe I don't need the method below
    text = re.sub('[,0-9]+[-][0-9,]+', number_ranges, text)
    text = re.sub('\(Coordinates:[^)]+\)', '', text)
    text = re.sub('\d+\s*\d*\s*(m|m2|km|km2|ft|in|lb|lbs|kg|ha|sq mi|cm|mm|km|ft|in|yd|%)\W', spell_out_units, text)
    text = re.sub('\d+\s*to \d+\s*(m|m2|km|km2|ft|in|lb|lbs|kg|ha|sq mi|cm|mm|km|ft|in|yd|%)\W', spell_out_units, text)
    text = text.replace("kilometers2","square kilometers") # not sure why above doesn't catch this, kluge
    text = re.sub('[+]?\d\d?/\d+', fractions, text) 
    text = re.sub('[,0-9.]+', replace_decimal_points, text)
    sentences_in = gh_sentences (text) 
    sentences_out = []
    for sen in sentences_in:
        sen = re.sub ('[A-Z][A-Z]*', acronym_split, sen)
        sen = sen.replace("."," ") # this are going to be stuff like degrees, initials, etc at this point
        sen = sen.replace("/"," ") 
        if ( len (sen) < 2 ): continue #these are stubs often just a period
        if ( len (sen) > 390 ):
            middleish_comma = get_middle_comma ( sen )
            sentences_out.append ( normalize_local ( sen[:middleish_comma] ) )
            sentences_out.append ( normalize_local ( sen[middleish_comma+1:] ) )
        else: sentences_out.append ( normalize_local  ( sen ) )        
    return sentences_out
