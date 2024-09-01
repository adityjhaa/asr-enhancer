import heapq

class Agent(object):
    def __init__(self, phoneme_table, vocabulary) -> None:
        """
        Your agent initialization goes here. You can also add code but don't remove the existing code.
        """
        self.phoneme_table = phoneme_table
        self.vocabulary = vocabulary
        
        self.inv_phoneme_table = {}
        for phoneme, symbols in phoneme_table.items():
            for symbol in symbols:
                if symbol not in self.inv_phoneme_table:
                    self.inv_phoneme_table[symbol] = []
                self.inv_phoneme_table[symbol].append(phoneme)   
        # need to keep updating this
        self.best_state = None

    def asr_corrector(self, environment):
        """
        Your ASR corrector agent goes here. Environment object has following important members.
        - environment.init_state: Initial state of the environment. This is the text that needs to be corrected.
        - environment.compute_cost: A cost function that takes a text and returns a cost. E.g., environment.compute_cost("hello") -> 0.5

        Your agent must update environment.best_state with the corrected text discovered so far.
        """
        self.best_state = environment.init_state # sentence to be corrected
        cost = environment.compute_cost(self.best_state)
        beam_width = 5  # Number of candidates to keep at each step
        
        beam = [(cost, self.best_state)]  # Each element is a tuple (current cost, current sentence as list of words)
        heapq.heapify(beam)  # Convert list to a heap
        
        for i in range(len(self.best_state)):
            new_beam = []
            while beam:
                _, sentence = heapq.heappop(beam)
                current_char = sentence[i]
                possible_corrections = self.inv_phoneme_table[current_char]

                for correction in possible_corrections:
                    new_sentence = sentence[:i] + [correction] + sentence[i+1:]
                    new_cost = environment.compute_cost(new_sentence)
                    heapq.heappush(new_beam, (new_cost, new_sentence))

            # Keep only the top beam_width candidates by using heapq
            beam = heapq.nsmallest(beam_width, new_beam)
            heapq.heapify(beam)  # Convert list to a heap

        # The sentence with the lowest cost
        best_cost, best_sentence = beam[0]
        self.best_state = best_sentence
