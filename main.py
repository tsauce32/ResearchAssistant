from flask import Flask, request, render_template_string, jsonify
import openai
import os

app = Flask(__name__)

# Load the OPENAI_API_KEY from environment variables
openai.api_key = os.getenv('OPENAI_API_KEY')

# Function to get text based on the topic using OpenAI
def get_text_based_on_topic(topic):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": f"Write about {topic}."}
            ]
        )
        return response.choices[0].message['content']
    except Exception as e:
        return str(e)

# HTML template string with JavaScript for AJAX
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Text Editor</title>
<script>
function generateText(event) {
    event.preventDefault(); // Prevent the default form submission
    var topic = document.getElementById('topic').value;
    fetch('/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ topic: topic }) // Send the topic as JSON
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById('editor').value = data.text; // Update the textarea with the API response
    })
    .catch(error => console.error('Error:', error));
}
</script>
</head>
<body>
    <h1>Academic Paper Helper</h1>
    <form method="post" onsubmit="generateText(event)">
        <label for="topic">What would you like to write about?</label><br>
        <input type="text" id="topic" name="topic"><br>
        <input type="submit" value="Generate Text">
    </form>
    <textarea id="editor" name="editor" rows="20" cols="80"></textarea>
</body>
</html>
"""

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        data = request.get_json()  # Get JSON data sent from the fetch in the JavaScript
        topic = data['topic']
        text_content = get_text_based_on_topic(topic)
        return jsonify({'text': text_content})  # Respond with JSON
    else:
        # Return the empty page on a GET request
        return render_template_string(HTML_TEMPLATE)

# Run the Flask app
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
