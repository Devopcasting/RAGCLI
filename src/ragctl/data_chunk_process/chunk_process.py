import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

# Ensure the necessary NLTK data is downloaded. Once it is downloaded don't try to download again
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt', quiet=True)
try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords', quiet=True)

class DataChunkProcess:
    def __init__(self, data_chunk) -> None:
        self.data_chunk = data_chunk
    
    def process(self) -> dict:
        # Tokenize the text
        tokens = word_tokenize(self.data_chunk)

        # Remove stop words
        stop_words = set(stopwords.words('english'))
        filtered_tokens = [word for word in tokens if word.lower() not in stop_words]
        filtered_text = ' '.join(filtered_tokens)
        result = {
            "data_chunk": self.data_chunk,
            "filtered_text": filtered_text
        }
        return result