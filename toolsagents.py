# # import streamlit as st
# # from langchain_groq import ChatGroq
# # from langchain_community.utilities import ArxivAPIWrapper,WikipediaAPIWrapper
# # from langchain_community.tools import ArxivQueryRun,WikipediaQueryRun,DuckDuckGoSearchRun
# # from langchain.agents import initialize_agent,AgentType
# # from langchain.callbacks import StreamingStdOutCallbackHandler
# # import os
# # from dotenv import load_dotenv


# # # arxiv and wikipedia tools
# # api_wrapper_wiki = WikipediaAPIWrapper(top_k_results=1,doc_content_chars_max=250)
# # wiki = WikipediaQueryRun(api_wrapper=api_wrapper_wiki)

# # api_wrapper_arz = ArxivAPIWrapper(top_k_results=3,doc_content_chars_max=250)
# # arz = ArxivQueryRun(api_wrapper=api_wrapper_arz)

# # search = DuckDuckGoSearchRun(name="Search")

# # st.title("Langchain - chat with searches")
# # """
# # in this example we are using streamlit call back handler to display  thougths 
# # and actions 

# # """



# # # sidebar for settings
# # st.sidebar.title("Settings")
# # api_key = st.sidebar.text_input("Enter your groq qpi key:",type="password")

# # if "messages" not in st.session_state:
# #     st.session_state["messages"]=[
# #         {"role":"assisstant","content":"Hi i'm a chatbot who can search the web . How can i help you?"}

# #     ]

# # for msg in st.session_state.messages:
# #     st.chat_message(msg["role"]).write(msg['content'])

# # if prompt:=st.chat_input(placeholder="What is machine learning?"):
# #     st.session_state.messages.append({"role":"user","content":prompt})
# #     st.chat_message("user").write(prompt)
    
    
# #     llm = ChatGroq(
# #         model="openai/gpt-oss-120b"

# #     ,
# #         api_key=os.getenv("GROQ_API_KEY")
# #     )
# #     tools = [search,arz,wiki]

# #     search_agent = initialize_agent(tools,llm,agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,handling_parsing_errors=True)
# #     with st.chat_message("assistant"):
# #         st_cb = StreamingStdOutCallbackHandler(st.container(),expand_new_thoughts=False)
        
# #         response = search_agent.run(st.session_state.messages,callbacks=st_cb)
# #         st.session_state.messages.append({'role':'assistant',"content":response})
# #         st.write(response)


import streamlit as st
from langchain_groq import ChatGroq
from langchain_community.utilities import ArxivAPIWrapper, WikipediaAPIWrapper
from langchain_community.tools import ArxivQueryRun, WikipediaQueryRun, DuckDuckGoSearchRun
from langchain.agents import initialize_agent, AgentType
from langchain.callbacks import StreamingStdOutCallbackHandler
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# ----------------------
# Tools Setup
# ----------------------

# Wikipedia tool
api_wrapper_wiki = WikipediaAPIWrapper(top_k_results=1, doc_content_chars_max=250)
wiki_tool = WikipediaQueryRun(api_wrapper=api_wrapper_wiki)

# Arxiv tool
api_wrapper_arx = ArxivAPIWrapper(top_k_results=3, doc_content_chars_max=250)
arx_tool = ArxivQueryRun(api_wrapper=api_wrapper_arx)

# DuckDuckGo search tool
search_tool = DuckDuckGoSearchRun(name="Search")

tools = [wiki_tool, arx_tool, search_tool]

# ----------------------
# Streamlit App UI
# ----------------------
st.title("LangChain Chatbot with Search")

st.sidebar.title("Settings")
api_key_input = st.sidebar.text_input("Enter your Groq API Key:", type="password")

# Initialize chat messages
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "assistant", "content": "Hi! I'm a chatbot who can search the web. How can I help you?"}
    ]

# Display chat history
for msg in st.session_state["messages"]:
    st.chat_message(msg["role"]).write(msg["content"])

# User input
if prompt := st.chat_input(placeholder="Ask me anything..."):
    # Append user message
    st.session_state["messages"].append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    # Initialize LLM
    llm = ChatGroq(
        model="openai/gpt-oss-120b",  # replace with any valid Groq model
        api_key=api_key_input or os.getenv("GROQ_API_KEY")
    )

    # Initialize agent
    agent = initialize_agent(
        tools,
        llm,
        agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        handle_parsing_errors=True
    )

    # Stream response
    st_cb = StreamingStdOutCallbackHandler()  # ✅ No arguments needed
    with st.chat_message("assistant"):
        # Run agent
        response = agent.run(prompt, callbacks=[st_cb])
        st.session_state["messages"].append({"role": "assistant", "content": response})
        st.write(response)












