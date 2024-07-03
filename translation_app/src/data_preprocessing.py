import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk import pos_tag, SnowballStemmer, RegexpTokenizer
from snowballstemmer import stemmer

nltk.download('averaged_perceptron_tagger')
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')

srpske_stop_rijeci = [
    'i', 'u', 'za', 'je', 'su', 'sam', 'si', 'smo', 'ste', 'su', 'bi', 'će', 'ćemo', 'ćeš', 'ćete', 'hoću',
    'hoćeš', 'hoće', 'hoćemo', 'hoćete', 'moj', 'moja', 'moje', 'tvog', 'tvoja', 'tvoje', 'njegov', 'njegova',
    'njegovo', 'naš', 'naša', 'naše', 'vaš', 'vaša', 'vaše', 'svog', 'svoja', 'svoje', 'ovaj', 'ova', 'ovo',
    'ovde', 'ovamo', 'onde', 'otuda', 'odavde', 'svaki', 'svaka', 'svako', 'svi', 'sve', 'svih', 'svima', 'svega'
    # Dodajte više riječi po potrebi
]
def preprocess_text(text):
    tokens = word_tokenize(text.lower())
    tokens = [t for t in tokens if t.isalnum() or t in ['?', '!', '.', ',', ':', ';', '-', '(', ')', '"', "'"]]

    #stop_words = set(stopwords.words('english')) - {'i', 'me', 'you', 'he', 'she', 'we', 'they', 'who', 'what'}
    #tokens = [t for t in tokens if t not in stop_words]

    lemmatizer = WordNetLemmatizer()
    tokens = [lemmatizer.lemmatize(t) for t in tokens]

    tagged_tokens = pos_tag(tokens)

    pos_map = {
        'NN': 'NOUN',
        'VB': 'VERB',
        'NNS': 'NOUN',
        'VBP': 'VERB',
        'PRP': 'PRONOUN',
        'DT': 'DETERMINER',
        'IN': 'PREPOSITION',
        'RB': 'ADVERB',
        'JJ': 'ADJECTIVE',
        'WP': 'PRONOUN',
        '.': 'PUNCTUATION',
    }

    processed_tokens = [(word, pos_map.get(tag[:2], 'NOUN')) for word, tag in tagged_tokens]

    return processed_tokens

def preprocess_text_sr(text):
    tokens = word_tokenize(text.lower())

    # Filtrirajte tokene
    tokens = [t for t in tokens if t.isalnum() or t in ['?', '!', '.', ',', ':', ';', '-', '(', ')', '"', "'"]]

    # Uklonite stop riječi
    #tokens = [t for t in tokens if t not in srpske_stop_rijeci]

    # Stemizacija tokena
    stemmer_sr = stemmer('serbian')
    tokens = [stemmer_sr.stemWord(t) for t in tokens]

    # # Procesirani tokeni
    processed_tokens = [(word, 'NOUN') for word in tokens]  # Postavljamo sve na NOUN jer nema POS tagiranja za srpski

    return processed_tokens