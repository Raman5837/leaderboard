import json
import sys
from threading import Event, Thread
from typing import Dict

from core.config import RedisClient, RedisKey
from core.services import LeaderboardService


class EventConsumer:
    """
    Background worker to persist scores from Redis queue to DB
    """

    def __init__(self, queue: RedisKey = RedisKey.SCORE_QUEUE.value) -> None:
        self.__queue = queue
        self.__running = Event()
        self.__client = RedisClient()
        self.__thread = Thread(target=self.__consume_events, daemon=False)

    def start(self) -> None:
        """
        Start the consumer thread
        """

        self.__running.set()
        self.__thread.start()

    def stop(self) -> None:
        """
        Gracefully stop the consumer
        """

        if not self.__running.is_set():
            return

        print("[EventConsumer]: Shutting down...")

        self.__running.clear()
        self.__thread.join(timeout=5)
        self.__client.close_connection()

    def shutdown_handler(self, signum, frame):
        """
        Gracefully stop the consumer on shutdown signals.
        """

        _ = frame
        print(f"[EventConsumer]: Received signal {signum}. Stopping consumer...")

        self.stop()
        sys.exit(0)

    def __consume_events(self) -> None:
        """
        Continuously consume events from Redis
        """

        while self.__running.is_set():
            try:
                if payload := self.__client.pop(self.__queue, timeout=1):
                    _, event = payload
                    self.__process_event(json.loads(event))
                else:
                    print("[EventConsumer]: No new events...")

            except Exception as exception:
                print(f"[EventConsumer]: Error while consuming events: {exception}")

    def __process_event(self, event: Dict) -> None:
        """
        Process the event and store in DB
        """

        print(f"[EventConsumer]: Processing event {event}")

        try:
            mode = event["mode"]
            score = event["score"]
            user_id = event["user_id"]
            LeaderboardService.persist_session(user_id, mode, score)

        except KeyError as exception:
            print(f"[EventConsumer]: Missing key in event data: {exception}")

        except Exception as exception:
            print(
                f"[EventConsumer]: Unexpected error while processing event: {exception}"
            )
