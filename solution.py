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
        current_state = environment.init_state
        current_state_list = list(current_state)
        current_cost = environment.compute_cost(current_state)
        self.best_state = current_state

        improved = True

        # Continue until no improvement is found
        while improved:
            improved = False
            neighbors = []

            # Generate neighbors by modifying each character
            for i in range(len(current_state_list)):
                current_char = current_state_list[i]

                # Skip spaces or characters not in the phoneme table
                if current_char == ' ' or current_char not in self.inv_phoneme_table:
                    continue

                # Generate neighboring states by replacing the current character
                for corr_char in self.inv_phoneme_table[current_char]:
                    # Create a new state with the correction
                    new_state_list = current_state_list[:i] + [corr_char] + current_state_list[i+1:]
                    new_state_str = ''.join(new_state_list)
                    new_cost = environment.compute_cost(new_state_str)
                    # Collect all possible neighbors
                    neighbors.append((new_state_str, new_cost))

            # Find the best neighbor with the lowest cost
            if neighbors:
                best_neighbor = min(neighbors, key=lambda x: x[1])
                best_neighbor_state, best_neighbor_cost = best_neighbor
                best_neighbor_state_list = list(best_neighbor_state)

                # Move to the best neighbor if it improves the cost
                if best_neighbor_cost < current_cost:
                    current_state = best_neighbor_state
                    current_cost = best_neighbor_cost
                    current_state_list = best_neighbor_state_list
                    self.best_state = current_state
                    improved = True

        # word addition
        print(self.best_state, current_cost)
        for front in self.vocabulary + ['']:
            new_state = [front] + [' '] + current_state_list
            new_state_str = ''.join(new_state)
            new_cost = environment.compute_cost(new_state_str)
            if new_cost < current_cost:
                self.best_state = new_state_str
                current_cost = new_cost
                print(self.best_state, current_cost)

        current_state_list = list(self.best_state)

        print(self.best_state, current_cost)
        for back in self.vocabulary + ['']:
            new_state = current_state_list + [' '] + [back]
            new_state_str = ''.join(new_state)
            new_cost = environment.compute_cost(new_state_str)
            if new_cost < current_cost:
                self.best_state = new_state_str
                current_cost = new_cost
                print(self.best_state, current_cost)
        
        end_time = time.time()
        print()
        print(self.best_state, current_cost)
        print('Time taken:', end_time - start_time)

# class Agent(object):
#     def __init__(self, phoneme_table, vocabulary) -> None:
#         """
#         Your agent initialization goes here. You can also add code but don't remove the existing code.
#         """
#         self.phoneme_table = phoneme_table
#         self.vocabulary = vocabulary
        
#         self.inv_phoneme_table = {}
#         for phoneme, symbols in phoneme_table.items():
#             for symbol in symbols:
#                 if symbol not in self.inv_phoneme_table:
#                     self.inv_phoneme_table[symbol] = []
#                 self.inv_phoneme_table[symbol].append(phoneme)   
#         # need to keep updating this
#         self.best_state = None

#     def asr_corrector(self, environment):
#         """
#         Your ASR corrector agent goes here. Environment object has following important members.
#         - environment.init_state: Initial state of the environment. This is the text that needs to be corrected.
#         - environment.compute_cost: A cost function that takes a text and returns a cost. E.g., environment.compute_cost("hello") -> 0.5

#         Your agent must update environment.best_state with the corrected text discovered so far.
#         """
#         start_time = time.time()
#         curr_state = environment.init_state
#         curr_cost = environment.compute_cost(curr_state)
#         self.best_state = curr_state
#         best_state_list = list(self.best_state)

#         # char correction
#         for i in range(len(best_state_list)):
#             curr_char = best_state_list[i]
#             if (curr_char == ' '):
#                 continue
            
#             if curr_char not in self.inv_phoneme_table:
#                 continue
            
