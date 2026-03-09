
import os
import openai

# Set up OpenAI API key (if needed for authentication, even though it's not used in local case)
openai.api_key = 'your_local_api_key'

# Define the URL of your local LLM server
API_URL = "http://localhost:11434/v1"

# Function to save context
def save_context(session_id, context):
    with open(f"context_{session_id}.md", "w") as f:
        f.write(context)

# Function to load context
def load_context(session_id):
    if os.path.exists(f"context_{session_id}.md"):
        with open(f"context_{session_id}.md", "r") as f:
            return f.read()
    return ""

# Main function to handle the agent
def agent(session_id=None):
    # Load context or create a new one if it doesn't exist
    context = load_context(session_id)
    
    while True:
        user_input = input("User: ")
        
        # Combine user input with current context
        combined_input = f"Context:\n{context}\n\nUser Input:\n{user_input}"
        
        try:
            # Use the OpenAI API to send the request to your local server
            response = requests.post(
                API_URL,
                headers={"Content-Type": "application/json"},
                json={
                    "model": "local-model",  # Change this to whatever identifier you are using for your model
                    "prompt": combined_input,
                    "max_tokens": 150,  # Adjust as needed
                }
            )
            
            response.raise_for_status()  # Raise an exception if the request failed
            
            ai_response = response.json().get("choices", [{}])[0].get("text", "").strip()
            print(f"AI: {ai_response}")
        except Exception as e:
            print(f"Error: {e}")
        
        # Update context with user input and AI response
        context += f"\nUser Input:\n{user_input}\n\nAI Response:\n{ai_response}"
        
        # Save updated context
        save_context(session_id, context)

# Example usage
if __name__ == "__main__":
    session_id = "session123"  # You can generate a unique ID dynamically if needed
    agent(session_id)


