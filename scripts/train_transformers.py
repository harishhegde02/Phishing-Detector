import pandas as pd
import torch
from torch.utils.data import Dataset
from transformers import DistilBertTokenizerFast, DistilBertForSequenceClassification, Trainer, TrainingArguments
from sklearn.metrics import f1_score, precision_score, recall_score
import numpy as np
import os

# Load data
train_df = pd.read_csv('data/processed/train.csv')
val_df = pd.read_csv('data/processed/val.csv')

labels = ['urgency', 'authority', 'fear', 'impersonation']

class SEDataset(Dataset):
    def __init__(self, texts, labels, tokenizer, max_len=128):
        self.texts = texts
        self.labels = labels
        self.tokenizer = tokenizer
        self.max_len = max_len

    def __len__(self):
        return len(self.texts)

    def __getitem__(self, idx):
        text = str(self.texts[idx])
        label = self.labels[idx]
        
        encoding = self.tokenizer.encode_plus(
            text,
            add_special_tokens=True,
            max_length=self.max_len,
            padding='max_length',
            return_token_type_ids=False,
            truncation=True,
            return_attention_mask=True,
            return_tensors='pt',
        )

        return {
            'input_ids': encoding['input_ids'].flatten(),
            'attention_mask': encoding['attention_mask'].flatten(),
            'labels': torch.tensor(label, dtype=torch.float)
        }

def multi_label_metrics(predictions, labels, threshold=0.5):
    # Apply sigmoid to get probabilities
    probs = 1 / (1 + np.exp(-predictions))
    y_pred = np.where(probs > threshold, 1, 0)
    y_true = labels
    
    f1 = f1_score(y_true, y_pred, average='macro')
    precision = precision_score(y_true, y_pred, average='macro', zero_division=0)
    recall = recall_score(y_true, y_pred, average='macro', zero_division=0)
    
    return {'f1': f1, 'precision': precision, 'recall': recall}

def compute_metrics(p):
    preds = p.predictions[0] if isinstance(p.predictions, tuple) else p.predictions
    result = multi_label_metrics(preds, p.label_ids)
    return result

# Initialize
tokenizer = DistilBertTokenizerFast.from_pretrained('distilbert-base-uncased')
model = DistilBertForSequenceClassification.from_pretrained(
    'distilbert-base-uncased', 
    num_labels=len(labels),
    problem_type="multi_label_classification"
)

train_dataset = SEDataset(
    train_df['cleaned_text'].to_list(),
    train_df[labels].values,
    tokenizer
)

val_dataset = SEDataset(
    val_df['cleaned_text'].to_list(),
    val_df[labels].values,
    tokenizer
)

training_args = TrainingArguments(
    output_dir='./results',
    num_train_epochs=3,
    per_device_train_batch_size=8,
    per_device_eval_batch_size=8,
    warmup_steps=100,
    weight_decay=0.01,
    logging_dir='./logs',
    logging_steps=10,
    evaluation_strategy="epoch",
    save_strategy="epoch",
    load_best_model_at_end=True,
)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
    eval_dataset=val_dataset,
    compute_metrics=compute_metrics
)

# Train
print("Starting fine-tuning...")
trainer.train()

# Save
model.save_pretrained('models/distilbert_se_detector')
tokenizer.save_pretrained('models/distilbert_se_detector')
print("Model and tokenizer saved to models/distilbert_se_detector")
