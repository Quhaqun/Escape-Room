# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet
from rasa_sdk.executor import CollectingDispatcher


class ActionStart(Action):

    def name(self) -> Text:
        return "action_start"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(template="utter_greet")

        return []



look_descriptions = {
    "bed": "The prison bed is made of dull gray metal, with a thin mattress that sags in the middle from years of use. The bedding is sparse and worn, with a single scratchy blanket and a small, lumpy pillow. Underneath the bed frame, I can see a screwdriver tucked into a hidden",
    "lamp": "The prison lamp is a solitary source of light in an otherwise dark and foreboding cell.",
    "sink": "The prison sink is a grimy, rusted fixture that has seen better days.",
    "toilet": "Upon closer inspection, I can see that the toilet was affixed to the wall by means of four large screws.",
}

class ActionLook(Action):
    def name(self) -> Text:
        return "action_look"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        spoken = False
        for blob in tracker.latest_message['entities']:
            if blob['entity'] == 'object':
                dispatcher.utter_message(text=look_descriptions[blob['value']])
                spoken = True
        if not spoken:
            dispatcher.utter_message(text="Could you repeat what you're trying to look at?")
        return []

class ActionPickUp(Action):
    def name(self) -> Text:
        return "action_pickup"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(text="I have now picked up the screwdriver.")
        return [SlotSet("screwdriver", True)]

class Actionunscrew(Action):
    def name(self) -> Text:
        return "action_unscrew"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        slot_value = tracker.get_slot("screwdriver")
        if slot_value == True:
            dispatcher.utter_message(text=
            """I knew that the toilet held the key to my escape, and so I set to work unscrewing it from the floor.
            I retrieved the screwdriver from my pocket and began to work on the first of the four bolts that held it in place.
            It was tough going at first, as the screw had become rusted and stuck over time. But with a bit of persistence and elbow grease,
            I managed to loosen it enough to remove it entirely. With the first bolt out of the way, the rest of the job was a bit easier.
            I worked my way around the perimeter of the toilet, removing each bolt in turn and setting them aside.
            As I did so, I could feel the fixture starting to shift slightly, becoming looser and more mobile as it lost its grip on the floor.
            Finally, the last bolt came free, and the toilet was mine to move. I pulled it up and out of its mounting, taking care not to make too much noise in the process.
            Beneath it, I saw a small hole in the floor, just big enough for me to squeeze through.
            Without hesitation, I crawled into the hole, pulling the toilet along behind me. It was a tight fit, and I had to contort my body in all sorts of uncomfortable ways to make it through.
            But after a few moments of wriggling and squirming, I emerged on the other side, into a new room that I had never seen before.
            The toilet lay discarded beside me, a testament to my ingenuity and determination. And as I gazed around at my new surroundings, I knew that I had taken one step closer to freedom.""")
        else:
            dispatcher.utter_message(text="You dont have a screwdriver to do this!")
