import unittest
import os
from src.personas_util import PersonasUtil

class TestPersonasUtil(unittest.TestCase):

    def setUp(self):
        """Set up a dummy config file for testing."""
        self.test_config_path = 'tests/test_config.toml'
        with open(self.test_config_path, 'w', encoding='utf-8') as f:
            f.write("""
[shauli]
name = "Shauli"
role = "Parliament Group Leader"
instructions = "Shauli's instructions"
description="Group leader, humorous, self-centered facilitator."

[amatzia]
name = "Amatzia"
role = "Taxi Driver"
instructions = "Amatzia's instructions"
description="Taxi driver, authentic, street-smart, socially conscious."

[karakov]
name = "Karakov"
role = "Zoo feeding aminals"
instructions = "Karakov's instructions"
description="Retired zoo feeder, quiet, dark humor, to-the-point."

[hektor]
name = "Hektor"
instructions = "Hektor's instructions"
description="Dentist (Argentinian origin), seeks justice/order, sometimes irrelevant."

[avi]
name = "Avi"
instructions = "Avi's instructions"
description="Unemployed, sarcastic, confrontational, chaotic ideas."

[translator]
name = "EnglishHebrewTranslator"
role = "Professional Translator"
instructions = "Translator's instructions"

[agents.scripter]
name = "Scripter"
role = "TV Script Writer"
instructions = "Scripter's instructions"
""")
        self.personas_util = PersonasUtil(config_path=self.test_config_path)

    def tearDown(self):
        """Remove the dummy config file."""
        os.remove(self.test_config_path)

    def test_get_parliament_members(self):
        """Test that the correct parliament members are returned."""
        members = self.personas_util.get_parliament_members()
        self.assertEqual(len(members), 5)
        self.assertIn('shauli', members)
        self.assertIn('amatzia', members)
        self.assertIn('karakov', members)
        self.assertIn('hektor', members)
        self.assertIn('avi', members)
        self.assertNotIn('translator', members)
        self.assertNotIn('scripter', members)

    def test_get_persona_instructions(self):
        """Test that the correct instructions are returned for each persona."""
        self.assertEqual(self.personas_util.get_persona('shauli')['instructions'], "Shauli's instructions")
        self.assertEqual(self.personas_util.get_persona('amatzia')['instructions'], "Amatzia's instructions")
        self.assertEqual(self.personas_util.get_persona('karakov')['instructions'], "Karakov's instructions")
        self.assertEqual(self.personas_util.get_persona('hektor')['instructions'], "Hektor's instructions")
        self.assertEqual(self.personas_util.get_persona('avi')['instructions'], "Avi's instructions")

    def test_get_scripter_instructions(self):
        """Test that the correct instructions are returned for the scripter."""
        scripter = self.personas_util.get_persona('scripter')
        self.assertEqual(scripter['instructions'], "Scripter's instructions")

    def test_get_translator_instructions(self):
        """Test that the correct instructions are returned for the translator."""
        translator = self.personas_util.get_persona('translator')
        self.assertEqual(translator['instructions'], "Translator's instructions")

    def test_get_non_existent_persona(self):
        """Test that an empty dictionary is returned for a non-existent persona."""
        persona = self.personas_util.get_persona('non_existent')
        self.assertEqual(persona, {})

if __name__ == '__main__':
    unittest.main()
