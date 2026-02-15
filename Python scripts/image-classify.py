from transformers import pipeline

image_classification_model = pipeline("image-classification")

image_path = "test1.jpg"
result = image_classification_model(images=image_path)

print("Predictions:")
for prediction in result:
    print(f"Label: {prediction['label']}, Score: {prediction['score']}")
