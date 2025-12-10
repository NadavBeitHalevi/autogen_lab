import os
from autogen_ext.models.openai import OpenAIChatCompletionClient, AzureOpenAIChatCompletionClient
from autogen_core.models import ModelInfo, ModelFamily

class AgentsFactory:
    """A factory for creating different AI clients."""

    def get_client(self, client_type: str = "grok"):
        """
        Gets a concrete client instance based on the client_type.

        Args:
            client_type (str): The type of client to create ('azure', 'grok', or 'openai'). 
                               Defaults to 'grok'.

        Returns:
            An instance of the requested client, or None if configuration is missing.
        
        Raises:
            ValueError: If the client_type is unknown.
        """
        if client_type == "azure":
            return self._create_azure_client()
        elif client_type == "grok":
            return self._create_grok_client()
        elif client_type == "openai":
            return self._create_openai_client()
        else:
            raise ValueError(f"Unknown client type: {client_type}")

    def _create_azure_client(self):
        """Creates an Azure OpenAI client."""
        azure_api_key = os.getenv("AZURE_API_KEY")
        azure_api_version = os.getenv("AZURE_API_VERSION")
        azure_endpoint = os.getenv("AZURE_API_ENDPOINT")
        azure_deployment_name = os.getenv("AZURE_DEPLOYMENT_NAME")

        if not all([azure_api_key, azure_api_version, azure_endpoint, azure_deployment_name]):
            print("Azure credentials are not fully configured. Skipping Azure agent.")
            return None
        
        assert azure_deployment_name is not None and azure_api_key is not None and azure_api_version is not None and azure_endpoint is not None
        
        return AzureOpenAIChatCompletionClient(
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

    def _create_grok_client(self):
        """Creates a Grok client."""
        grok_deployment_name = os.getenv("GROK_DEPLOYMENT_NAME")
        grok_endpoint = os.getenv("GROK_ENDPOINT")
        azure_api_key = os.getenv("AZURE_API_KEY") # Re-using for Grok as per original main.py

        if not all([grok_deployment_name, grok_endpoint, azure_api_key]):
            print("Grok credentials are not fully configured. Skipping Grok agent.")
            return None

        # Ensure all variables are not None
        assert grok_deployment_name is not None and grok_endpoint is not None and azure_api_key is not None
        return OpenAIChatCompletionClient(
            model=grok_deployment_name,
            base_url=grok_endpoint,
            api_key=azure_api_key,
            temperature=0.7,
            model_info=ModelInfo(
                vision=False,
                function_calling=True,
                json_output=True,
                structured_output=True,
                family=ModelFamily.UNKNOWN,
            )
        )

    def _create_openai_client(self):
        """Creates an OpenAI client."""
        openai_api_key = os.getenv("OPENAI_API_KEY")
        if not openai_api_key:
            print("OPENAI_API_KEY is not set in environment variables. Skipping OpenAI agent.")
            return None

        return OpenAIChatCompletionClient(
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
