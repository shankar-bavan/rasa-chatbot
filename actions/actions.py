
# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet, EventType
from rasa_sdk.executor import CollectingDispatcher
import webbrowser
from weather import Weather
from main import bed_availability

class ActionVideo(Action):
    def name(self) -> Text:
        return "action_video"

    async def run(
        self,
        dispatcher,
        tracker: Tracker,
        domain: "DomainDict",
    ) -> List[Dict[Text, Any]]:
        video_url="https://youtu.be/WosDVe3tM8M"
#         video_url="https://youtu.be/Ssvu2yncgWU"
        dispatcher.utter_message("wait... Playing your video.")
        webbrowser.open(video_url)
        return []

class ValidateRestaurantForm(Action):
    def name(self) -> Text:
        return "user_details_form"

    def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict
    ) -> List[EventType]:
        required_slots = ["name", "number"]

        for slot_name in required_slots:
            if tracker.slots.get(slot_name) is None:
                # The slot is not filled yet. Request the user to fill this slot next.
                return [SlotSet("requested_slot", slot_name)]

        # All slots are filled.
        return [SlotSet("requested_slot", None)]

class ActionSubmit(Action):
    def name(self) -> Text:
        return "action_submit"

    def run(
        self,
        dispatcher,
        tracker: Tracker,
        domain: "DomainDict",
    ) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(template="utter_details_thanks",
                                 Name=tracker.get_slot("name"),
                                 Mobile_number=tracker.get_slot("number"))

class ActionHelloWorld(Action):

    def name(self) -> Text:
        return "action_weather_api"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        city=tracker.latest_message['text']
        temp=int(Weather(city)['temp']-273)
        dispatcher.utter_template("utter_temp",tracker,temp=temp)

        return []

class ActionCheckVacantBeds(Action):

    def name(self) -> Text:
        return "action_check_non_icu_vacant_beds"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # time.sleep(2)
        beds = "https://www.covidbedmbmc.in/HospitalInfo/show"
        extract_output=bed_availability(beds)
        sorted_result=sorted(extract_output,key=lambda x:x[4],reverse=True)
        dispatcher.utter_message(text="Here are the top 5 hospitals having maximum vacant beds with there contact details,")
        top_five=""
        for (hospital_name, contact, vacant, icu_vacant, non_icu_vacant) in sorted_result[:5]:
            # if contact is not None:
                top_five+='''Hospital: {} ,
Contact: {} ,
Total Vacant: {} ,
Non ICU Vacant: {} ,
Location: "[{}](https://www.google.co.in/maps/search/{})"  ,
{}\n'''.format(hospital_name, contact, vacant, non_icu_vacant, hospital_name, hospital_name.strip().replace(" ", "+"), "*" * 50)

        # print(top_five)
        dispatcher.utter_message(text=top_five)
        dispatcher.utter_message(response="utter_also_check")
        dispatcher.utter_message(text="Is there anything else that i can help you with?",buttons=[
            {"title":"Yes","payload":"/affirm"},
            {"title":"NO","payload":"/deny"},
        ])
        return []


class ActionCheckVacentBeds(Action):

    def name(self) -> Text:
        return "action_check_icu_vacant_beds"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # time.sleep(2)
        beds = "https://www.covidbedmbmc.in/HospitalInfo/show"
        extract_output=bed_availability(beds)
        sorted_result=sorted(extract_output,key=lambda x:x[3],reverse=True)
        dispatcher.utter_message(text="Here are the top 5 hospitals having maximum vacant beds with there contact details,")
        top_five=""
        for (hospital_name, contact, vacant, icu_vacant, non_icu_vacant) in sorted_result[:5]:
            # if contact is not None:
                top_five+='''Hospital: {} ,
Contact: {} ,
Total Vacant: {} ,
ICU Vacant: {} ,
Location: "[{}](https://www.google.co.in/maps/search/{})"  ,
{}\n'''.format(hospital_name, contact, vacant, icu_vacant,hospital_name,hospital_name.strip().replace(" ","+"), "*" * 50)

        # print(top_five)
        dispatcher.utter_message(text=top_five)
        dispatcher.utter_message(response="utter_also_check")
        dispatcher.utter_message(text="Is there anything else that i can help you with?", buttons=[
            {"title": "Yes", "payload": "/affirm"},
            {"title": "NO", "payload": "/deny"},
        ])
        return []

# class ActionService(Action):
#
#     def name(self) -> Text:
#         return "action_service"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#
#         buttons=[
#             {"payload":"", "title": ""},
#             {}
#         ]
#
#         dispatcher.utter_template(text="HEllo")
#
#         return []