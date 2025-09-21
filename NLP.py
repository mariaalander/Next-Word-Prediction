import regex as re
import os

cand_nbr = 5  # number of candidate words to suggest
all_words = []  # list to hold all words in the corpora

# Regular expression patterns
nonletter = r'[^\p{L}.;:?!]+'
sentence_boundaries = r'([.;:?!])\s+(\p{Lu})'
sentence_markup = r' </s>\n<s> \2'

def get_files(dir, suffix):
    files = []
    for file in os.listdir(dir):
        if file.endswith(suffix):
            files.append(file)
    return files

# Tokenize text into words
def tokenize(text):
    words = re.findall(r'\p{L}+', text)
    return words

# Remove non-letter characters
def clean(text):
  return re.sub(nonletter, ' ', text)

# Split text into sentences, mark sentence boundaries with <s> and </s>, lowercase everything
def segment_sentences(text):
    text = re.sub(sentence_boundaries, sentence_markup, text)
    text = '<s> ' + text + ' </s>'
    text = re.sub(r' +', ' ' , text)
    text = re.sub(r'[.;:?!]', '', text)
    return text.lower()

# Frequency calculations
def unigrams(words):
    frequency = {}
    for word in words:
        frequency[word] = frequency.get(word, 0) + 1
    return frequency


def bigrams(words):
    frequency_bigrams = {}
    for i in range(len(words) - 1):
        pair = (words[i], words[i + 1])
        frequency_bigrams[pair] = frequency_bigrams.get(pair, 0) + 1
    return frequency_bigrams


def trigrams(words):
    frequencies = {}
    for i in range(len(words) - 2):
        triple = tuple(words[i:i + 3])
        frequencies[triple] = frequencies.get(triple, 0) + 1
    return frequencies

#Process the corpus
corpora = get_files('corpora', '.txt')
for filename in corpora:
    with open(os.path.join('corpora', filename), encoding='utf8') as f:
        corpus = f.read()
        corpus_cleaned = clean(corpus)
        corpus = segment_sentences(corpus_cleaned)
        words = re.findall(r'[\p{L}\p{<>/}]+', corpus)
        all_words.extend(words)
        print(f"Processed {filename}, total words so far: {len(words)}")




print(f"Total words in corpora: {len(all_words)}")
#Compute frequencies
frequency_unigrams = unigrams(all_words)
frequency_bigrams = bigrams(all_words)
frequency_trigrams = trigrams(all_words)


#User input
current_input = input("Enter a sentence: ").lower()
tokens = current_input.split()


# Generate candidate next words
candidates = {}
for (w1, w2, w3), freq in frequency_trigrams.items():
    if w1 == tokens[-2] and w2 == tokens[-1]:
      candidates[w3] = freq

#Backoff to bigrams if empty
if not candidates and len(tokens) >= 1:
    w1 = tokens[-1]
    for (b1, b2), freq in frequency_bigrams.items():
        if b1 == w1:
            candidates[b2] = freq

# Backoff to unigrams if still empty
if not candidates:
    candidates = frequency_unigrams.copy()


# Sort candidates by frequency and alphabetically
sorted_candidates = sorted(
    candidates.items(),
    key=lambda tuple: (-tuple[1], tuple[0])
)


next_word_predictions = [word for word, _ in sorted_candidates[:cand_nbr]]
print("Next word predictions: ", next_word_predictions)