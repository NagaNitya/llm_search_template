
# LLM-Based RAG System

## Overview

This project is designed to create a Retrieval-Augmented Generation (RAG) system using a Large Language Model (LLM). The system integrates with an API to scrape content from the internet and uses an API to serve the LLM-generated answers. A simple front-end interface is provided to interact with the system. 
Note: ONLY use the packages provided in the requirements.txt file (similar/alternative packages are ok only if they perform similar task/function). 

## Process Overview

1. **User Input via Streamlit Interface**:
   - The user interacts with a Streamlit-based front-end where they can input their query.

2. **Query Sent to Flask Backend**:
   - The query entered by the user is sent from the Streamlit interface to a Flask backend via an API call.

3. **Internet Search and Article Scraping**:
   - The Flask backend searches the internet for the query using a designated API. It retrieves the top relevant articles and scrapes their content, extracting only the useful text (headings and paragraphs).

4. **Content Processing**:
   - The scraped content is processed to create a coherent input, which is then passed to the LLM for generating a response.

5. **LLM Response Generation**:
   - The processed content and the user's query are used to generate a contextual answer using the LLM. The LLM is accessed via an API, and the generated response is returned to the Flask backend.

6. **Response Sent Back to Streamlit Interface**:
   - The Flask backend sends the generated answer back to the Streamlit interface, where it is displayed to the user.
