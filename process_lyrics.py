from stop_words import get_stop_words
from nltk.stem.porter import PorterStemmer

stop_words = get_stop_words('english')
# NOISE_WORDS = [
#     "a","an", "an'", "about","above","ain't","aint", "all","along","also","although","am","an","any","are","aren't", "away",
#     "as","at","ay", "back", "be","because","'cause","cause", "bit", "been","but","by","can", "can't", "cant","cannot","could","couldn't","come","comes","cuase", "chorus",
#     "did","didn't","do","does","doesn't","don't","dont", "em'","else", "e.g.","either","etc","etc.","even","ever","every",
#     "for","from","further","get","gets","give", "gives","going", "goin'", "goes", "go","gonna", "gotta", "got","had","hardly","has","hasn't","having","he",
#     "hence","her","here","hereby","herein","hereof","hereon","hereto","herewith","him",
#     "his","how","however","i","i'll", "ill", "im'","im", "i.e.","if","into","it","it's","its","just", "know", "ic", "lyricchecksum", "lyricid", "like","let", "make", "me","more","most",
#     "mr","my","near","nor","now","of", "ok","on", "one","onto","other","our","out","over","put", "really",
#     "said","same", "say","see", "she","should","shouldn't","since","so","some","such","take", "than","that","thats", "that's",
#     "the","their","them","then","there","thereby","therefore","therefrom","therein","tell",
#     "thereof","thereon","thereto","therewith","these","they","this","those","through", "thing","try",
#     "thus","to","too","under","until","till'", "unto","upon","us","very","viz","want", "was", "wasn't", "wanna", "whatcha", "way",
#     "we","went","were","what","when","where","whereby","wherein","whether","which","while", "will", "well", "wit",
#     "who","whom","whose","why","with","without","would","x", "you","your","you're", "youre", "y'all", "verse", "repeat", "chorus"
# ]

lyricisms = ["oh","ohh","ooh", "ah", "ahh", "yeah","yes", "u", "mmm", "uh", "hey", "la", "na", "yo", "ya", "yeh",
"woah","whoa", "huh", "woah", "yea", "doo", "de", "nah", "da", "ha", "ba", "wo", "wow", "woo", "ooo", "dee", "dum", "hmm"]

#profane = [insert profane words] excluded
profane = []

punct = '?!,.:";/()'

remove_words = stop_words + lyricisms #+ profane + NOISE_WORDS

instrumental = '<span style=padding1em>'


def preprocess_all(text):
    p_stemmer = PorterStemmer()
    table = str.maketrans(dict.fromkeys(punct))
    text = text.translate(table)
    text = text.replace('\n', ' ')
    if instrumental in text:
        text = 'Instrumental'
    for p in profane:
        text = text.replace(p, p[0].upper()+'word')
    resultwords  = [word for word in text.split(' ') if word.lower() not in remove_words]
    resultwords = [p_stemmer.stem(i) for i in resultwords]
    text = ' '.join(resultwords)
    return text

def preprocess_curses(text):
    text = text.replace('\n', ' ')
    text = text.replace('got', '')
    for p in profane:
        text = text.replace(p, p[0].upper()+'word')
    return text

def preprocess_text(text):
    profane = ['shit', 'fuck', 'nigga', 'pussy', 'bitch', 'dick']
    text = text.replace('\n', ' ')
    for p in profane:
        text = text.replace(p, '')
    return text
