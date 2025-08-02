import streamlit as st
import urllib.parse

st.title("Study Topic: Related Website Suggestions")

topic = st.text_input("Enter your study topic or keyword:")

if topic:
    query = urllib.parse.quote(topic)
    
    # Popular search engines
    google_search = f"https://www.google.com/search?q={query}"
    bing_search = f"https://www.bing.com/search?q={query}"
    duckduckgo_search = f"https://duckduckgo.com/?q={query}"
    
    # Educational sites and resources
    wikipedia_search = f"https://en.wikipedia.org/wiki/{urllib.parse.quote(topic.replace(' ', '_'))}"
    khan_academy_search = f"https://www.khanacademy.org/search?page_search_query={query}"
    coursera_search = f"https://www.coursera.org/search?query={query}"
    edx_search = f"https://www.edx.org/search?q={query}"
    stackexchange_search = f"https://stackexchange.com/search?q={query}"
    quora_search = f"https://www.quora.com/search?q={query}"
    
    st.markdown("### Explore your topic on popular search engines:")
    st.markdown(f"- [Google Search]({google_search})")
    st.markdown(f"- [Bing Search]({bing_search})")
    st.markdown(f"- [DuckDuckGo Search]({duckduckgo_search})")
    
    st.markdown("### Check out these educational platforms:")
    st.markdown(f"- [Wikipedia]({wikipedia_search})")
    st.markdown(f"- [Khan Academy]({khan_academy_search})")
    st.markdown(f"- [Coursera]({coursera_search})")
    st.markdown(f"- [edX]({edx_search})")
    
    st.markdown("### Community Q&A and knowledge sharing:")
    st.markdown(f"- [Stack Exchange]({stackexchange_search})")
    st.markdown(f"- [Quora]({quora_search})")
    
else:
    st.info("Enter a topic above to get suggestions on where to find related content.")