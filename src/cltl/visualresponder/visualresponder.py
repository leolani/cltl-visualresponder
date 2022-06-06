from random import choice
from cltl.visualresponder.api import VisualResponder
from emissor.representation.scenario import ScenarioContext

class VisualResponderImpl(VisualResponder):

    SEE_OBJECT = [
        "what do you see",
        "what can you see",
        "what did you see",
        "what have you seen"
    ]

    SEE_PERSON = [
        "who do you see",
        "who can you see",
    ]

    SEE_PERSON_ALL = [
        "who did you see",
        "who have you seen"
    ]

    SEE_SPECIFIC = [
        "do you see ",
        "can you see ",
        "where is the "
    ]

    I_SEE = [
        "I see",
        "I can see",
        "I think I see",
        "I observe",
    ]

    I_SAW = [
        "I saw",
        "I have seen",
        "I think I observed"
    ]

    NO_OBJECT = [
        "I don't see anything",
        "I don't see any object",
    ]

    NO_PEOPLE = [
        "I don't see anybody I know",
        "I don't see familiar faces",
        "I cannot identify any of my friends",
    ]

    def __init__(self):
        self.started = False

    #TODO use the confidence scores from the return in the output
    def respond(self, scenarioContext:ScenarioContext, statement:str) -> str:

        objects = [obj.name for obj in scenarioContext.objects]
        people = [p.name for p in scenarioContext.people]

        all_people = [p.name for p in scenarioContext.all_people]

        # Enumerate Currently Visible Objects
        if statement.lower() in self.SEE_OBJECT:
            if objects:
                say = "{} {}".format(choice(self.I_SEE), self._objects_to_sequence(objects))
                return say
               # return 1, lambda: app.say("{} {}".format(choice(self.I_SEE), self._objects_to_sequence(objects)))
            else:
                return choice(self.NO_OBJECT)
               # return 0.5, lambda: app.say(choice(self.NO_OBJECT))

        # Enumerate Currently Visible People
        elif statement.lower() in self.SEE_PERSON:
            if people:
                say = "{} {}".format(choice(self.I_SEE), self._people_to_sentence(people))
                return say
               # return 1, lambda: app.say("{} {}".format(choice(self.I_SEE), self._people_to_sentence(people)))
            else:
                return choice(self.NO_PEOPLE)
              #  return 0.5, lambda: app.say(choice(self.NO_PEOPLE))

        # Enumerate All Observed People
        elif statement.lower() in self.SEE_PERSON_ALL:
            if all_people:
                return "{} {}".format(choice(self.I_SAW), self._people_to_sentence(all_people))
             #   return 1, lambda: app.say("{} {}".format(choice(self.I_SAW), self._people_to_sentence(all_people)))
            else:
                return choice(self.NO_PEOPLE)
              #  return 0.5, lambda: app.say(choice(self.NO_PEOPLE))

        else:
            return "Sorry but I cannot see it."

#TODO checkout the pepper3 code how the pointing works
        # Respond to Individual Object Queries
#        else:
#            for cue in self.SEE_SPECIFIC:
#                if cue in utterance.transcript.lower():
#                    for obj in utterance.context.objects:
#                        if obj.name.lower() in utterance.transcript.lower():
#                            return 1.0, lambda: self._point_to_objects(app, obj)
#
#                    return 1.0, lambda: app.say("I cannot see {}".format(self._insert_a_an(utterance.tokens[-1])))

#    def _point_to_objects(self, app, obj):
#        app.say("I can see {}".format(self._insert_a_an(obj.name)))
#        app.motion.point(obj.direction, speed=0.2)
#        app.motion.look(obj.direction, speed=0.1)
#        app.say("There it is!!")
