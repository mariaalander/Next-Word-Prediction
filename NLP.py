import regex as re

cand_nbr = 5  # number of candidate words to suggest

corpus = open('PrideAndPrejudice.txt', encoding='utf8').read()


# Regular expression patterns
nonletter = r'[^\p{L}.;:?!]+'
sentence_boundaries = r'([.;:?!])\s+(\p{Lu})'
sentence_markup = r' </s>\n<s> \2'



# Tokenize text into words (sequences of letters)
def tokenize(text):
    words = re.findall(r'\p{L}+', text)
    return words

# Remove non-letter characters, except for sentence boundary punctuation
def clean(text):
  return re.sub(nonletter, ' ', text)

# Split text into sentences, mark sentence boundaries with <s> and </s>, lowercase everything
def segment_sentences(text):
    text = re.sub(sentence_boundaries, sentence_markup, text)
    text = '<s> ' + text + ' </s>'
    text = re.sub(r' +', ' ' , text)
    text = re.sub(r'[.;:?!]', '', text)
    return text.lower()



corpus_cleaned = clean(corpus)
corpus = segment_sentences(corpus_cleaned)

words = re.findall(r'[\p{L}\p{<>/}]+', corpus)



def unigrams(words):
    frequency = {}
    for i in range(len(words)):
        if words[i] in frequency:
            frequency[words[i]] += 1
        else:
            frequency[words[i]] = 1
    return frequency

frequency = unigrams(words)

def bigrams(words):
    bigrams = []
    for i in range(len(words) - 1):
        bigrams.append((words[i], words[i + 1]))
    frequency_bigrams = {}
    for i in range(len(words) - 1):
        if bigrams[i] in frequency_bigrams:
            frequency_bigrams[bigrams[i]] += 1
        else:
            frequency_bigrams[bigrams[i]] = 1
    return frequency_bigrams

frequency_bigrams = bigrams(words)


def trigrams(words):
    trigrams = [tuple(words[idx:idx + 3]) for idx in range(len(words) - 2)]
   
    frequencies = {}
    for ngram in trigrams:
        if ngram in frequencies:
            frequencies[ngram] += 1
        else:
            frequencies[ngram] = 1
    return frequencies

frequency_trigrams = trigrams(words)

current_input = input("Enter a sentence: ").lower()
tokens = current_input.split()


frequency_trigrams = trigrams(words)
candidates = {}

for (w1, w2, w3), freq in frequency_trigrams.items():
    if w1 == tokens[-2] and w2 == tokens[-1]:
      candidates[w3] = freq

sorted_candidates = sorted(
    candidates.items(),
    key=lambda tuple: (-tuple[1], tuple[0])
)
next_word_predictions = [word for word, _ in sorted_candidates[:cand_nbr]]

print("Next word predictions: ", next_word_predictions)