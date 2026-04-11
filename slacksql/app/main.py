from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from app.config import settings
from app.bot.handler import handle_ask_command


def start():
    try:
        app = App(
            token=settings.SLACK_BOT_TOKEN.get_secret_value(),
            signing_secret=settings.SLACK_SIGNING_SECRET.get_secret_value()
        )
        
        app.command("/ask")(handle_ask_command) 
        handler = SocketModeHandler(app, settings.SLACK_APP_TOKEN.get_secret_value())
        handler.start()
    except Exception as e:
        print(f"Failed to start: {e}")
    
if __name__ == "__main__":
    start()
    