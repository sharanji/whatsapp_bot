import random
import json
import sys

import torch

from chatbot.botfiles.model import NeuralNet
from chatbot.botfiles.nltk_utils import bag_of_words, tokenize
from pathlib import Path


device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

BASE_DIR = Path(__file__).resolve().parent

with open(BASE_DIR/'intents.json', 'r') as json_data:
    intents = json.load(json_data)

FILE = BASE_DIR/"data.pth"
data = torch.load(FILE)

input_size = data["input_size"]
hidden_size = data["hidden_size"]
output_size = data["output_size"]
all_words = data['all_words']
tags = data['tags']
model_state = data["model_state"]

model = NeuralNet(input_size, hidden_size, output_size).to(device)
model.load_state_dict(model_state)
model.eval()

bot_name = "jesbot"
# print("Let's chat! (type 'quit' to exit)")


def talk(sentence):
    # sentence = "do you use credit cards?"
    if sentence == "quit":
        return "Sorry .. I am can't able to understand"

    # if sentence in ['1','2','3']:
    #     return ['Thanks for your reponse']

    sentence = tokenize(sentence)
    X = bag_of_words(sentence, all_words)
    X = X.reshape(1, X.shape[0])
    X = torch.from_numpy(X).to(device)

    output = model(X)
    _, predicted = torch.max(output, dim=1)

    tag = tags[predicted.item()]

    probs = torch.softmax(output, dim=1)
    prob = probs[0][predicted.item()]
    if prob.item() > 0.6:
        for intent in intents['intents']:
            if tag == intent["tag"]:
                if intent['type'] != 'button':
                    response = random.choice(intent['responses'])
                else:
                    response = intent['responses'][0]
                return {
                    "intent":intent["tag"],
                    "response":response ,
                    "type" : intent['type']
                }
    else:
        return { "intent":'unknown',"response":"Your query has been forwarded to our customer care excecutive and will contact you soon","type":"text"}


# if __name__ == "__main__":
#     message = sys.argv[1]
#     print(talk(message))
