import dotenv
import asyncio
from autogen_ext.models.openai import OpenAIChatCompletionClient, AzureOpenAIChatCompletionClient
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.messages import TextMessage
from autogen_core import CancellationToken
import os
import toml
from google import genai
from google.genai import types
from PIL import Image
import io
from autogen_core.models import ModelInfo, ModelFamily

# Load environment variables from .env file with override
dotenv.load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '.env'), override=True)

async def get_weather(city:str) -> str:
    '''Get weather for a given city'''
    return f"The weather in {city} is sunny with a high of 75°F."


async def main() -> None:
    """Initialize and run the AutoGen Lab application.
    
    Sets up the OpenAI model client for agent interactions.
    """
    
    message = TextMessage(content="Hello, AutoGen Lab!, I'd like to go to Tel-Aviv", source="user")

    print(f"Welcome to AutoGen Lab :)")

    # Initialize Azure OpenAI model client
    azure_api_key = os.getenv("AZURE_API_KEY")
    azure_api_version = os.getenv("AZURE_API_VERSION")
    azure_endpoint = os.getenv("AZURE_API_ENDPOINT")
    azure_deployment_name = os.getenv("AZURE_DEPLOYMENT_NAME")

    if not all([azure_api_key, azure_api_version, azure_endpoint, azure_deployment_name]):
        print("Azure credentials are not fully configured. Skipping Azure agent.")
    else:
        azure_client = AzureOpenAIChatCompletionClient(
            model=azure_deployment_name,
            api_key=azure_api_key,
            api_version=azure_api_version,
            azure_endpoint=azure_endpoint,
            model_info=ModelInfo(
                vision=False,
                function_calling=True,
                json_output=True,
                structured_output=True,
                family=ModelFamily.UNKNOWN,
            )
        )

        # Let's try first the AZURE gpt-4o model
        print("Running Azure GPT-4o Agent...")
        azure_agent = AssistantAgent(name="AzureWeatherBot",
                                model_client=azure_client,
                                system_message="You are a helpful assistant for an airline. You give short, humorous answers.",
                                model_client_stream=True)
        
        response = await azure_agent.on_messages([message], cancellation_token=CancellationToken())
        if response and response.chat_message and hasattr(response.chat_message, 'content'):
            print(f"Azure GPT-4o response: {response.chat_message.content}")

    # Now let's try Grok if available
    print("Attempting to run Grok Agent if configured...")

    # Initialize Grok agent
    grok_deployment_name = os.getenv("GROK_DEPLOYMENT_NAME")
    grok_endpoint = os.getenv("GROK_ENDPOINT")

    if not all([grok_deployment_name, grok_endpoint, azure_api_key]):
        print("Grok credentials are not fully configured. Skipping Grok agent.")
    else:
        # We use OpenAIChatCompletionClient but override the base_url.
        # We use the Azure API Key as it seems to be hosted on Azure.
        grok_client = OpenAIChatCompletionClient(
            model=grok_deployment_name,
            base_url=grok_endpoint,
            api_key=azure_api_key,
            temperature=0.7,
            model_info = ModelInfo(
                vision=False,
                function_calling=True,
                json_output=True,
                structured_output=True, # Indicate structured output support (required for Grok)
                family=ModelFamily.UNKNOWN,
            )
        )

        grok_agent = AssistantAgent(
            name="grok_reasoner",
            model_client=grok_client,
            system_message="You are a helpful assistant for an airline. You give short, humorous answers."
        )
        
        response = await grok_agent.on_messages([message], cancellation_token=CancellationToken())
        if response and response.chat_message and hasattr(response.chat_message, 'content'):
            print(f"Grok response: {response.chat_message.content}")

    # Now let's try OpenAI if available
    print("Attempting to run OpenAI Agent if configured...")
    openai_api_key = os.getenv("OPENAI_API_KEY")
    if not openai_api_key:
        print("OPENAI_API_KEY is not set in environment variables. Skipping OpenAI agent.")
    else:
        openai_client = OpenAIChatCompletionClient(
            model="gpt-4",
            api_key=openai_api_key,
            model_info=ModelInfo(
                vision=False,
                function_calling=True,
                json_output=True,
                structured_output=True,
                family="openai",
            )
        )
        openai_agent = AssistantAgent(
            name="OpenAIWeatherBot",
            model_client=openai_client,
            system_message="You are a helpful assistant for an airline. You give short, humorous answers."
        )
        response = await openai_agent.on_messages([message], cancellation_token=CancellationToken())
        if response and response.chat_message and hasattr(response.chat_message, 'content'):
            print(f"OpenAI response: {response.chat_message.content}")
    
if __name__ == "__main__":
    asyncio.run(main())