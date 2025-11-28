from langgraph.prebuilt import create_react_agent
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

# Agente multi-herramienta (simula multi-agente delegando tareas)
agent = create_react_agent(
    model=llm,
    tools=[get_weather, calculate],
    prompt="Eres un asistente multi-tarea. Usa get_weather para consultas de clima y calculate para cálculos matemáticos. Delega la tarea apropiada."
)