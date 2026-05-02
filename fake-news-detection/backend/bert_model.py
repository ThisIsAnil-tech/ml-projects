import torch
from transformers import BertTokenizer, BertForSequenceClassification
from torch.utils.data import DataLoader, TensorDataset
from torch.optim import AdamW
import os

class BERTModel:
    def __init__(self, model_name='bert-base-uncased', device='cpu'):
        self.device = device
        self.tokenizer = BertTokenizer.from_pretrained(model_name)
        self.model = BertForSequenceClassification.from_pretrained(model_name, num_labels=2).to(device)

    def prepare_data(self, texts, labels=None, max_length=128):
        encodings = self.tokenizer(texts, truncation=True, padding=True, max_length=max_length, return_tensors='pt')
        if labels is not None:
            dataset = TensorDataset(encodings['input_ids'], encodings['attention_mask'], torch.tensor(labels))
            return dataset
        else:
            return encodings['input_ids'], encodings['attention_mask']

    def train(self, texts, labels, epochs=3, batch_size=16, lr=2e-5):
        dataset = self.prepare_data(texts, labels)
        loader = DataLoader(dataset, batch_size=batch_size, shuffle=True)
        
        optimizer = AdamW(self.model.parameters(), lr=lr)
        self.model.train()

        for epoch in range(epochs):
            total_loss = 0
            for batch in loader:
                input_ids, attention_mask, batch_labels = [b.to(self.device) for b in batch]
                
                optimizer.zero_grad()
                outputs = self.model(input_ids, attention_mask=attention_mask, labels=batch_labels)
                loss = outputs.loss
                loss.backward()
                optimizer.step()
                
                total_loss += loss.item()
            print(f"BERT Epoch {epoch+1}/{epochs}, Loss: {total_loss/len(loader):.4f}")

    def predict(self, texts):
        input_ids, attention_mask = self.prepare_data(texts)
        input_ids = input_ids.to(self.device)
        attention_mask = attention_mask.to(self.device)

        self.model.eval()
        with torch.no_grad():
            outputs = self.model(input_ids, attention_mask=attention_mask)
            logits = outputs.logits
            probs = torch.softmax(logits, dim=1)
            preds = torch.argmax(probs, dim=1)
        
        return preds.cpu().numpy(), probs.cpu().numpy()

    def save_model(self, save_dir):
        os.makedirs(save_dir, exist_ok=True)
        self.model.save_pretrained(save_dir)
        self.tokenizer.save_pretrained(save_dir)

    def load_model(self, save_dir):
        self.tokenizer = BertTokenizer.from_pretrained(save_dir)
        self.model = BertForSequenceClassification.from_pretrained(save_dir).to(self.device)
