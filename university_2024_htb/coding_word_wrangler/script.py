import re
from collections import Counter

input_text = input()

def most_common_word(text):
    words = re.findall(r'\b\w+\b', text.lower())
    
    word_counts = Counter(words)
    
    most_common = max(word_counts, key=word_counts.get)
    
    return most_common

print(most_common_word(input_text))
