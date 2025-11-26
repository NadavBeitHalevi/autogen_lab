# Copilot Instructions for autogen_lab

This repository appears to be a new project focused on AutoGen or agentic workflows.

## Project Context
- **Architecture**: Multi-agent conversation system simulating a "Parliament" group meeting.
- **Domain**: A group of friends meeting at a coffee house to discuss weekly topics with humor and specific personality traits.
- **Primary Language**: Python (Standard for AutoGen).

## Defined Personas (from `src/config.toml`)
- **Shauli**: Group leader, humorous, self-centered facilitator.
- **Amatzia**: Taxi driver, authentic, street-smart, socially conscious.
- **Karakov**: Retired zoo feeder, quiet, dark humor, to-the-point.
- **Hektor**: Dentist (Argentinian origin), seeks justice/order, sometimes irrelevant.
- **Avi**: Unemployed, sarcastic, confrontational, chaotic ideas.
- **Scripter**: Generates the initial dialogue script (British humor style).
- **Translator**: Translates the script to Hebrew and handles file I/O.

## Code Style & Conventions
- **Type Hinting**: Strictly enforce Python type hints (`typing` module) for better AI analysis.
- **Docstrings**: Use Google-style docstrings. Include `Args`, `Returns`, and `Raises`.
- **Async**: Prefer asynchronous patterns (`async`/`await`) for agent communication where applicable.

## Critical Workflows
- **Environment**: Use a virtual environment (`.venv`).
- **Dependencies**: Maintain `requirements.txt` or `pyproject.toml`.
- **Testing**: Use `pytest`. Tests should mock LLM responses to avoid API costs during CI.

## Agent Development Patterns
- **Configuration**: Externalize LLM configurations (API keys, model names) using `OAI_CONFIG_LIST` or environment variables.
- **System Messages**: Keep system prompts in separate files or clearly defined constants for maintainability.
- **Error Handling**: Implement retry logic for LLM API calls.

## Updates
As the project grows, update this file with:
- Specific service boundaries.
- Custom agent classes and their intended use.
- Debugging commands for agent interactions.
