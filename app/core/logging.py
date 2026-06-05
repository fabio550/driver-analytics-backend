import structlog
import os


def setup_logging():
    renderer = (
        structlog.dev.ConsoleRenderer()
        if os.getenv("ENV", "dev") == "dev"
        else structlog.processors.JSONRenderer()
    )

    structlog.configure(
        processors=[
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.processors.add_log_level,
            structlog.stdlib.add_logger_name,
            renderer,
        ]
    )


logger = structlog.get_logger()