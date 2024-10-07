# Import the FastAPI class
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from langchain_google_genai import ChatGoogleGenerativeAI

# Replace 'your_google_api_key' with your actual Google API key
key = "AIzaSyAapf_GYO6P5XZz8Kp9b8rh-25eKV7UYt8"

# Create an instance of the FastAPI class
app = FastAPI()

# Create the primary model instance outside the route
llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",
    google_api_key=key,
    temperature=0.2,
    convert_system_message_to_human=True
)

# Define a route for the root URL
@app.get("/")
async def read_root(genre:str,lang:str,description:str):
    ques=f"write the {genre} song in {lang} for the situation of {description}"
    prompt = (
        "Please provide a comprehensive answer to the following question based on general knowledge:\n\n"
        f"Question: {ques}"
    )
    response = llm.invoke(prompt)
    return response

# To run the app, use the command: uvicorn filename:app --reload
