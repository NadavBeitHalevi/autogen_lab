import dotenv
import asyncio
from autogen_ext.models.openai import OpenAIChatCompletionClient, AzureOpenAIChatCompletionClient
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.messages import TextMessage
from autogen_core import CancellationToken
import os

# Load environment variables from .env file with override
dotenv.load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '.env'), override=True)

async def get_weather(city:str) -> str:
    '''Get weather for a given city'''
    return f"The weather in {city} is sunny with a high of 75°F."


async def main() -> None:
    """Initialize and run the AutoGen Lab application.
    
    Sets up the OpenAI model client for agent interactions.
    """
    try:
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY is not set in environment variables.")
        else:
            print("OPENAI_API_KEY loaded successfully.")
    except Exception as e:
        print(f"Error loading environment variables: {e}")
        return
    
    message = TextMessage(content="Hello, AutoGen Lab!, I'd like to go to Tel-Aviv",
                          source="user")

    print(f"Wlcome to AutoGen Lab :)")
    model_client: OpenAIChatCompletionClient = OpenAIChatCompletionClient(model="gpt-4")
    
    azure_api_key = os.getenv("AZURE_API_KEY")
    azure_api_version = os.getenv("AZURE_API_VERSION")
    azure_endpoint = os.getenv("AZURE_API_ENDPOINT")
    
    if not azure_api_key or not azure_api_version or not azure_endpoint:
        raise ValueError("AZURE_API_KEY, AZURE_API_VERSION, and AZURE_API_ENDPOINT must be set in environment variables.")
    
    azure_client = AzureOpenAIChatCompletionClient(
        model="gpt-4o",
        api_key=azure_api_key,
        api_version=azure_api_version,
        azure_endpoint=azure_endpoint,
    )

    azure_agent = AssistantAgent(name="AzureWeatherBot",
                            model_client=azure_client,
                            system_message="You are a helpful assistant for an airline. You give short, humorous answers.",
                            model_client_stream=True)
    
    response = await azure_agent.on_messages([message], cancellation_token=CancellationToken())

    agent = AssistantAgent(name="WeatherBot", 
                           model_client=model_client,
                           system_message="You are a helpful assistant for an airline. You give short, humorous answers.",
                           model_client_stream=True)
    
    response = await agent.on_messages([message], cancellation_token=CancellationToken())
    # print(f'Full response: {response}')

    if isinstance(response.chat_message, TextMessage):
        print(f"response content: {response.chat_message.content}")
    else:
        print(f"response: {response.chat_message}")
    
if __name__ == "__main__":
    asyncio.run(main())