from langgraph.prebuilt import create_react_agent, create_supervisor
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool

# Herramientas
@tool
def get_weather(city: str) -> str:
    """Obtiene el clima de una ciudad."""
    return f"El clima en {city} es soleado."

@tool
def calculate(expression: str) -> str:
    """Calcula una expresión matemática."""
    try:
        return str(eval(expression))
    except:
        return "Error en cálculo."

# Modelo
llm = ChatOpenAI(model="gpt-4o")

# Agentes especializados
weather_agent = create_react_agent(
    model=llm,
    tools=[get_weather],
    name="weather_agent",
    prompt="Eres un agente de clima. Responde solo sobre clima."
)

math_agent = create_react_agent(
    model=llm,
    tools=[calculate],
    name="math_agent",
    prompt="Eres un agente de matemáticas. Responde solo sobre cálculos."
)

# Supervisor
agent = create_supervisor(
    [weather_agent, math_agent],
    model=llm,
    prompt="Eres un supervisor. Delega tareas a los agentes apropiados: weather_agent para clima, math_agent para cálculos."
)