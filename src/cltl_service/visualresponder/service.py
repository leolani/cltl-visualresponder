import logging

from cltl.combot.infra.config import ConfigurationManager
from cltl.combot.infra.event import Event, EventBus
from cltl.combot.infra.resource import ResourceManager
from cltl.combot.infra.time_util import timestamp_now
from cltl.combot.infra.topic_worker import TopicWorker
from cltl.visualresponder.api import VisualResponder
from cltl.combot.event.emissor import TextSignalEvent
from emissor.representation.scenario import ScenarioContext, TextSignal

logger = logging.getLogger(__name__)


CONTENT_TYPE_SEPARATOR = ';'


class VisualResponderService:
    @classmethod
    def from_config(cls, visualresponder: VisualResponder, event_bus: EventBus, resource_manager: ResourceManager,
                    config_manager: ConfigurationManager):
        config = config_manager.get_config("cltl.visualresponder")

        return cls(config.get("topic_input"), config.get("topic_output"), visualresponder, event_bus, resource_manager)

    def __init__(self, input_topic: str, output_topic: str, visualresponder: VisualResponder,
                 event_bus: EventBus, resource_manager: ResourceManager):
        self._visualresponder = visualresponder

        self._event_bus = event_bus
        self._resource_manager = resource_manager

        self._input_topic = input_topic
        self._output_topic = output_topic

        self._topic_worker = None

    @property
    def app(self):
        return None

    def start(self, timeout=30):
        self._topic_worker = TopicWorker([self._input_topic], self._event_bus, provides=[self._output_topic],
                                         resource_manager=self._resource_manager, processor=self._process,
                                         name=self.__class__.__name__)
        self._topic_worker.start().wait()

        greeting_payload = self._create_payload(self._visualresponder.respond(None))
        self._event_bus.publish(self._output_topic, Event.for_payload(greeting_payload))

    def stop(self):
        if not self._topic_worker:
            pass

        self._topic_worker.stop()
        self._topic_worker.await_stop()
        self._topic_worker = None

    def _process(self, event: Event[TextSignalEvent], scenarioContext: ScenarioContext):
        response = self._visualresponder.respond(scenarioContext, event.payload.signal.text)

        if response:
            visual_event = self._create_payload(response)
            self._event_bus.publish(self._output_topic, Event.for_payload(visual_event))

    def _create_payload(self, response):
        signal = TextSignal.for_scenario(None, timestamp_now(), timestamp_now(), None, response)

        return TextSignalEvent.create(signal)
