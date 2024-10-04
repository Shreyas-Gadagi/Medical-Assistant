# AI Driven Medical Assistant
This is a Application which shows how OpenAI can be used with Neo4j, Vector database and Snowflake to build and consume Knowledge Graphs using unstructured Medical Transcript Corpus. Using OpenAI GPT-4 model.

This notebook parses data from a public corpus of Medical Case Sheet using OpenAI's `gpt-4-32k` model. The model is prompted to recognise and extract entities and relationships. 

We then use the `gpt-4-32k` model and prompt it to convert questions in English to Cypher - Neo4j's query language for data retrieval.


## Notebook
The notebook is at Ingesting_data_to_neo4j  walks through prompts and tuning a model.  You will need to run that before the UI. 

## UI
The UI application is based on Streamlit. 


To install Streamlit and other dependencies:

    pip install -r requirements.txt

Check if `streamlit` command is accessible from PATH by running this command:

    streamlit --version

If not, you need to add the `streamlit` binary to PATH variable like below:

    export PATH="/app/venv/genai/bin:$PATH"

Next up you'll need to create a secrets file for the app to use.  Open the file and edit it:

    cd streamlit
    cd .streamlit
    cp secrets.toml.example secrets.toml
    vi secrets.toml

You will now need to edit that file to reflect your Azure OpenAI and Neo4j credentials. The file has the following variables:

    OPENAI_API_KEY = "" #OPENAI KEY
    OPENAI_API_TYPE = "azure"
    OPENAI_API_VERSION = "2023-03-15-preview"
    OPENAI_API_BASE = ""
    OPENAI_MODEL_NAME = "gpt-4-32k"
    OPENAI_DEPLOYMENT_NAME = "gpt-4-32k"
    NEO4J_URI = "neo4j+s://xxxxx.databases.neo4j.io" # Neo4j URL. Include port if applicable
    NEO4J_USER = "neo4j" # Neo4j User Name
    NEO4J_PASSWORD = "Foo12345678" #Neo4j Password

Now we can run the app with the commands:

    streamlit run test.py 
   

## Sample Questions to ask:
1.Who are suffering from fever give me case details?
2.give me case details of cancer patients?
3.how many male and female patients are there?
4.which patient has more number of symptoms give me case details and list all the symptoms?
5.How many patients are there in the hospital?
