import streamlit as st
import requests

# Set page config
st.set_page_config(page_title="Pilatus", page_icon="🤖")

# Use custom CSS to style the app
st.markdown("""
<style>
.stApp {
    max-width: 800px;
    margin: 0 auto;
}
</style>
""", unsafe_allow_html=True)

st.title("Pilatus")

# Initialize session state variables
if "messages" not in st.session_state:
    st.session_state.messages = []
if "company" not in st.session_state:
    st.session_state.company = ""
if "chat_started" not in st.session_state:
    st.session_state.chat_started = False

# List of companies
companies = [
    "adidas AG",
    "Brunello Cucinelli S.p.A",
    "Burberry Group Plc",
    "Bureau Veritas SA",
    "Compagnie Financière Richemont SA",
    "Davide Campari-Milano N.V.",
    "Diageo plc",
    "EssilorLuxottica Société anonyme",
    "Eurazeo SE",
    "Hennes & Mauritz",
    "Hermès International société en commandite par actions",
    "Industria de Diseno Textil Inditex S.A.",
    "Intertek Group plc",
    "Kering SA",
    "LVMH Moët Hennesy",
    "Moncler S.p.A",
    "Nexans S.A.",
    "Nike Inc",
    "Pandora",
    "Pernod Ricard SA",
    "Prada S.p.A.",
    "Prysmian S.p.A.",
    "Publicis Groupe S.A.",
    "PUMA SE",
    "SGS SA",
    "The Interpublic Group of Companies Inc",
    "The Swatch Group AG",
    "WPP plc"
    # ... (add all 9000 companies here)
]

# Function to send message to Flowise and get response
def get_flowise_response(message, company):
    flowise_api_endpoint = "https://flowise-flowise.gdp2xu.easypanel.host/api/v1/prediction/1d5c140f-272f-4f14-a268-b6f8a5f6cc3f"
    try:
        response = requests.post(
            flowise_api_endpoint,
            json={"message": message, "company": company}
        )
        response.raise_for_status()
        return response.json()["response"]
    except requests.RequestException as e:
        return f"Sorry, I encountered an error: {str(e)}"

# Simple string matching function
def find_matches(input_string, choices, limit=5):
    input_lower = input_string.lower()
    return [choice for choice in choices if input_lower in choice.lower()][:limit]

# Start of conversation
if not st.session_state.chat_started:
    st.write("Hi there, I am Pilatus. Which company do you want to discuss today?")
    
    company_input = st.text_input("Type a company name", key="company_input")
    
    if company_input:
        matches = find_matches(company_input, companies)
        
        if matches:
            st.write("Did you mean one of these?")
            for match in matches:
                if st.button(match):
                    st.session_state.company = match
                    st.session_state.chat_started = True
                    st.experimental_rerun()
        else:
            st.warning("No matching companies found. Please try again.")
    
    if st.button("Start Chat"):
        if company_input in companies:
            st.session_state.company = company_input
            st.session_state.chat_started = True
            st.experimental_rerun()
        else:
            st.warning("Please select a valid company name from the suggestions before starting the chat.")

# Main chat interface
if st.session_state.chat_started:
    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # React to user input
    if prompt := st.chat_input(f"What do you want to know about {st.session_state.company}?"):
        # Display user message in chat message container
        st.chat_message("user").markdown(prompt)
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})

        # Get response from Flowise
        full_prompt = f"About {st.session_state.company}: {prompt}"
        assistant_response = get_flowise_response(full_prompt, st.session_state.company)

        # Display assistant response in chat message container
        with st.chat_message("assistant"):
            st.markdown(assistant_response)
        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": assistant_response})

# Add a reset button
if st.button("Reset Chat"):
    st.session_state.messages = []
    st.session_state.company = ""
    st.session_state.chat_started = False
    st.experimental_rerun()
