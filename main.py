from transformers import GPT2LMHeadModel, GPT2Tokenizer
from torch.optim import Adam
from torch.utils.data import DataLoader
import tqdm
import torch

def train(chatData, model, optim):

    epochs = 12

    for i in tqdm.tqdm(range(epochs)):
        for X, a in chatData:
            X = X.to(device)
            a = a.to(device)
            optim.zero_grad()
            loss = model(X, attention_mask=a, labels=X).loss
            loss.backward()
            optim.step()
        torch.save(model.state_dict(), "model_state.pt")
        print(infer("I'm feeling really overwhelmed with work and school. I don't know how to manage my time and it's causing me a lot of stress."))
        print(infer("I'm having trouble with my procrastination, what can I do to be more productive?"))
        print(infer("I'm having trouble making decisions and I'm constantly second-guessing myself. What should I do?"))


def infer(inp):
    inp = "<startofstring> " + inp + " <bot>: "
    inp = tokenizer.encode(inp, return_tensors="pt")
    inp = inp.to(device)
    output = model.generate(inp, max_length=100, num_return_sequences=1)
    output = tokenizer.decode(output[0])
    return output


device = "cuda" if torch.cuda.is_available() else "mps" if torch.backends.mps.is_available() else "cpu"

tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
tokenizer.add_special_tokens({"pad_token": "<pad>", 
                                "bos_token": "<startofstring>",
                                "eos_token": "<endofstring>"})
tokenizer.add_tokens(["<bot>:"])

model = GPT2LMHeadModel.from_pretrained("gpt2")
model.resize_token_embeddings(len(tokenizer))

model = model.to(device)

# print(tokenizer.decode(model.generate(**tokenizer("hey i was good at basketball but ",
#                          return_tensors="pt"))[0]))

chatData = ChatData("/content/psychology.json", tokenizer)
chatData =  DataLoader(chatData, batch_size=64)

model.train()

optim = Adam(model.parameters(), lr=1e-4)

print("training .... ")
train(chatData, model, optim)

print("infer from model : ")
while True:
  inp = input()
  print(infer(inp))
  