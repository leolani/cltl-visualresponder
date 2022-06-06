import unittest
from cltl.visualresponder.visualresponder import VisualResponderImpl
from emissor.representation.scenario import ScenarioContext

class TestVisual(unittest.TestCase):
    def setUp(self) -> None:
        self.visual = VisualResponderImpl()

    def test_response(self):
        objects = ["char", "chair", "teddybear", "dog", "potted plant", "laptop", "laptop"]
        people = ["Thomas", "Selene", "Jaap", "Lea", "Mark", "Piek"]
        scenarioContext = ScenarioContext("Leolani", objects, people, people, "Piek's office")
        statement = "What did you see?"
        response = self.visual.respond(scenarioContext, statement)
        print(response)
        self.assertRegex(response, "saw")


