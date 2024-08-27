import pickle
import json
import argparse
from tqdm import tqdm
from copy import deepcopy

import torch
from transformers import WhisperForConditionalGeneration, WhisperProcessor

if torch.cuda.is_available():
    DEVICE = 'cuda'
else:
    DEVICE = 'cpu'


class CostModel(object):
    def __init__(self) -> None:
        # Load Whisper model and processor
        self.__processor = WhisperProcessor.from_pretrained("openai/whisper-small.en")
        self.__model = WhisperForConditionalGeneration.from_pretrained("openai/whisper-small.en").to(DEVICE)
        self.__audio_inputs = None

    def set_audio(self, audio, sampling_rate):
        self.__audio_inputs = self.__processor(
            audio, sampling_rate=sampling_rate, return_tensors="pt"
        ).input_features.to(DEVICE)

    def get_loss(self, text):
        # Prepare the target text input IDs
        target = self.__processor(
            text=text, return_tensors="pt", padding=True
        ).input_ids.to(DEVICE)

        # Make sure to set the decoder input IDs
        with torch.no_grad():
            outputs = self.__model(input_features=self.__audio_inputs, labels=target)

        return outputs.loss.item()


class Environment(object):
    def __init__(self, init_state, cost_function, phoneme_table) -> None:
        self.init_state = init_state
        self.phoneme_table = deepcopy(phoneme_table)
        self.__cost_function = cost_function

    def compute_cost(self, text):
        try:
            cost = self.__cost_function(text)
        except:
            cost = 1e6
        return cost


def main():
    parser = argparse.ArgumentParser(description="Process the input file.")
    
    parser.add_argument(
        '--input_file', type=str, help='Input filename',
        default='data/data.pkl', required=False
    )
    parser.add_argument(
        '--output_file', type=str, help='Output filename',
        default='outputs.json', required=False
    )
    parser.add_argument(
        '--phoneme_file', type=str, help='Phoneme filename',
        default='data/phoneme_table.json', required=False
    )
    parser.add_argument(
        '--vocab_file', type=str, help='Vocabulary filename',
        default='data/vocabulary.json', required=False
    )

    args = parser.parse_args()

    with open(args.input_file, 'rb') as fp:
        data = pickle.load(fp)

    with open(args.phoneme_file, 'r') as fp:
        phoneme_table = json.load(fp)

    with open(args.vocab_file, 'r') as fp:
        vocabulary = json.load(fp)

    cost_model = CostModel()

    from solution import Agent
    agent = Agent(phoneme_table, vocabulary)

    corrected_texts = []
    for sample in tqdm(data):
        audio = sample['audio']['array']
        sr = sample['audio']['sampling_rate']
        text = sample['text']
        cost_model.set_audio(audio, sr)
        environment = Environment(text, cost_model.get_loss, phoneme_table)

        try:
            agent.asr_corrector(environment)
            pred = agent.best_state
        except:
            pred = None

        corrected_texts.append(pred)

    with open(args.output_file, 'w') as fp:
        json.dump(corrected_texts, fp, indent=2)

if __name__ == '__main__':
    main()
