import time

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
        start_time = time.time()
        curr_state = environment.init_state
        curr_cost = environment.compute_cost(curr_state)
        self.best_state = curr_state
        best_state_list = list(self.best_state)
                
        for i in range(len(best_state_list)):
            curr_char = best_state_list[i]
            if (curr_char == ' '):
                continue
            
            if curr_char not in self.inv_phoneme_table:
                continue
            
            for corr_char in self.inv_phoneme_table[curr_char]:
                new_state = best_state_list[:i] + [corr_char] + best_state_list[i+1:]
                new_state_str = ''.join(new_state)
                new_cost = environment.compute_cost(new_state_str)
                if new_cost < curr_cost:
                    self.best_state = new_state_str
                    best_state_list = new_state
                    curr_cost = new_cost

        end_time = time.time()
        print()
        print(self.best_state, curr_cost)
        print('Time taken:', end_time - start_time)