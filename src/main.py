import dotenv
import os

dotenv.load_dotenv(dotenv_path=".env.example", override=True)

def main():
    print(f"Hello, AutoGen Lab!")
    openai_api_key = os.getenv("OPENAI_API_KEY")
    if openai_api_key:
        print("OpenAI API Key loaded successfully.")
    else:
        print("OpenAI API Key not found. Please set it in the .env file.")
    
if __name__ == "__main__":
    main()