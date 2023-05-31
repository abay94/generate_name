import random
import pandas as pd
from collections import defaultdict

def read_names_from_file(file_path):
    with open(file_path, 'r') as file:
        names = file.read().splitlines()
    return names

def build_bigram_frequencies(names):
    bigram_counts = defaultdict(int)
    letter_counts = defaultdict(int)

    for name in names:
        name = f"^{name}$"
        for i in range(len(name) - 1):
            bigram = name[i:i+2]
            bigram_counts[bigram] += 1
            letter_counts[bigram[0]] += 1

    bigram_prob = {}
    for first_letter in letter_counts:
        bigram_prob[first_letter] = {}
        for second_letter in letter_counts:
            bigram = first_letter + second_letter
            bigram_prob[first_letter][second_letter] = bigram_counts[bigram] / letter_counts[first_letter]

    return bigram_prob

# Example usage
file_path = 'names.txt'  # Replace with your file path
names = read_names_from_file(file_path)
bigram_frequencies = build_bigram_frequencies(names)

# Create a DataFrame from the bigram probabilities
df = pd.DataFrame(bigram_frequencies).fillna(0)
df.index.name = 'First Letter'
df.columns.name = 'Second Letter'

# Display the DataFrame
print(df)


### need to generate name
def build_bigram_model(names):
    bigram_counts = defaultdict(int)
    initial_letters = set()

    for name in names:
        name = f"^{name}$"
        for i in range(len(name) - 1):
            bigram = name[i:i+2]
            bigram_counts[bigram] += 1

            if i == 0:
                initial_letters.add(bigram[0])

    bigram_prob = defaultdict(float)
    for bigram, count in bigram_counts.items():
        first_letter = bigram[0]
        bigram_prob[bigram] = count / sum(bigram_counts[other_bigram] for other_bigram in bigram_counts if other_bigram[0] == first_letter)

    return bigram_prob

def generate_name(bigram_prob):
    name = random.choice(list(bigram_prob.keys()))
    while name[-1] != '$':
        next_letter = generate_next_letter(bigram_prob, name[-1])
        name += next_letter
    return name[1:-1]

def generate_next_letter(bigram_prob, current_letter):
    possible_bigrams = [bigram for bigram in bigram_prob if bigram[0] == current_letter]
    probabilities = [bigram_prob[bigram] for bigram in possible_bigrams]
    next_bigram = random.choices(possible_bigrams, probabilities)[0]
    return next_bigram[1]
    
bigram_prob = build_bigram_model(names)
new_name = generate_name(bigram_prob)
print("Generated Name:", new_name)
