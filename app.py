import re
import os
from fastapi import FastAPI
from fastapi.responses import PlainTextResponse
from fastapi.middleware.cors import CORSMiddleware
from langchain_google_genai import ChatGoogleGenerativeAI

key = os.getenv("API_KEY")

# Create an instance of the FastAPI class
app = FastAPI()

# Add CORS Middleware to allow requests from any origin
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust this list to specify the allowed origins (e.g., your Flutter app's domain)
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)

# Create the primary model instance outside the route
llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",
    google_api_key=key,
    temperature=0.2,
    convert_system_message_to_human=True
)

# Define a route for the root URL
@app.get("/", response_class=PlainTextResponse)
async def read_root(genre: str, lang: str, description: str):
    ques = f"write the {genre} song in {lang} for the situation of {description}"
    prompt = (
        "You are the great lyric writer, so please provide a comprehensive answer to the following request based on general knowledge:\n\n"
        f"Question: {ques}"
    )
    response = llm.invoke(prompt)

    # Access the content from the response directly
    content = response.content if hasattr(response, 'content') else ""

    # Refine and clean the content
    refined_content = content.replace("## ", "").replace("(", "").replace(")", "").strip()

    # Dynamically format sections
    formatted_content = ""
    section_pattern = re.compile(r'(?<=\n)([A-Z][a-z\-]*)')

    lines = refined_content.splitlines()
    for line in lines:
        match = section_pattern.match(line.strip())
        if match:
            formatted_content += f"\n**{line.strip()}**\n"  # Bold section names
        else:
            formatted_content += f"{line.strip()}\n"  # Regular song lines

    # Clean up extra newlines
    formatted_content = re.sub(r'\n+', '\n\n', formatted_content).strip()

    return formatted_content  # Return as plain text

# To run the app, use the command: uvicorn app:app --reload
