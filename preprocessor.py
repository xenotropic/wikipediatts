import sys, re, csv, os, roman
from unidecode import unidecode

nemo_on = True #often skip this for debugging because it is slow

from nemo_text_processing.text_normalization.normalize import Normalizer
normalizer = None
if nemo_on:
    normalizer = Normalizer(input_case='cased', lang='en' )

#TODO: handle long parentheticals

#Notes and lists that tend to appear at the end of an article and are not suitable for reading

def csv_to_dict(csv_file):
    csv_file_exp = os.path.expandvars(csv_file)
    with open(csv_file_exp, mode='r') as infile:
        reader = csv.reader(infile)
        mydict = {rows[0]:rows[1] for rows in reader}
    return mydict

replace_acronyms = csv_to_dict ("$BASEDIR/wikipedia-tts/pronounced_acronyms.csv") 
bulk_replace_dict = csv_to_dict ("$BASEDIR/wikipedia-tts/bulk_replace.csv") # long context-independent strings 

def do_headings (text):
    lines = text.splitlines()
    heading_pattern = r'^==[^=]+==$'
    subheading_pattern = r'^==='
    heading_counter = 1
    output = ""
    for line in lines:
        if re.match (heading_pattern, line):
            output = output + "==" + "[Announcing] Main heading " + str (heading_counter) + ", "  +  line[2:] + " [period] .\n "
            heading_counter += 1
        elif re.match (subheading_pattern, line):
            index = 0  # could be three or four depending on level
            while index < len(line) and line[index] == '=':
                index += 1
            output = output + line[:index] + "[Announcing] Subheading, "+ line[index:] + "[period] .\n "
        else: output = output + line + "\n"
    output = re.sub ("=[=]+", "", output)
    return output

def remove_boring_end(text):
    dictionary = {"== Books ==", "== Honors and awards ==" , "== Bibliography ==" , "== Speeches and works ==","== Primary sources ==","== External links ==","== References ==","== Notes and References ==","== See Also ==","== Honours ==","== Honors ==","== Gallery ==","== See also ==","== Further reading ==","== External links ==","== Works= ="}
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

# things that can be bulk replaced, don't require regex or other context
def bulk_replace (text):
    for key in bulk_replace_dict.keys():
        text = text.replace(key, bulk_replace_dict[key])
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
#    text = re.sub('==*', '.', text) # wikipedia headers
    text = text.replace("\n",".")
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
    if text in replace_acronyms: return replace_acronyms[text]
    return " ".join(text)  # the default is split with spaces so each letter spoken see https://stackoverflow.com/a/18221460/

def get_middle_comma (sentence):
    if len (sentence) ==0: return 0
    comma_indices = [i for i, char in enumerate(sentence) if char == ',']
    space_indices = [i for i, char in enumerate(sentence) if char == ' ']

    middle_index = len(sentence) // 2
    nearest_comma_index = None
    
    # Find the nearest comma that is not in the middle of a number
    for index in comma_indices:
        if not (index == 0 ) and not (index > ( len (sentence) - 2 )):
            if not sentence[index-1].isdigit() and not sentence[index+1].isdigit():
                if nearest_comma_index is None or abs(index - middle_index) < abs(nearest_comma_index - middle_index):
                    nearest_comma_index = index

    # If no valid comma is found, find the nearest space
    if nearest_comma_index is None:
        nearest_space_index = min(space_indices, key=lambda x: abs(x - middle_index))
        return nearest_space_index

    return nearest_comma_index


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
    if nemo_on:
        return  normalizer.normalize (text, verbose=False, punct_post_process=True)
    else:
        return  text

