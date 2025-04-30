# AI Crew for Landing Pages
## Introduction
This project is an example using the CrewAI framework to automate the process of creating landing pages from a single idea. CrewAI orchestrates autonomous AI agents, enabling them to collaborate and execute complex tasks efficiently.

*Disclaimer: Templates are not included as they are Tailwind templates. Place Tailwind individual template folders in `./templates`, if you have a lincese you can download them at (https://tailwindui.com/templates), their references are at `config/templates.json`, this was not tested this with other templates, prompts in `tasks.py` might require some changes for that to work.*

By [@joaomdmoura](https://x.com/joaomdmoura)

- [CrewAI Framework](#crewai-framework)
- [Running the script](#running-the-script)
- [Details & Explanation](#details--explanation)
- [Using GPT 3.5](#using-gpt-35)
- [Using Local Models with Ollama](#using-local-models-with-ollama)
- [Using MCP Server Tools](#using-mcp-server-tools)
- [Contributing](#contributing)
- [Support and Contact](#support-and-contact)
- [License](#license)

## CrewAI Framework
CrewAI is designed to facilitate the collaboration of role-playing AI agents. In this example, these agents work together to transform an idea into a fully fleshed-out landing page by expanding the idea, choosing a template, and customizing it to fit the concept.

## Running the Script
It uses GPT-4 by default so you should have access to that to run it.

***Disclaimer:** This will use gpt-4 unless you changed it 
not to, and by doing so it will cost you money (~2-9 USD).
The full run might take around ~10-45m. Enjoy your time back*


- **Configure Environment**: Copy ``.env.example` and set up the environment variables for [Browseless](https://www.browserless.io/), [Serper](https://serper.dev/) and [OpenAI](https://platform.openai.com/api-keys)
- **Install Dependencies**: Run `poetry install --no-root`.
- **Add Tailwind Templates**: Place Tailwind individual template folders in `./templates`, if you have a linces you can download them at (https://tailwindui.com/templates), their references are at `config/templates.json`, I haven't tested this with other templates, prompts in `tasks.py` might require some changes for that to work.
- **Execute the Script**: Run `poetry run python main.py` and input your idea.

## Details & Explanation
- **Running the Script**: Execute `python main.py`` and input your idea when prompted. The script will leverage the CrewAI framework to process the idea and generate a landing page.
- **Output**: The generated landing page will be zipped in the a `workdir.zip` file you can download.
- **Key Components**:
  - `./main.py`: Main script file.
  - `./tasks.py`: Main file with the tasks prompts.
  - `./tools`: Contains tool classes used by the agents.
  - `./config`: Configuration files for agents.
  - `./templates`: Directory to store Tailwind templates (not included).

## Using GPT 3.5
CrewAI allow you to pass an llm argument to the agent construtor, that will be it's brain, so changing the agent to use GPT-3.5 instead of GPT-4 is as simple as passing that argument on the agent you want to use that LLM (in `main.py`).
```python
from langchain.chat_models import ChatOpenAI

llm = ChatOpenAI(model='gpt-3.5') # Loading GPT-3.5

self.idea_analyst = Agent(
    **idea_analyst_config,
    verbose=True,
    llm=llm, # <----- passing our llm reference here
    tools=[
        SearchTools.search_internet,
        BrowserTools.scrape_and_summarize_kwebsite
    ]
)
```

## Using Local Models with Ollama
The CrewAI framework supports integration with local models, such as Ollama, for enhanced flexibility and customization. This allows you to utilize your own models, which can be particularly useful for specialized tasks or data privacy concerns.

### Setting Up Ollama
- **Install Ollama**: Ensure that Ollama is properly installed in your environment. Follow the installation guide provided by Ollama for detailed instructions.
- **Configure Ollama**: Set up Ollama to work with your local model. You will probably need to [tweak the model using a Modelfile](https://github.com/jmorganca/ollama/blob/main/docs/modelfile.md), I'd recommend adding `Observation` as a stop word and playing with `top_p` and `temperature`.

### Integrating Ollama with CrewAI
- Instantiate Ollama Model: Create an instance of the Ollama model. You can specify the model and the base URL during instantiation. For example:

```python
from langchain.llms import Ollama
ollama_openhermes = Ollama(model="agent")
# Pass Ollama Model to Agents: When creating your agents within the CrewAI framework, you can pass the Ollama model as an argument to the Agent constructor. For instance:

self.idea_analyst = Agent(
    **idea_analyst_config,
    verbose=True,
    llm=ollama_openhermes, # Ollama model passed here
    tools=[
        SearchTools.search_internet,
        BrowserTools.scrape_and_summarize_website
    ]
)
```

### Advantages of Using Local Models
- **Privacy**: Local models allow processing of data within your own infrastructure, ensuring data privacy.
- **Customization**: You can customize the model to better suit the specific needs of your tasks.
- **Performance**: Depending on your setup, local models can offer performance benefits, especially in terms of latency.

## Using MCP Server Tools
The project now includes support for Machine Context Processing (MCP) servers, which provide specialized functions like math calculations and weather data retrieval.

### Setting Up MCP Server Tools
- **Install Dependencies**: The necessary dependencies are included in the `pyproject.toml` file. Run `poetry install` to update your environment.
- **Configure MCP Servers**: The project includes example MCP server implementations in the `examples` directory.

### Using MCP Tools with CrewAI
You can use the MCP tools with CrewAI agents:

```python
from landing_page_generator.tools.mcp_tools import MCPServerToolProvider

# Configure your MCP servers
mcp_server_config = {
    "math": {
        "command": "python",
        "args": ["/path/to/math_server.py"],
        "transport": "stdio",
    },
    "weather": {
        "url": "http://localhost:8000/sse",
        "transport": "sse",
    }
}

# Create the MCP provider and get individual tools
mcp_provider = MCPServerToolProvider(server_config=mcp_server_config)
mcp_tools = mcp_provider.get_tools()

# Add the tools to your agent
data_analyst = Agent(
    role="Data Analyst",
    goal="Provide accurate data and calculations",
    backstory="You are an expert data analyst with access to specialized computational tools.",
    verbose=True,
    tools=mcp_tools  # Pass the list of tools directly
)

# Don't forget to close the provider when you're done
# In an async context:
# await mcp_provider.close()
```

### Using MCP with LangGraph
You can also use the MCP tools directly with LangGraph's `create_react_agent`:

```python
from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent
from langchain_openai import ChatOpenAI

model = ChatOpenAI(model="gpt-4o")

async with MultiServerMCPClient(server_config) as client:
    agent = create_react_agent(model, client.get_tools())
    result = await agent.ainvoke({"messages": "what's (3 + 5) x 12?"})
```

For complete examples, check the `examples/mcp_agent_example.py` and `examples/langgraph_mcp_example.py` files.

## License
This project is released under the MIT License.
