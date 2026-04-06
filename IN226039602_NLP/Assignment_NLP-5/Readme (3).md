# 🚀 BERT Fine-Tuning for Named Entity Recognition (NER)

## 📌 Overview
This project demonstrates fine-tuning a transformer-based model (DistilBERT) for the task of Named Entity Recognition (NER). The model identifies entities such as **Person, Organization, Location**, etc., from text.

The implementation uses the Hugging Face Transformers ecosystem along with PyTorch.

---

## 🎯 Objective
- Understand how BERT works for token classification
- Perform fine-tuning on a real-world dataset
- Evaluate model performance using standard metrics
- Build an end-to-end NLP pipeline

---

## 📂 Dataset
- **Dataset Used:** CoNLL-2003 (via Hugging Face)
- Contains labeled tokens for NER tasks

Example:
```
John works at Google in California
```
Output:
```
John → PERSON
Google → ORGANIZATION
California → LOCATION
```

---

## ⚙️ Tech Stack
- Python
- PyTorch
- Hugging Face Transformers
- Datasets Library
- Evaluate (seqeval)

---

## 🔄 Pipeline
```
Raw Data → Tokenization → Label Alignment → Model Training → Evaluation → Prediction
```

---

## 🧠 Model Details
- Model: `distilbert-base-uncased`
- Task: Token Classification (NER)
- Optimizer: AdamW
- Training Epochs: 1

---

## 🛠️ Implementation Steps

### 1. Data Loading
- Loaded dataset using Hugging Face Datasets

### 2. Tokenization & Label Alignment
- Used tokenizer with `is_split_into_words=True`
- Handled subword tokens using `-100` masking

### 3. Model Building
- Used `AutoModelForTokenClassification`
- Configured with custom label set

### 4. Training
- Used Hugging Face `Trainer`
- Small subset used for faster training

### 5. Evaluation
- Metrics used:
  - Precision
  - Recall
  - F1 Score

---

## 📊 Results
- Training Loss: ~0.19
- Model successfully identifies entities in text

---

## 🧪 Sample Prediction
```
Input: John works at Google in California

Output:
John → LABEL_3 (Person)
Google → LABEL_1 (Organization)
California → LABEL_5 (Location)
```

---

## 🚀 How to Run

1. Clone the repository:
```
git clone https://github.com/Soham10Patil/Data-Science-Internship-February-2026
```

2. Install dependencies:
```
pip install transformers datasets evaluate seqeval torch
```

3. Run the notebook:
- Open Jupyter Notebook / VS Code
- Execute all cells

---

## 📈 Key Learnings
- Understanding of transformer-based architectures
- Practical experience with fine-tuning BERT
- Handling token classification tasks
- Working with real NLP datasets

---

## 🔮 Future Improvements
- Train on full dataset (not subset)
- Increase epochs for better performance
- Try BERT / RoBERTa
- Implement early stopping
- Deploy as API using FastAPI

---

## 🤝 Connect with Me
If you found this useful, feel free to connect on LinkedIn and explore more projects!

---

⭐ If you like this project, give it a star on GitHub!

