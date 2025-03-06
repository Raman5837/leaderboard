import atexit
import signal

from django.apps import AppConfig


class CoreConfig(AppConfig):
    name = "core"
    default_auto_field = "django.db.models.BigAutoField"

    def ready(self) -> None:
        """
        Start the background event consumer when Django starts.
        Register shutdown cleanup to stop the consumer gracefully.
        """

        from core.shared.consumer import EventConsumer

        self.__consumer = EventConsumer()
        self.__consumer.start()

        # Register cleanup when app exits
        atexit.register(self.__consumer.stop)

        # Handle termination signals (SIGINT for Ctrl+C, SIGTERM for system shutdowns)
        signal.signal(signal.SIGINT, self.__consumer.shutdown_handler)
        signal.signal(signal.SIGTERM, self.__consumer.shutdown_handler)
