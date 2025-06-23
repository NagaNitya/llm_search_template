
from flask import Flask, request, jsonify
from utils import search_articles, fetch_article_content, concatenate_content, generate_answer

app = Flask(__name__)

@app.route('/query', methods=['POST'])
def query():
    
    # get the data/query from streamlit app
    data = request.get_json()
    user_query = data.get('query', '')  # Extract the query
    print("Received query: ", user_query)

    # Step 1: Search and scrape articles based on the query
    print("Step 1: searching articles")
    search_results = search_articles(user_query)

    articles_content = []
    for article in search_results.get("organic", []):  # Assuming "organic" holds the articles
        article_content = fetch_article_content(article['link'])  # Fetch content for each URL
        if article_content:  # If content is successfully fetched
            articles_content.append(article_content)  # Collect the content
        else:
            print(f"Failed to fetch content for {article['link']}")
            
    # Debugging output
    print(f"Fetched content for {len(articles_content)} articles.")

    # Step 2: Concatenate content from the scraped articles
    print("Step 2: concatenating content")
    concatenated_content = concatenate_content(articles_content)
    # WORKS

    # Step 3: Generate an answer using the LLM
    print("Step 3: generating answer")
    answer = generate_answer(concatenate_content, user_query)
    print("Generated answer: ", answer)

    # return the jsonified text back to streamlit
    return jsonify({"answer": answer})

if __name__ == '__main__':
    app.run(host='localhost', port=5001)