#             for corr_char in self.inv_phoneme_table[curr_char]:
#                 new_state = best_state_list[:i] + [corr_char] + best_state_list[i+1:]
#                 new_state_str = ''.join(new_state)
#                 new_cost = environment.compute_cost(new_state_str)
#                 if new_cost < curr_cost:
#                     self.best_state = new_state_str
#                     best_state_list = new_state
#                     curr_cost = new_cost


#         # word addition
#         print(self.best_state, curr_cost)
#         for front in self.vocabulary + ['']:
#             new_state = [front] + [' '] + best_state_list
#             new_state_str = ''.join(new_state)
#             new_cost = environment.compute_cost(new_state_str)
#             if new_cost < curr_cost:
#                 self.best_state = new_state_str
#                 curr_cost = new_cost
#                 print(self.best_state, curr_cost)

#         best_state_list = list(self.best_state)

#         print(self.best_state, curr_cost)
#         for back in self.vocabulary + ['']:
#             new_state = best_state_list + [' '] + [back]
#             new_state_str = ''.join(new_state)
#             new_cost = environment.compute_cost(new_state_str)
#             if new_cost < curr_cost:
#                 self.best_state = new_state_str
#                 curr_cost = new_cost
#                 print(self.best_state, curr_cost)
        
#         end_time = time.time()
#         print()
#         print(self.best_state, curr_cost)
#         print('Time taken:', end_time - start_time)
        
    # did not get enough benefit compared to the time taken
    
    # def greedy_word_correction_3(self, environment):
    #     start_time = time.time()
    #     curr_state = environment.init_state
    #     curr_cost = environment.compute_cost(curr_state)
    #     self.best_state = curr_state
    #     best_state_list = list(self.best_state)

    #     # char correction
    #     for i in range(len(best_state_list)):
    #         curr_char = best_state_list[i]
    #         if (curr_char == ' '):
    #             continue
            
    #         if curr_char not in self.inv_phoneme_table:
    #             continue
            
    #         for corr_char in self.inv_phoneme_table[curr_char]:
    #             new_state = best_state_list[:i] + [corr_char] + best_state_list[i+1:]
    #             new_state_str = ''.join(new_state)
    #             new_cost = environment.compute_cost(new_state_str)
    #             if new_cost < curr_cost:
    #                 self.best_state = new_state_str
    #                 best_state_list = new_state
    #                 curr_cost = new_cost


    #     # word addition
    #     print(self.best_state, curr_cost)
    #     for front in self.vocabulary + ['']:
    #         new_state = [front] + [' '] + best_state_list
    #         new_state_str = ''.join(new_state)
    #         new_cost = environment.compute_cost(new_state_str)
    #         if new_cost < curr_cost:
    #             self.best_state = new_state_str
    #             curr_cost = new_cost
    #             print(self.best_state, curr_cost)

    #     best_state_list_save = list(self.best_state)

    #     print(self.best_state, curr_cost)
    #     for back in self.vocabulary + ['']:
    #         new_state = best_state_list + [' '] + [back]
    #         new_state_str = ''.join(new_state)
    #         new_cost = environment.compute_cost(new_state_str)
    #         if new_cost < curr_cost:
    #             self.best_state = new_state_str
    #             curr_cost = new_cost
    #             print(self.best_state, curr_cost)

    #     # updating for rear word check
    #     best_state_list = best_state_list_save

    #     print(self.best_state, curr_cost)
    #     for back in self.vocabulary + ['']:
    #         new_state = best_state_list + [' '] + [back]
    #         new_state_str = ''.join(new_state)
    #         new_cost = environment.compute_cost(new_state_str)
    #         if new_cost < curr_cost:
    #             self.best_state = new_state_str
    #             curr_cost = new_cost
    #             print(self.best_state, curr_cost)
        
    #     end_time = time.time()
    #     print()
    #     print(self.best_state, curr_cost)
    #     print('Time taken:', end_time - start_time)