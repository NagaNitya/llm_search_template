from dotenv import load_dotenv
import os
import requests
from bs4 import BeautifulSoup
import openai
from langchain.memory import ConversationBufferMemory

 
env_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../.env')
load_dotenv(env_path)

# Load API keys from environment variables
SERPER_API_KEY = os.getenv("SERP_KEY")
SERPER_API_ENDPOINT = "https://google.serper.dev/search"

AZURE_API_KEY = os.getenv("AZURE_KEY")
AZURE_API_ENDPOINT="https://nagan-ma89qxi2-eastus2.cognitiveservices.azure.com/"


# memeory for storing conversation history
memory = ConversationBufferMemory()


def search_articles(query):
    """
    Searches for articles related to the query using Serper API.
    Returns a list of dictionaries containing article URLs, headings, and text.
    """
    print(query)
    articles = None
    headers = {'X-API-KEY': SERPER_API_KEY} 
    params = { "q": query, "gl": "in", "hl": "en", "num": 6} 
    try:
        # GET request
        articles = requests.get(SERPER_API_ENDPOINT, headers=headers, params=params)
        if articles.ok:  # Status code 200
            return articles.json()  
        else:
            return None
    except requests.exceptions.RequestException as e:
        print(f"Error fetching articles: {e}")
        return None

def fetch_article_content(url):
    """
    Fetches the article content, extracting headings and text.
    """
    content=""
    try:
        # Fetch the HTML content of the page
        response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
        response.raise_for_status()  # Check for request errors
        html_content = response.text

        # Parse HTML using BeautifulSoup
        soup = BeautifulSoup(html_content, 'html.parser')

        # Extract headings
        headings = []
        for heading_tag in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
            for heading in soup.find_all(heading_tag):
                if heading and heading.text:
                    headings.append(heading.text.strip())  # Get clean text

        # Extract paragraph text
        paragraphs = []
        for p in soup.find_all('p'):
            if p and p.text:  # Check if paragraph is valid and has text
                paragraphs.append(p.text.strip())

        # Combine content
        content = {
            "headings": headings,
            "paragraphs": paragraphs
        }

        return content
    except Exception as e:
        print(f"Error fetching content: {e}")
        return {"headings": [], "paragraphs": []}
    

def concatenate_content(articles):
    """
    Concatenates the content of the provided articles into a single string.
    """
    full_text = ""
    # formatting + concatenation of the string is implemented here
    for article in articles:
        headings = " ".join(article.get("headings", []))  # Combine all headings
        paragraphs = " ".join(article.get("paragraphs", []))  # Combine all paragraphs
        full_text += f"{headings}\n{paragraphs}\n\n"  # Append to the full content

    return full_text


def generate_answer(content, query):
    """
    Generates an answer from the concatenated content using GPT-4.
    The content and the user's query are used to generate a contextual answer.
    """

    response = None
    client = openai.AzureOpenAI(api_version="2024-12-01-preview",  azure_endpoint=AZURE_API_ENDPOINT,  api_key=AZURE_API_KEY)
    conversation_context = memory.load_memory_variables({})['history']  # Retrieve memory

    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": f"system", "content": "You are a friendly yet concise chat assistant. generate a response to the query using this content: \n{content}"},
                {"role": "user", "content": f"Previous conversation:\n{conversation_context}\n\nUser query:\n{query}"}
            ],
            temperature=0.7,
            max_tokens=500
        )

        ans=response.choices[0].message.content
        print(ans)
        memory.chat_memory.add_user_message(query)  # Store query
        memory.chat_memory.add_ai_message(ans)  # Store response

        return ans
    except Exception as e:
        memory.clear()  # Clears previous chat history
        return "Error generating answer. Please try again."
        

    
    