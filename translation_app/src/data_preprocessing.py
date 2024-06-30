import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk import pos_tag

nltk.download('averaged_perceptron_tagger')
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')

def preprocess_text(text):
    tokens = word_tokenize(text.lower())
    tokens = [t for t in tokens if t.isalnum() or t in ['?', '!', '.', ',', ':', ';', '-', '(', ')', '"', "'"]]

    stop_words = set(stopwords.words('english')) - {'i', 'me', 'you', 'he', 'she', 'we', 'they', 'who', 'what'}
    tokens = [t for t in tokens if t not in stop_words]

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

