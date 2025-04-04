from transformers import pipeline
import torch

def test_model():
    # Initialize the pipeline with a sentiment analysis model
    classifier = pipeline("sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english")
    
    # Test sentences
    test_sentences = [
        "This movie is absolutely fantastic!",
        "I really don't like this product.",
        "The weather is nice today.",
        "This is the worst experience I've ever had."
    ]
    
    # Get predictions
    results = classifier(test_sentences)
    
    # Print results
    print("\nModel Test Results:")
    print("-" * 50)
    for sentence, result in zip(test_sentences, results):
        print(f"Sentence: {sentence}")
        print(f"Label: {result['label']}")
        print(f"Score: {result['score']:.4f}")
        print("-" * 50)

if __name__ == "__main__":
    # Check if CUDA is available
    print(f"CUDA available: {torch.cuda.is_available()}")
    if torch.cuda.is_available():
        print(f"Current CUDA device: {torch.cuda.get_device_name(0)}")
    
    # Run the test
    test_model() 