from flask import Flask, request, jsonify
import requests
import json
import openai

app = Flask(__name__)

# Set up OpenAI API credentials
openai.api_key = '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'

def fetch_user_repositories(github_url):
    username = github_url.split("/")[-1]
    api_url = f"https://api.github.com/users/{username}/repos"
    response = requests.get(api_url)

    if response.status_code == 200:
        repositories = response.json()
        return repositories
    else:
        print(f"Failed to fetch repositories. Error: {response.status_code}")

def apply_chunking(content, chunk_size):
    chunks = []
    length = len(content)

    for i in range(0, length, chunk_size):
        chunk = content[i:i+chunk_size]
        chunks.append(chunk)

    return chunks

def evaluate_code_complexity(code):
    prompt_template = "evaluate technical complexity:\n{code}\n.Provide insights."

    # Fill in the template with the code
    prompt = prompt_template.format(code=code)

    # Define GPT-3.5 parameters
    model = 'text-davinci-003'
    max_tokens = 10  # Adjust the value based on your requirements

    # Prepend or append the prompt to the code
    input_text = f"{prompt}\n\n{code}"  # You can also append the prompt if desired

    # Generate response from GPT
    response = openai.Completion.create(
        engine=model,
        prompt=input_text,
        max_tokens=max_tokens,
        n=1,
        stop=None,
        temperature=0.7
    )

    # Process the response and extract generated text
    if 'choices' in response and len(response['choices']) > 0:
        generated_text = response['choices'][0]['text']
        return generated_text
    else:
        return "Failed to generate a response."
@app.route('/analyze', methods=['POST'])
def analyze_github_complexity():
    try:
        # Provide the GitHub URL directly in the code
        github_url = "https://github.com/Annieemmanuel"

        repositories = fetch_user_repositories(github_url)

        if not repositories:
            return jsonify({'error': 'Failed to fetch repositories.'}), 500

        complexity_results = []

        for repo in repositories:
            repo_name = repo["name"]
            repo_owner = repo["owner"]["login"]
            repo_api_url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/contents"

            response = requests.get(repo_api_url)
            if response.status_code == 200:
                code_files = json.loads(response.content)

                for code_file in code_files:
                    file_name = code_file["name"]
                    file_api_url = code_file.get("download_url")

                    if not file_api_url:
                        print(f"File {file_name} does not have a download URL.")
                        continue

                    file_response = requests.get(file_api_url)
                    if file_response.status_code == 200:
                        file_content = file_response.content

                        # Apply chunking to the file_content
                        chunk_size = 1000  # Define your desired chunk size here
                        chunks = apply_chunking(file_content, chunk_size)

                        # Process each chunk as needed
                        for chunk in chunks:
                            complexity_insights = evaluate_code_complexity(chunk)
                            complexity_results.append({
                                "file_name": file_name,
                                "complexity_insights": complexity_insights
                            })

                    else:
                        print(f"Failed to fetch file {file_name}. Error: {file_response.status_code}")
            else:
                print(f"Failed to fetch code files for repository {repo_name}. Error: {response.status_code}")

        return jsonify({'complexity_results': complexity_results})

    except Exception as e:
        import traceback
        traceback.print_exc()
        print(f"An error occurred: {str(e)}")
        return jsonify({'error': 'An error occurred while analyzing the GitHub repository.'}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
