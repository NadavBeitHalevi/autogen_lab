from dotenv import load_dotenv
import asyncio
import os
import random
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.teams import SelectorGroupChat
from autogen_agentchat.conditions import MaxMessageTermination
from autogen_agentchat.messages import TextMessage # type: ignore
from autogen_core import CancellationToken
from openai import OpenAI # type: ignore
from agents_factory import AgentsFactory



# for tracing
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import ConsoleSpanExporter, SimpleSpanProcessor
from opentelemetry.instrumentation.openai_v2 import OpenAIInstrumentor # type: ignore

from personas_util import PersonasUtil # type: ignore

# setup tracing
# 1. Set up the "Console Tracer"
tracer_provider = TracerProvider()
trace.set_tracer_provider(tracer_provider)
tracer = trace.get_tracer_provider().get_tracer(__name__)
tracer_provider.add_span_processor(
    SimpleSpanProcessor(ConsoleSpanExporter())  # <--- This prints to your terminal
)

# 2. Enable automatic instrumentation
OpenAIInstrumentor().instrument()

# Load environment variables from .env file with override
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '.env'), override=True)

async def get_weather(city:str) -> str:
    '''Get weather for a given city'''
    return f"The weather in {city} is sunny with a high of 75°F."


async def main() -> None:
    """Initialize and run the AutoGen Lab application.
    
    Sets up the OpenAI model client for agent interactions.
    """
    # Load and display personas
    personas_util = PersonasUtil()
    parliament_members = personas_util.get_parliament_members()
    print("--- Parliament Members ---")
    for name, persona in parliament_members.items():
        print(f"  - {name.capitalize()}: {persona.get('description')}")
    
    scripter = personas_util.get_persona('scripter')
    if scripter:
        print("\n--- Scripter ---")
        print(f"  - Name: {scripter.get('name')}")
        print(f"  - Role: {scripter.get('role')}")
    print("-" * 20)
    
    # message = TextMessage(content="Hello, AutoGen Lab!, I'd like to go to Tel-Aviv", source="user")

    print(f"Welcome to AutoGen Lab :)")

    # Create the AgentsFactory instance
    factory = AgentsFactory()

    # get the topic from the user input (trtminal or other source
    # print("What would you like to cover today?  (Press Enter for default topic 'weather')")
    # topic = input().strip()
    # if not topic:
    #     topic = "weather"
    # print(f"Topic selected: {topic}")

    # now, use the personas util to load the personas, instructions (that should be the system message) and the description

    personas_util = PersonasUtil()
    parliament_members = personas_util.get_parliament_members()
    print("--- Parliament Members ---")
    for name, persona in parliament_members.items():
        print(f"  - {name.capitalize()}: {persona.get('description')}")
    print("-" * 20)    
    # -------------------------------------------------------

    # lets get the scripter persona and the translator persona too - print them out
    scripter = personas_util.get_persona('scripter')
    if scripter:
        print("\nScripter Persona Loaded:")
        print(f"  - Name: {scripter.get('name')}")
        print(f"  - Role: {scripter.get('role')}")
        print(f"  - Instructions: {scripter.get('instructions')}")
    translator = personas_util.get_translator()
    if translator:
        print("\nTranslator Persona Loaded:")
        print(f"  - Name: {translator.get('name')}")
        print(f"  - Role: {translator.get('role')}")
        print(f"  - Instructions: {translator.get('instructions')}")
    # -------------------------------------------------------

    # get the topic subject for the client
    print("And what topic would you like to discuss today? (Press Enter for default topic 'weather')")
    topic = input().strip()
    if not topic:
        topic = "weather"
    print(f"Topic selected: {topic}")
    # great, now that we have the personas loaded, let's create the agents using the factory
    # add both sysytem message and description from the persona
    parliament_agents: list[AssistantAgent] = []

    # select a random model for each member from the available ones    
    for parliament_member in parliament_members.values():
        # select different client - use rand for variety
        print(f"current parliament member: {parliament_member}")
        client_name = random.choice(["grok", "azure", "openai"])
        model_client = factory.get_client(client_name)
        if model_client is None:
            print(f"Warning: Could not create client '{client_name}', skipping agent creation")
            continue
        
        agent = AssistantAgent(
            name = parliament_member.get('name', 'Agent'),
            model_client=model_client,
            system_message=parliament_member.get('instructions', 'You are a helpful assistant.'),
            description=parliament_member.get('description', '')
        )
        parliament_agents.append(agent)
    # -------------------------------------------------------
    # get instructions and description for the group chat moderator (scripter persona)
    scripter_instructions = scripter.get('instructions', 'You are moderating the discussion.').format(topic)
    scripter_description = scripter.get('description', 'A skilled moderator.')

    # Get the group chat model client and ensure it's not None
    groupchat_model_client = factory.get_client("azure")
    if groupchat_model_client is None:
        print("Error: Could not create Azure client for group chat management")
        return

    groupchat = SelectorGroupChat(
        name="ParliamentChat",
        participants=parliament_agents,  # type: ignore
        model_client=groupchat_model_client,  # Using Azure for group chat management
        termination_condition=MaxMessageTermination(max_messages=5),
        allow_repeated_speaker=True,
        selector_prompt=scripter_instructions,
        description=scripter_description
    )

    result = await groupchat.run(task=f"You are discussing today's topic: {topic}.", cancellation_token=CancellationToken())

    # --- PHASE 2: SAVE (The Middleware) ---
    script_text = ""
    print("\n💾 Saving Script...")
    
    for msg in result.messages:
        # Filter out system events, keep only text messages
        if hasattr(msg, 'content') and msg.source != "user":
            script_text += f"{msg.source}: {msg.content}\n\n" # type: ignore

    print("Script Content:")
    print(script_text)

    with open("pub_script.txt", "w", encoding="utf-8") as f:
        f.write(script_text)
        
    print(f"Script saved ({len(result.messages)} messages).")

    print("\n Here is the final response from the group chat:")
    # # Initialize Azure OpenAI model client
    # azure_client = factory.get_client("azure")
    # if azure_client:
    #     # Let's try first the AZURE gpt-4o model
    #     print("Running Azure GPT-4o Agent...")
    #     azure_agent = AssistantAgent(name="AzureWeatherBot",
    #                             model_client=azure_client,
    #                             system_message="You are a helpful assistant for an airline. You give short, humorous answers.",
    #                             model_client_stream=True)
        
    #     response = await azure_agent.on_messages([message], cancellation_token=CancellationToken())
    #     if response and response.chat_message and hasattr(response.chat_message, 'content'):
    #         print(f"Azure GPT-4o response: {response.chat_message.content}")

    # # Now let's try Grok if available
    # grok_client = factory.get_client("grok")
    # if grok_client:
    #     print("Attempting to run Grok Agent if configured...")
    #     grok_agent = AssistantAgent(
    #         name="grok_reasoner",
    #         model_client=grok_client,
    #         system_message="You are a helpful assistant for an airline. You give short, humorous answers."
    #     )
        
    #     response = await grok_agent.on_messages([message], cancellation_token=CancellationToken())
    #     if response and response.chat_message and hasattr(response.chat_message, 'content'):
    #         print(f"Grok response: {response.chat_message.content}")

    # # Now let's try OpenAI if available
    # openai_client = factory.get_client("openai")
    # if openai_client:
    #     print("Attempting to run OpenAI Agent if configured...")
    #     openai_agent = AssistantAgent(
    #         name="OpenAIWeatherBot",
    #         model_client=openai_client,
    #         system_message="You are a helpful assistant for an airline. You give short, humorous answers."
    #     )
    #     response = await openai_agent.on_messages([message], cancellation_token=CancellationToken())
    #     if response and response.chat_message and hasattr(response.chat_message, 'content'):
    #         print(f"OpenAI response: {response.chat_message.content}")

    # # Now create OpenAI agent
    # client = OpenAI()
    # print("Running OpenAI GPT-5 with Web Search Tool...")
    # try:
    #     response = client.responses.create(
    #         model="gpt-5",
    #         tools=[{"type": "web_search"}],
    #         input="What was a positive news story from today?"
    #     )
    #     print("OpenAI GPT-5 response with Web Search Tool:")
    #     print(response.output_text)
    # except Exception as e:
    #     print(f"Error with OpenAI GPT-5 call: {e}")
    
if __name__ == "__main__":
    asyncio.run(main())