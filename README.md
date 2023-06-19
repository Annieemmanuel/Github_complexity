# mercor
# GitHub Code Complexity Analyzer

This Flask application analyzes the technical complexity of code snippets from GitHub repositories. It uses OpenAI's GPT-3.5 model to evaluate factors such as code readability, algorithmic efficiency, and maintainability. The application fetches code files from a specified GitHub repository and provides insights and suggestions for improvement.

## Setup

1. Clone the repository:

   ```shell
   git clone https://github.com/your-username/code-complexity-analyzer.git

2. pip install -r requirements.txt
3. Set up OpenAI API credentials:

Sign up for an OpenAI account at https://openai.com/.
Generate an API key and replace openai_key with your API key in the openai.api_key line of app.py.
4. python mercor_test.py