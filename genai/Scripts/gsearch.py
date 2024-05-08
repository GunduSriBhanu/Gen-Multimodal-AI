import streamlit as st
from googlesearch import search
from langchain_community.tools import YouTubeSearchTool

from langchain_community.utilities import StackExchangeAPIWrapper

def google_search(query, num_results=5):
    """
    Perform a Google search and return search results.

    Args:
        query (str): The search query.
        num_results (int): Number of search results to retrieve. Default is 5.

    Returns:
        list: A list of search results.
    """
    results = []
    try:
        for result in search(query, num_results=num_results):
            results.append(result)
    except Exception as e:
        print("Error:", e)
    return results

def chatbot():
    user_input = st.text_input("You:")
    if user_input:
        if user_input.lower() == 'quit':
            st.write("Chatbot: Goodbye!")
        else:
            search_results = google_search(user_input)
            if search_results:
                st.write("Chatbot: Here are some search results:")
                for i, result in enumerate(search_results, start=1):
                    st.write(f"{i}. {result}")
            else:
                st.write("Chatbot: Sorry, I couldn't find any relevant information.")

tool = YouTubeSearchTool()
print(tool.run("Construction JH Kelly"))


stackexchange = StackExchangeAPIWrapper()

print(stackexchange.run("zsh: command not found: python"))


chatbot()
