import random
import json
import sys

import torch

from chatbot.botfiles.model import NeuralNet
from chatbot.botfiles.nltk_utils import bag_of_words, tokenize

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

with open('chatbot/botfiles/intents.json', 'r') as json_data:
    intents = json.load(json_data)

FILE = "chatbot/botfiles/data.pth"
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
        return

    sentence = tokenize(sentence)
    X = bag_of_words(sentence, all_words)
    X = X.reshape(1, X.shape[0])
    X = torch.from_numpy(X).to(device)

    output = model(X)
    _, predicted = torch.max(output, dim=1)

    tag = tags[predicted.item()]

    probs = torch.softmax(output, dim=1)
    prob = probs[0][predicted.item()]
    if prob.item() > 0.7:
        for intent in intents['intents']:
            if tag == intent["tag"]:
                return f"{random.choice(intent['responses'])} and {prob.item()}"
    else:
        return "I do not understand..."


# if __name__ == "__main__":
#     message = sys.argv[1]
#     print(talk(message))
