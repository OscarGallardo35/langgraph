from langgraph.prebuilt import create_react_agent
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langgraph.graph import StateGraph, START, END
from typing import Literal

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

# Agentes especializados
llm = ChatOpenAI(model="gpt-4o")

weather_agent = create_react_agent(
    model=llm,
    tools=[get_weather],
    prompt="Eres un agente de clima. Responde solo sobre clima."
)

math_agent = create_react_agent(
    model=llm,
    tools=[calculate],
    prompt="Eres un agente de matemáticas. Responde solo sobre cálculos."
)

# Supervisor
supervisor_prompt = """
Eres un supervisor. Decide qué agente usar basado en la consulta:
- Para clima: weather_agent
- Para cálculos: math_agent
- Si no aplica: responde directamente.

Responde solo con: weather_agent, math_agent, o END.
"""

def supervisor_node(state):
    response = llm.invoke(supervisor_prompt + f"\nConsulta: {state['query']}")
    decision = response.content.strip().lower()
    if "weather" in decision:
        return "weather_agent"
    elif "math" in decision:
        return "math_agent"
    else:
        return END

# Grafo
builder = StateGraph(dict)
builder.add_node("supervisor", supervisor_node)
builder.add_node("weather_agent", weather_agent)
builder.add_node("math_agent", math_agent)

builder.add_edge(START, "supervisor")
builder.add_conditional_edges("supervisor", lambda x: x, {"weather_agent": "weather_agent", "math_agent": "math_agent", END: END})
builder.add_edge("weather_agent", END)
builder.add_edge("math_agent", END)

graph = builder.compile()