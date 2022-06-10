import unittest
from queue import Queue, Empty
from unittest.mock import Mock

from cltl.combot.infra.event import Event
from cltl.combot.infra.event.memory import SynchronousEventBus
from cltl.combot.event.emissor import TextSignalEvent

from cltl.visualresponder.api import VisualResponder
from cltl_service.visualresponder.service import VisualResponderService


class VisualServiceTest(unittest.TestCase):
    def setUp(self) -> None:
        visual_mock = unittest.mock.MagicMock(VisualResponder)
        visual_mock.respond.side_effect = [f"response {i}" for i in range(10)]

        self.event_bus = SynchronousEventBus()
        self.service = VisualResponderService("inputTopic", "outputTopic", visual_mock, self.event_bus, None)

    def tearDown(self) -> None:
        if self.service:
            self.service.stop()

    def test_service_all_utterances(self):
        events = Queue()

        def handler(ev):
            events.put(ev)

        self.event_bus.subscribe("outputTopic", handler)

        self.service.start()

        event = events.get(timeout=1)
        self.assertEqual("TextSignalEvent", event.payload.type)
        self.assertEqual("response 0", event.payload.text)
        self.assertRaises(Empty, lambda: events.get(timeout=0.01))

        self.event_bus.publish("inputTopic", Event.for_payload(TextSignalEvent.for_agent("signal id", 1, "bla", [])))

        event = events.get(timeout=1)
        self.assertEqual("TextSignalEvent", event.payload.type)
        self.assertEqual("response 1", event.payload.text)
        self.assertRaises(Empty, lambda: events.get(timeout=0.01))
