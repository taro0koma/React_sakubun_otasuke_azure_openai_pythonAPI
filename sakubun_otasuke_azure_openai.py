from flask import Flask, request, jsonify
import os
from openai import AzureOpenAI

app = Flask(__name__)

# Initialize Azure OpenAI client
client = AzureOpenAI(
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    api_version="2024-02-01",
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT")
)

@app.route('/api/chat', methods=['POST'])
def chat():
    """
    Endpoint to receive chat messages from external projects.
    Expects JSON input with a `messages` field (list of messages).
    """
    try:
        # Parse input JSON
        data = request.get_json()
        messages = data.get('messages')

        if not messages:
            return jsonify({"error": "`messages` field is required and cannot be empty."}), 400

        # Call Azure OpenAI API
        response = client.chat.completions.create(
            model="gpt-35-turbo",  # Replace with your deployment name
            messages=messages
        )

        # Return response
        return jsonify({
            "model": response.model_dump_json(indent=2),
            "reply": response.choices[0].message.content
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    # Run the Flask app on a specific port
    app.run(host='0.0.0.0', port=5000)
