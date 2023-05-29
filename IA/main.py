from transformers import GPT2LMHeadModel, GPT2Tokenizer
from torch.optim import Adam
from torch.utils.data import DataLoader
import tqdm
import torch

def train(chatData, model, optim):

    epochs = 30

    for i in tqdm.tqdm(range(epochs)):
        for X, a in chatData:
            X = X.to(device)
            a = a.to(device)
            optim.zero_grad()
            loss = model(X, attention_mask=a, labels=X).loss
            loss.backward()
            optim.step()
        torch.save(model.state_dict(), "/content/drive/MyDrive/IA/model_state/model_state2.pt")
        model.config.save_pretrained("/content/drive/MyDrive/IA/model_config/")
        tokenizer.save_pretrained("/content/drive/MyDrive/IA/tokenizer_info/")
        print(infer("I've been feeling really anxious lately, and I don't know why."))
        print(infer("Give three tips for staying healthy."))
        print(infer("Write a short story in third person narration about a protagonist who has to make an important career decision."))
        print(infer("I feel so lonely in my life i dont have anyone to talk."))


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

chatData = ChatData("/content/drive/MyDrive/IA/FullDB1.json", tokenizer)
chatData =  DataLoader(chatData, batch_size=256)

model.train()

optim = Adam(model.parameters(), lr=1e-5)

print("training .... ")
train(chatData, model, optim)

print("infer from model : ")
while True:
  inp = input()
  print(infer(inp))
  
