import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, TensorDataset
import numpy as np
import os

class CNNModel(nn.Module):
    def __init__(self, vocab_size, embedding_dim=100, num_filters=128, filter_sizes=[3, 4, 5], num_classes=2, dropout=0.5):
        super(CNNModel, self).__init__()
        self.embedding = nn.Embedding(vocab_size, embedding_dim)
        self.convs = nn.ModuleList([
            nn.Conv1d(in_channels=embedding_dim, out_channels=num_filters, kernel_size=fs)
            for fs in filter_sizes
        ])
        self.fc = nn.Linear(len(filter_sizes) * num_filters, num_classes)
        self.dropout = nn.Dropout(dropout)

    def forward(self, x):
        # x shape: (batch_size, seq_len)
        embedded = self.embedding(x).permute(0, 2, 1) # shape: (batch_size, embedding_dim, seq_len)
        
        conved = [torch.relu(conv(embedded)) for conv in self.convs]
        pooled = [torch.max_pool1d(conv, conv.shape[2]).squeeze(2) for conv in conved]
        
        cat = self.dropout(torch.cat(pooled, dim=1))
        return self.fc(cat)

class LSTMModel(nn.Module):
    def __init__(self, vocab_size, embedding_dim=100, hidden_dim=256, num_layers=2, num_classes=2, dropout=0.5):
        super(LSTMModel, self).__init__()
        self.embedding = nn.Embedding(vocab_size, embedding_dim)
        self.lstm = nn.LSTM(embedding_dim, hidden_dim, num_layers=num_layers, 
                            batch_first=True, dropout=dropout if num_layers > 1 else 0, bidirectional=True)
        self.fc = nn.Linear(hidden_dim * 2, num_classes)
        self.dropout = nn.Dropout(dropout)

    def forward(self, x):
        # x shape: (batch_size, seq_len)
        embedded = self.dropout(self.embedding(x))
        output, (hidden, cell) = self.lstm(embedded)
        # hidden shape: (num_layers * num_directions, batch, hidden_dim)
        hidden = self.dropout(torch.cat((hidden[-2,:,:], hidden[-1,:,:]), dim=1))
        return self.fc(hidden)

class DLTrainer:
    def __init__(self, vocab_size, device='cpu'):
        self.device = device
        self.cnn = CNNModel(vocab_size=vocab_size).to(device)
        self.lstm = LSTMModel(vocab_size=vocab_size).to(device)

    def train_model(self, model_name, X_train, y_train, epochs=5, batch_size=32, lr=0.001):
        if model_name == 'cnn':
            model = self.cnn
        elif model_name == 'lstm':
            model = self.lstm
        else:
            raise ValueError("Unknown model")

        optimizer = optim.Adam(model.parameters(), lr=lr)
        criterion = nn.CrossEntropyLoss()

        dataset = TensorDataset(torch.tensor(X_train, dtype=torch.long), torch.tensor(y_train, dtype=torch.long))
        loader = DataLoader(dataset, batch_size=batch_size, shuffle=True)

        model.train()
        for epoch in range(epochs):
            total_loss = 0
            for batch_X, batch_y in loader:
                batch_X, batch_y = batch_X.to(self.device), batch_y.to(self.device)
                optimizer.zero_grad()
                outputs = model(batch_X)
                loss = criterion(outputs, batch_y)
                loss.backward()
                optimizer.step()
                total_loss += loss.item()
            print(f"Epoch {epoch+1}/{epochs}, Loss: {total_loss/len(loader):.4f}")

    def predict(self, model_name, X):
        if model_name == 'cnn':
            model = self.cnn
        elif model_name == 'lstm':
            model = self.lstm
        else:
            raise ValueError("Unknown model")

        model.eval()
        with torch.no_grad():
            X_tensor = torch.tensor(X, dtype=torch.long).to(self.device)
            outputs = model(X_tensor)
            probs = torch.softmax(outputs, dim=1)
            preds = torch.argmax(probs, dim=1)
        return preds.cpu().numpy(), probs.cpu().numpy()

    def save_models(self, save_dir):
        os.makedirs(save_dir, exist_ok=True)
        torch.save(self.cnn.state_dict(), os.path.join(save_dir, 'cnn_model.pth'))
        torch.save(self.lstm.state_dict(), os.path.join(save_dir, 'lstm_model.pth'))

    def load_models(self, save_dir):
        self.cnn.load_state_dict(torch.load(os.path.join(save_dir, 'cnn_model.pth'), map_location=self.device))
        self.lstm.load_state_dict(torch.load(os.path.join(save_dir, 'lstm_model.pth'), map_location=self.device))
