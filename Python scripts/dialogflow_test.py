from transformers import pipeline

def perform_sentiment_analysis(text):
    # Step 3: Load a pre-trained sentiment analysis model
    sentiment_analysis_model = pipeline("sentiment-analysis")

    # Step 4: Use the model for sentiment analysis
    result = sentiment_analysis_model(text)

    # Extract sentiment and confidence
    sentiment = result[0]['label']
    confidence = result[0]['score']

    print(f"Sentiment: {sentiment}, Confidence: {confidence*100}%")

if __name__ == "__main__":
    # User input for sentiment analysis
    text_to_analyze = input("Enter the text for sentiment analysis: ")

    # Call the function to perform sentiment analysis
    s = perform_sentiment_analysis(text_to_analyze)
    text_generation_model = pipeline("text-generation")
    generated_text = text_generation_model(text_to_analyze)
    print(generated_text[0]['generated_text'])
