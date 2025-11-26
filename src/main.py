import dotenv
import asyncio
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.messages import TextMessage
from autogen_core import CancellationToken

dotenv.load_dotenv(override=True)

async def get_weather(city:str) -> str:
    '''Get weather for a given city'''
    return f"The weather in {city} is sunny with a high of 75°F."


async def main() -> None:
    """Initialize and run the AutoGen Lab application.
    
    Sets up the OpenAI model client for agent interactions.
    """
    message = TextMessage(content="Hello, AutoGen Lab!, I'd like to go to Tel-Aviv",
                          source="user")

    print(f"Wlcome to AutoGen Lab :)")
    model_client: OpenAIChatCompletionClient = OpenAIChatCompletionClient(model="gpt-4")
    
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