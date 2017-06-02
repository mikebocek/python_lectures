import random 

def split_line_to_digraphs(line):
    words = line.split()
    
    # Ignore strings with fewer than two words
    if len(words) < 2:
        return []
    
    digraphs = []
    
    current_word = words[0]
    for next_word in words[1:]:
        digraphs.append((current_word, next_word))
        current_word = next_word
        
    return digraphs

def convert_digraphs_to_dict(digraphs):
    words_with_frequencies = {}
    for first_word, second_word in digraphs:
        if first_word not in words_with_frequencies:
            words_with_frequencies[first_word] = {second_word: 1}
        elif second_word not in words_with_frequencies[first_word]:
            words_with_frequencies[first_word][second_word] = 1
        else:
            words_with_frequencies[first_word][second_word] += 1
    return words_with_frequencies 

def merge_and_sum_dictionaries(counts_1, counts_2):
    combined_counts = {} 
    
    # Copy contents of first dictionary to combined counts
    for word, count in counts_1.items():
        combined_counts[word] = count
    
    for word, count in counts_2.items():
        if word in combined_counts:
            combined_counts[word] += count
        else:
            combined_counts[word] = count
    return combined_counts

def merge_outer_dictionaries(old_words, new_words):
    merged_words = {}
    for word, counts_dict in old_words.items():
        merged_words[word] = counts_dict
    for word, counts_dict in new_words.items():
        if word in merged_words:
            merged_words[word] = merge_and_sum_dictionaries(merged_words[word], counts_dict)
        else:
            merged_words[word] = counts_dict
    return merged_words

def normalize_counts(count_dictionary):
    total = sum(count_dictionary.values())
    output_dict = {}
    for word, count in count_dictionary.items():
        output_dict[word] = count/total
    return output_dict

def word_counts_from_file(filename):
    with open(filename) as speech_file:
        word_counts = {}
        for line in speech_file:
            digraphs = split_line_to_digraphs(line)
            line_counts = convert_digraphs_to_dict(digraphs)
            word_counts = merge_outer_dictionaries(word_counts, line_counts)
        for word, counts in word_counts.items():
            word_counts[word] = normalize_counts(counts)
    return word_counts

def random_choice_from_frequency_dict(frequency_dict):
    probability_threshold = random.random()
    total_probability = 0
    for word, probability in frequency_dict.items():
        total_probability += probability
        if total_probability > probability_threshold:
            return word
    return word

def generate_sentence(word_dict, number_words):
    output_words = []
    unique_words = list(word_dict.keys())
    current_word = random.choice(unique_words)
    for i in range(number_words):
        output_words.append(current_word)
        current_word = random_choice_from_frequency_dict(word_dict[current_word])
    return " ".join(output_words)