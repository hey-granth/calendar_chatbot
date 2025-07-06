from .calendar_utils import get_availability, book_event
import time
import google.api_core.exceptions
from datetime import datetime, timedelta
from langchain.agents import initialize_agent
from langchain.tools import tool
from langchain.llms.base import LLM
from typing import Optional, List, Union
import google.generativeai as genai
from .config import settings


class GeminiLLM(LLM):
    model_name: str = "models/gemini-1.5-flash-latest"
    # for i in genai.list_models():
    #     print(i.name)
    api_key: str = settings.GEMINI_API_KEY

    @property
    def _llm_type(self) -> str:
        return "gemini-llm"

    def _call(self, prompt: str, stop: Optional[Union[str, List[str]]] = None) -> str:
        genai.configure(api_key=self.api_key)
        model = genai.GenerativeModel(self.model_name)

        generation_config = {}
        if stop:
            generation_config["stop_sequences"] = [stop] if isinstance(stop, str) else stop
        try:
            response = model.generate_content(
                prompt,
                generation_config=generation_config if generation_config else None
            )
        except google.api_core.exceptions.ResourceExhausted as e:
            print("Rate limited. Retrying in 10s...")
            time.sleep(10)
            response = model.generate_content(
                prompt,
                generation_config=generation_config if generation_config else None
            )
        return response.text.strip()


@tool
def check_availability_tool(time_range: str) -> str:
    """Check upcoming events on the calendar and return count."""
    try:
        start_str, end_str = time_range.split(",")
        start = datetime.fromisoformat(start_str.replace("Z", "+00:00"))
        end = datetime.fromisoformat(end_str.replace("Z", "+00:00"))
        events = get_availability(start, end)
        return f"{len(events)} events found."
    except Exception as e:
        return f"Error parsing input: {e}"


@tool
def book_event_tool(info: str) -> str:
    """
    Book an event. Format: 'title, date(YYYY-MM-DD), time(HH:MM)'
    """
    try:
        title, date_str, time_str = [x.strip() for x in info.split(",")]
        start = datetime.strptime(f"{date_str} {time_str}", "%Y-%m-%d %H:%M")
        end = start + timedelta(minutes=30)
        return book_event(title, start, end)
    except Exception as e:
        return f"Error parsing input: {e}"

tools = [check_availability_tool, book_event_tool]

llm = GeminiLLM()
agent = initialize_agent(tools, llm, agent="chat-zero-shot-react-description", verbose=True)
