import logging
from transformers import pipeline, AutoTokenizer, AutoModelForSequenceClassification

# Load the tokenizer and model
tokenizer = AutoTokenizer.from_pretrained("roberta-large-mnli") # Reason for choosing roberta-large-mnli is ease to deployment and fast response for demonstration purpose
model = AutoModelForSequenceClassification.from_pretrained("roberta-large-mnli") # Can be replaced with better text-classifcation models or a well-fine-tuned model

# Create the pipeline using zero-shot classification
classifier = pipeline("zero-shot-classification", model=model, tokenizer=tokenizer)

# Define O-1A criteria
O_1A_CRITERIA = [
    "Awards",
    "Membership",
    "Press",
    "Judging",
    "Original contribution",
    "Scholarly articles",
    "Critical employment",
    "High remuneration"
]

def chunk_text(text, chunk_size=512):
    """
    Split text into smaller chunks of the specified size.
    """
    tokens = text.split()
    for i in range(0, len(tokens), chunk_size):
        yield " ".join(tokens[i:i + chunk_size])

def classify_text(text):
    """
    Classify the text according to O-1A criteria using zero-shot classification.
    """
    classifications = {criterion: 0 for criterion in O_1A_CRITERIA}
    for chunk in chunk_text(text):
        logging.info("Processing chunk of size: %d", len(chunk))
        try:
            result = classifier(chunk, candidate_labels=O_1A_CRITERIA)
            for label, score in zip(result['labels'], result['scores']):
                classifications[label] += score  # Increment score for each occurrence
        except Exception as e:
            logging.error("Error processing chunk: %s", e)
    return classifications
