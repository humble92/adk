import datetime
from zoneinfo import ZoneInfo
from google.adk.agents import Agent
from google.adk.tools import google_search, agent_tool


def get_weather(city: str) -> dict:
    """Retrieves the current weather report for a specified city.

    Args:
        city (str): The name of the city for which to retrieve the weather report.

    Returns:
        dict: status and result or error msg.
    """
    if city.lower() == "new york":
        return {
            "status": "success",
            "report": (
                "The weather in New York is sunny with a temperature of 25 degrees"
                " Celsius (77 degrees Fahrenheit)."
            ),
        }
    else:
        return {
            "status": "error",
            "error_message": f"Weather information for '{city}' is not available.",
        }


def get_current_time(city: str) -> dict:
    """Returns the current time in a specified city.

    Args:
        city (str): The name of the city for which to retrieve the current time.

    Returns:
        dict: status and result or error msg.
    """

    if city.lower() == "new york":
        tz_identifier = "America/New_York"
    else:
        return {
            "status": "error",
            "error_message": (
                f"Sorry, I don't have timezone information for {city}."
            ),
        }

    tz = ZoneInfo(tz_identifier)
    now = datetime.datetime.now(tz)
    report = (
        f'The current time in {city} is {now.strftime("%Y-%m-%d %H:%M:%S %Z%z")}'
    )
    return {"status": "success", "report": report}

google_search_agent = Agent(
    name="search_assistant",
    model="gemini-2.0-flash-lite",
    instruction="Answerer questions using Google Search when needed.",
    description="An assistant that can search the web.",
    tools=[google_search],
)

time_weather_agent = Agent(
    name="weather_time_agent",
    model="gemini-2.0-flash-lite",
    description=(
        "Agent to answer questions about the time and weather in a city."
    ),
    instruction=(
        "You are a helpful agent who can answer user questions about the time and weather in a city."
    ),
    tools=[get_weather, get_current_time],
)

# See: https://github.com/buggyj/simplifai/issues/1
# See also: https://github.com/google/adk-python/issues/53
# Bug:Google search tool is not working with function tools for now
root_agent = Agent(
    name="Coordinator",
    model="gemini-2.0-flash-lite",
    description="I coordinate google search and time/weather tasks.",
    tools=[
        agent_tool.AgentTool(agent=google_search_agent),
        agent_tool.AgentTool(agent=time_weather_agent),
    ],    
    # sub_agents=[
    #     google_search_agent,
    #     time_weather_agent
    # ],
)