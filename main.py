import os
from dotenv import load_dotenv
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel

load_dotenv()

from agent import plant_agent

console = Console()

def run():
    config = {"configurable": {"thread_id": "session_test"}}
    
    console.print("[bold green]🤖 Agent starting execution...[/bold green]\n")
    
    user_input = "გამარჯობა, შეამოწმე ეს ფოტო ხომ არ სჭირს რაიმე მცენარეს, ეს მცენარე არის პომიდორი: leaf.jpg"
    
    result = plant_agent.invoke(
        {"messages": [("user", user_input)]},
        config
    )
    
    # იღებს აგენტის ბოლო პასუხს
    final_message = result["messages"][-1]
    
    # თუ პასუხი ტექსტია, ლამაზად აფორმატირებს Markdown-ს
    if hasattr(final_message, "content") and isinstance(final_message.content, str):
        md_content = Markdown(final_message.content)
        console.print(Panel(md_content, title="[bold cyan]🌿 Greenhouse AI Assistant[/bold cyan]", border_style="green"))
    elif isinstance(final_message.content, list):
        # LangChain-ის ზოგიერთ ვერსიაში content შეიძლება იყოს სიის სახით
        text_content = "".join([item["text"] for item in final_message.content if "text" in item])
        md_content = Markdown(text_content)
        console.print(Panel(md_content, title="[bold cyan]🌿 Greenhouse AI Assistant[/bold cyan]", border_style="green"))

if __name__ == "__main__":
    run()