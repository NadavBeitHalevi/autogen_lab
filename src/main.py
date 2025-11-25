import os
import autogen
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def main():
    # Configuration for the agents
    config_list = autogen.config_list_from_json(
        "OAI_CONFIG_LIST",
        filter_dict={
            "model": ["gpt-4", "gpt-3.5-turbo"],
        },
    )
    
    llm_config = {
        "config_list": config_list,
        "timeout": 120,
    }

    # Create the Assistant Agent
    assistant = autogen.AssistantAgent(
        name="assistant",
        llm_config=llm_config,
        system_message="You are a helpful AI assistant."
    )

    # Create the User Proxy Agent
    user_proxy = autogen.UserProxyAgent(
        name="user_proxy",
        human_input_mode="NEVER",
        max_consecutive_auto_reply=10,
        is_termination_msg=lambda x: x.get("content", "").rstrip().endswith("TERMINATE"),
        code_execution_config={
            "work_dir": "coding",
            "use_docker": False, 
        },
    )

    # Start the conversation
    user_proxy.initiate_chat(
        assistant,
        message="Hello! Can you help me write a Python script to print 'Hello, AutoGen'?",
    )

if __name__ == "__main__":
    main()