def spell_out_units ( matchobj ):
    text = matchobj.group(0)
    length_dict = {"km2": "square kilometers",
                   "mm2": "square millimeters",
                   "m2": "square meters",
                   "sq mi": "square miles",
                   "km": "kilometers",
                   "mm": "millimeters",
                   "cm": "centimeters",
                   "nm": "nanometers",
                   "ft": "feet",
                   "in)": "inches)", #  false positives without parens
                   "lbs": "pounds",
                   "lb": "pounds",
                   "kg": "kilograms",
                   "g": "grams",
                   "mi": "miles",
                   "m": "meters",
                   "oz": "ounces",
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

def circas ( matchobj ):
    text = matchobj.group(0)
    text = text.replace("c."," sirka ")
    return text

def clause_split ( matchobj ):
    text = matchobj.group(0)
    text = text.replace(",",".")
    return text

def make_ordinal(n):

    n = int(n)
    if 11 <= (n % 100) <= 13:
        suffix = 'th'
    else:
        suffix = ['th', 'st', 'nd', 'rd', 'th'][min(n % 10, 4)]
    return str(n) + suffix

def monarch_replace ( matchobj ):
    text = matchobj.group(0)
    if ( "Malcolm" in text ): return text;
    name = re.search ('[A-Z][a-z]+ ', text).group(0)
    roman_n = re.search ('[XIV][XIV]+', text).group(0)
    int_n = roman.fromRoman ( roman_n )
    ord_n = make_ordinal ( int_n )
    return name + "the " + ord_n

#since there will be a lot of these
def template_method ( matchobj ):
    text = matchobj.group(0)
    return text


def preprocess (text):
    text = remove_boring_end (text)
    text = re.sub('{.*?\}', '', text) #curly brace formatting
    text = do_headings (text)
    text = text.replace("\u2212","minus ")
    text = text.replace("\u2014","-")
    text = text.replace("{","")
    text = text.replace("}","")
    text = text.replace("–","-")
    text = text.replace("–","-")
    text = text.replace(" "," ")
    text = bulk_replace (text) 
    #print ( text, file=sys.stderr )
    text = re.sub(': ?[0-9]+-[0-9]+', '', text)  # Wikipedia pincites
    text = re.sub(':[ ]?[0-9]+', '', text)  # Wikipedia pincites
    text = unidecode (text)
    text = text.replace("degF"," degrees fahrenheit " )
    text = text.replace("degC"," degrees celsius ")  
    text = text.replace("--","-")
    text = text.replace("[[","")
    text = text.replace("]]","")
    text = re.sub(',[ ]?(from|as well as|during|so|and|or|because|such|including|but|that|whereas|where|when|with|whether|for example|rather|although|who|in which|which)', clause_split, text)
    text = re.sub('[( -]c[.] ?[0-9]+', circas, text)
    text = re.sub('\([bd][.] ?[0-9]+\)', birth_death_dates, text)
    text = re.sub('#[0-9][0-9]*', ordinal_replace, text)
    text = re.sub('\$[0-9.]* ?[bmtz]illion', money_replace, text)
    text = re.sub('[A-Z][a-z]+ [XIV][XIV]+', monarch_replace, text)
    text = re.sub('\([0-9][0-9]?[0-9]?[0-9]?[ADBC ]*[-][0-9][0-9]?[0-9]?[0-9]?[ADBC ]*\)', date_ranges, text) 
    text = re.sub('(\d)[-](\d)', r'\1 to \2' , text) #number ranges, maybe I don't need the method below
    text = re.sub('[,0-9]+[-][0-9,]+', number_ranges, text)
    text = re.sub('\(Coordinates:[^)]+\)', '', text)
    text = re.sub('\d+\s*\d*\s*(m|m2|km|km2|mm2|ft|in|lb|lbs|g|kg|ha|sq mi|cm|mm|nm|km|ft|in|yd|oz|%)\W', spell_out_units, text)
    text = re.sub('\d+\s*to \d+\s*(m|m2|km|km2|mm2|ft|in|lb|lbs|g|kg|ha|sq mi|cm|mm|nm|km|ft|in|yd|oz|%)\W', spell_out_units, text)
    text = text.replace("kilometers2","square kilometers") # not sure why above doesn't catch this, kluge
    text = text.replace("mm2","square millimeters") # seems safe? pretty unique string
    text = re.sub('[+]?\d\d?/\d+', fractions, text) 
    text = re.sub('[,0-9.]+', replace_decimal_points, text)
    sentences_in = gh_sentences (text) 
    sentences_out = []
    for sen in sentences_in:
        sen = re.sub ('[A-Z][A-Z]*', acronym_split, sen)
        sen = sen.replace("."," ") # this are going to be stuff like degrees, initials, etc at this point
        sen = sen.replace(":"," ") # colons and semicolons were already used to do sentence breaks 
        sen = sen.replace(";"," ") 
        sen = sen.replace("/"," ") 
        sen = sen.replace("+"," ") 
        sen = sen.replace("*"," ")
        sen = sen.replace("(",",") # tortoise seems to pause more for commas than parens
        sen = sen.replace(")",",")
        sen = sen.replace(",,",",")
        sen = sen.replace(" ,",", ")
        sen = sen.replace("[period]",".")
        sen = sen.replace(" .|",".|")
        sen = sen.strip()
        if ( len (sen) < 3 ): continue #these are stubs often just a period
        if ( len (sen) > 320 ):
            middleish_comma = get_middle_comma ( sen )
            sentences_out.append ( normalize_local ( sen[:middleish_comma] ) )
            sentences_out.append ( normalize_local ( sen[middleish_comma+1:] ) )
        else: sentences_out.append ( normalize_local  ( sen ) )
    
    return sentences_out
