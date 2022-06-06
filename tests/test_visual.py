import unittest
from cltl.visualresponder.visualresponder import VisualResponderImpl
from emissor.representation.scenario import ScenarioContext

class TestVisual(unittest.TestCase):
    def setUp(self) -> None:
        self.visual = VisualResponderImpl()

    def test_response(self):
        scenarionContext = ScenarioContext()
        scenarionContext.objects = ["char", "chair", "teddybear", "dog", "potted plant", "laptop", "laptop"]
        scenarionContext.people = ["Thomas", "Selene", "Jaap", "Lea", "Mark", "Piek"]
        statement = "What did you see?"
        response = self.visual.respond(scenarionContext, statement)
        print(response)
        self.assertRegex(response)


