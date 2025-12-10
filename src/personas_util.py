import toml
from typing import Dict, Any

class PersonasUtil:
    """A utility class for loading and accessing persona configurations from a TOML file."""

    def __init__(self, config_path: str = 'src/config.toml'):
        """
        Initializes the PersonasUtil with the path to the configuration file.

        Args:
            config_path (str): The path to the TOML configuration file.
        """
        self.config_path = config_path
        self.personas = self._load_personas()

    def _load_personas(self) -> Dict[str, Any]:
        """
        Loads the personas from the TOML configuration file.

        Returns:
            A dictionary containing the persona configurations.
        """
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                return toml.load(f)
        except FileNotFoundError:
            print(f"Error: The configuration file was not found at {self.config_path}")
            return {}
        except toml.TomlDecodeError:
            print(f"Error: Could not decode the TOML file at {self.config_path}")
            return {}

    def get_persona(self, name: str) -> Dict[str, Any]:
        """
        Retrieves a specific persona by name.

        Args:
            name (str): The name of the persona to retrieve.

        Returns:
            A dictionary containing the persona's configuration, or an empty dictionary if not found.
        """
        # The scripter is nested under 'agents'
        if name.lower() == 'scripter':
            return self.personas.get('agents', {}).get('scripter', {})
        return self.personas.get(name.lower(), {})

    def get_all_personas(self) -> Dict[str, Any]:
        """
        Retrieves all loaded personas.

        Returns:
            A dictionary containing all persona configurations.
        """
        return self.personas

    def get_parliament_members(self) -> Dict[str, Dict[str, Any]]:
        """
        Retrieves only the personas that are members of the parliament.

        Returns:
            A dictionary containing the configurations for Shauli, Amatzia, Karakov, Hektor, and Avi.
        """
        members: Dict[str, Dict[str, Any]] = {}
        member_names = ['shauli', 'amatzia', 'karakov', 'hektor', 'avi']
        for name in member_names:
            if name in self.personas:
                members[name] = self.personas[name]
        return members
    
    def get_translator(self) -> Dict[str, Any]:
        """
        Retrieves the translator persona.

        Returns:
            A dictionary containing the translator's configuration.
        """
        return self.personas.get('translator', {})

if __name__ == '__main__':
    # Example usage:
    personas_util = PersonasUtil()

    # Get all parliament members
    parliament_members = personas_util.get_parliament_members()
    print("Parliament Members:")
    for name, persona in parliament_members.items():
        print(f"  - {name.capitalize()}: {persona.get('description')}")

    # Get the scripter
    scripter = personas_util.get_persona('scripter')
    if scripter:
        print("\nScripter:")
        print(f"  - Name: {scripter.get('name')}")
        print(f"  - Role: {scripter.get('role')}")

    # Get a specific member
    shauli = personas_util.get_persona('shauli')
    if shauli:
        print("\nDetails for Shauli:")
        print(f"  - Instructions: {shauli.get('instructions')}")
