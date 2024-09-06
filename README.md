# ASR Enhancer
## Correction Agent for ASR Errors in Voice-Enabled Assistants

<hr>

### Introduction
The **Agent** class implements a corrective algorithm aimed at enhancing the output of **Automatic Speech Recognition** (ASR) systems. The algorithm's primary goal is to refine an initial text state to achieve a lower cost, which signifies better alignment with the desired output. The approach integrates both character-level corrections and word-level adjustments based on a phoneme table and vocabulary.

### Algorithm Overview
The core idea is based on the hill climbing algorithm. Here’s a brief overview:

1. **State Definition:**<br>
A state is defined as the current best sentence produced by the algorithm.

2. **Neighbor Generation:**<br>
For each character in the sentence, the algorithm checks for its existence in the inverse phoneme table (a mapping from erroneous phonemes to their corrections). If the character or bigram exists in the table, it is replaced with its corrected representation. This process generates a tuple (state, cost) for each modification.   

3. **Selection of Best Neighbor:**<br>
Among the generated neighbors, the one with the lowest cost is selected, and the process is repeated.

### Attempted Algorithms

1. **Greedy Algorithm without Word Correction:**<br>
This initial approach involved iteratively updating each character from left to right by replacing it with the lowest-cost neighbor without considering other characters in the sentence.
    - Average Loss: 2.1136
    - Average Time per Sentence: 13 seconds


2. **Hill Climbing without Word Correction:**<br>
This method utilized hill climbing by considering all characters in the sentence before making updates. Note that bigrams were not checked in this approach.
    - Average Loss: 2.0243
    - Average Time per Sentence: 50 seconds


3. **Greedy Algorithm with Word Updates Before Character Correction:**<br>
Here, the first and last missing words were added in an O(n²) fashion, which proved to be time-consuming and yielded minimal improvement. Instead, adding words in two separate loops (one for the beginning and one for the end) was found to be more effective.
    - Average Loss: 1.8454
    - Average Time per Sentence: 25 seconds


4. **Greedy Algorithm with Word Updates After Character Correction:**<br>
Adding words after character correction was found to significantly reduce the loss compared to adding words before correction. This suggests that some added words were being incorrectly modified by the character correction algorithm.
    - Average Loss: 1.8058
    - Average Time per Sentence: 25 seconds


5. **Hill Climbing with Word Updates After Character Correction:**<br>
Combining hill climbing with word updates after character correction resulted in improved performance. Note that bigrams were not checked in this implementation.
    - Average Loss: 1.7099
    - Average Time per Sentence: 55 seconds


6. **Word Updates After Hill Climbing with Unigrams and Bigrams Correction:**<br>
Incorporating bigram checks into the algorithm addressed previously missed bigrams (e.g., ‘SH’) and further improved the correction process.
    - Average Loss: 1.5158
    - Average Time per Sentence: 60 seconds


