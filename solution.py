class Agent(object):
    def __init__(self, phoneme_table, vocabulary) -> None:
        """
        Your agent initialization goes here. You can also add code but don't remove the existing code.
        """
        self.phoneme_table = phoneme_table
        self.vocabulary = vocabulary
        self.best_state = None

    def generate_candidates(self, text):
        candidates = [text]
        return candidates
    
    def asr_corrector(self, environment):
        """
        Your ASR corrector agent goes here. Environment object has following important members.
        - environment.init_state: Initial state of the environment. This is the text that needs to be corrected.
        - environment.compute_cost: A cost function that takes a text and returns a cost. E.g., environment.compute_cost("hello") -> 0.5

        Your agent must update environment.best_state with the corrected text discovered so far.
        """
        self.best_state = environment.init_state
        current_cost = environment.compute_cost(self.best_state)
        beam_width = 5

        beam = [(self.best_state, current_cost)]

        while True:
            new_beam = []
            for state, cost in beam:
                candidates = self.generate_candidates(state)
                for candidate in candidates:
                    candidate_cost = environment.compute_cost(candidate)
                    new_beam.append((candidate, candidate_cost))
                    if candidate_cost < current_cost:
                        self.best_state = candidate
                        current_cost = candidate_cost
            
            beam = sorted(new_beam, key=lambda x: x[1])[:beam_width]

            if not new_beam or min(new_beam, key=lambda x: x[1])[1] >= current_cost:
                break

        environment.best_state = self.best_state

