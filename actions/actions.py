# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/core/actions/#custom-actions/


# This is a simple example for a custom action which utters "Hello World!"


from typing import Dict, Text, Any, List, Union, Optional
from elasticsearch import Elasticsearch
import rasa_sdk
from rasa_sdk import Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.forms import FormValidationAction
from rasa_sdk.forms import Action
from rasa_sdk.events import SlotSet, AllSlotsReset
# from weather import Weather
import requests
import json
# from rasa_core_sdk.forms import ( BooleanFormField, EntityFormField, FormAction, FreeTextFormField )

def Weather(city):
    city_api = "http://api.openweathermap.org/data/2.5/find?q={}&appid=d08af5634aa7ec71bd943b651ed453ca".format(city)
    city_json = requests.get(city_api).json()
    json_data = city_json['list'][0]
    format_add = json_data['main']
    temp = int(format_add['temp']-273)
    print(temp)
    return temp

class ActionWeather(Action):
    print("In Weather Action")

    def name(self) -> Text:
        return "action_weather"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        city = tracker.get_slot('city')
        try:
            temperature=Weather(city)
            response = "The current temperature at {} is {} degree Celsius.".format(city,temperature)
            print(response)
            dispatcher.utter_message(response)
            return [SlotSet("city", city)]
        except requests.exceptions.HTTPError as e:
            dispatcher.utter_message(text="City not found!")
        except Exception as e:
            dispatcher.utter_message(text="Could not find the city!")



# class WeatherForm(FormValidationAction):
#
#     def __init__(self):
#         super(WeatherForm, self).__init__()
#         self.slots = []
#
#     def name(self) -> Text:
#         """Unique identifier of the form"""
#         return "weather_form"
#
#     def domain_slots(self, domain: "DomainDict") -> List[Text]:
#         """Returns slots which were mapped in the domain.
#
#         Args:
#             domain: The current domain.
#
#         Returns:
#             Slot names which should be filled by the form. By default it
#             returns the slot names which are listed for this form in the domain
#             and use predefined mappings.
#         """
#         form = domain.get("forms", {}).get(self.form_name(), {})
#         if "required_slots" in form:
#             return form.get("required_slots", [])
#         return []
#
#     def slot_dom(self):
#         self.slots = self.domain_slots(Dict[Text, Any])
#         print(self.slots)
#
#     @staticmethod
#     def required_slots(self, dispatcher: "CollectingDispatcher", tracker: Tracker, domain: "DomainDict"):
#         """A list of required slots that the form has to fill"""
#         return ["city"]
#
#     # @staticmethod
#     # def required_slots(tracker: Tracker, domain: Dict[Text, Any]) -> List[Text]:
#     #     """A list of required slots that the form has to fill"""
#     #     return ["city"]
#
#     def submit(
#         self,
#         dispatcher: CollectingDispatcher,
#         tracker: Tracker,
#         domain: Dict[Text, Any],
#     ) -> List[Dict]:
#         """Define what the form has to do
#             after all required slots are filled"""
#         # utter submit template
#         city = tracker.get_slot('city')
#
#         try:
#             # city = "Atlanta"
#             city_api = "http://api.openweathermap.org/data/2.5/find?q={}&appid=d08af5634aa7ec71bd943b651ed453ca".format(city)
#             city_json = requests.get(city_api).json()
#             # api_address = 'http://api.openweathermap.org/data/2.5/weather?appid=d08af5634aa7ec71bd943b651ed453ca={}'.format(city)
#             # json_data = requests.get(api_address).json()
#             json_data = city_json['list'][0]
#             format_add = json_data['main']
#             temp = int(format_add['temp']-273)
#             dispatcher.utter_message(
#                 text="The current temperature is : {} degrees".format(temp))
#         except:
#             dispatcher.utter_message(
#                 text="Can't get the temperature for  {}".format(city))
#
#         return [AllSlotsReset()]


# wf = WeatherForm()
# print(wf.submit())

# city = "Atlanta"
# city_api = "http://api.openweathermap.org/data/2.5/find?q={}&appid=d08af5634aa7ec71bd943b651ed453ca".format(city)
# city_json = requests.get(city_api).json()
# print(city_json)
# city_id = city_json['list'][0]['id']
# # api_address = 'http://api.openweathermap.org/data/2.5/weather?id={}&units=metric&appid=d08af5634aa7ec71bd943b651ed453ca'.format(city_id)
# # json_data = requests.get(api_address).json()
# print("cityyyy", city_json['list'][0]['main']['temp'] - 273)
# format_add = json_data['main']
# temp = int(format_add['temp']-273)
# dispatcher.utter_message(
#     text="The current temperature is : {} degrees".format(temp))


# def elastic_search(query):
#     es = Elasticsearch([{'host': 'localhost', 'port': 9200}])
#     content = []
#     body = {"query": {
#         "match": {
#             "content": {
#                 "query": query
#             }
#         }
#     }
#     }
#     res = es.search(index="my_book_index", body=body)
#     for document in res['hits']['hits']:
#         content.append(document['_source']['content'])
#     return content
#
#
#
# class ObjectModifyForm(FormValidationAction):
#
#     def name(self) -> Text:
#         """Unique identifier of the form"""
#         return "modefying_form"
#
#     @staticmethod
#     def required_slots(tracker: Tracker) -> List[Text]:
#         """A list of required slots that the form has to fill"""
#         return ["object_name", "attribute"]
#
#     def submit(
#         self,
#         dispatcher: CollectingDispatcher,
#         tracker: Tracker,
#         domain: Dict[Text, Any],
#     ) -> List[Dict]:
#         """Define what the form has to do
#             after all required slots are filled"""
#         # utter submit template
#         dispatcher.utter_message(template="utter_modify_confirmation", object_name=tracker.get_slot('object_name'),
#                                  attribute=tracker.get_slot('attribute'))
#         return [AllSlotsReset()]
#
#     def slot_mappings(self) -> Dict[Text, Union[Dict, List[Dict]]]:
#         """A dictionary to map required slots to
#             - an extracted entity
#             - intent: value pairs
#             - a whole message
#             or a list of them, where a first match will be picked"""
#         return {
#             "object_name": self.from_entity(entity="object_name", intent=["give_object_name", "modify_Object"]),
#             "attribute": self.from_entity(entity="attribute", intent=["give_attribute", "modify_Object"]),
#         }
#
#
# class AttributeValueSearchForm(FormValidationAction):
#
#     def name(self) -> Text:
#         """Unique identifier of the form"""
#         return "attribute_value_search_form"
#
#     @staticmethod
#     def required_slots(tracker: Tracker) -> List[Text]:
#         """A list of required slots that the form has to fill"""
#         return ["object_name", "attribute"]
#
#     def submit(
#         self,
#         dispatcher: CollectingDispatcher,
#         tracker: Tracker,
#         domain: Dict[Text, Any],
#     ) -> List[Dict]:
#         """Define what the form has to do
#             after all required slots are filled"""
#         # utter submit template
#         dispatcher.utter_message(text="Are you sure you want to get the value for {} attribute in {} object ?".
#                                  format(tracker.get_slot('attribute'),
#                                         tracker.get_slot('object_name')))
#         return []
#
#
# class ObjectCreateForm(FormValidationAction):
#
#     def name(self) -> Text:
#         """Unique identifier of the form"""
#         return "object_create_form"
#
#     @staticmethod
#     def required_slots(tracker: Tracker) -> List[Text]:
#         """A list of required slots that the form has to fill"""
#         return ["object_type", "object_name"]
#
#     def submit(
#         self,
#         dispatcher: CollectingDispatcher,
#         tracker: Tracker,
#         domain: Dict[Text, Any],
#     ) -> List[Dict]:
#         """Define what the form has to do
#             after all required slots are filled"""
#         # utter submit template
#         dispatcher.utter_message(text="Are you sure you want create a/an {} with the name {} ?".format(
#             tracker.get_slot('object_type'), tracker.get_slot('object_name')))
#         return []
#
#     def slot_mappings(self) -> Dict[Text, Union[Dict, List[Dict]]]:
#         """A dictionary to map required slots to
#             - an extracted entity
#             - intent: value pairs
#             - a whole message
#             or a list of them, where a first match will be picked"""
#         return {
#             "object_name": self.from_entity(entity="object_name", intent=["give_object_name", "create_object"]),
#             "object_type": self.from_entity(entity="object_type", intent=["give_object_type", "create_object"],)
#         }
#
#
# class WeatherForm(FormValidationAction):
#
#     def name(self) -> Text:
#         """Unique identifier of the form"""
#         return "weather_form"
#
#     @staticmethod
#     def required_slots(tracker: Tracker) -> List[Text]:
#         """A list of required slots that the form has to fill"""
#         return ["city"]
#
#     def submit(
#         self,
#         dispatcher: CollectingDispatcher,
#         tracker: Tracker,
#         domain: Dict[Text, Any],
#     ) -> List[Dict]:
#         """Define what the form has to do
#             after all required slots are filled"""
#         # utter submit template
#         city = tracker.get_slot('city')
#
#         try:
#             api_address = 'http://api.openweathermap.org/data/2.5/weather?appid=0c42f7f6b53b244c78a418f4f181282a&q={}'.format(
#                 city)
#             json_data = requests.get(api_address).json()
#             format_add = json_data['main']
#             temp = int(format_add['temp']-273)
#             dispatcher.utter_message(
#                 text="The current temperature is : {} degrees".format(temp))
#         except:
#             dispatcher.utter_message(
#                 text="Can't get the temperature for  {}".format(city))
#
#         return [AllSlotsReset()]
#
#     def slot_mappings(self) -> Dict[Text, Union[Dict, List[Dict]]]:
#         """A dictionary to map required slots to
#             - an extracted entity
#             - intent: value pairs
#             - a whole message
#             or a list of them, where a first match will be picked"""
#         return {
#             "object_name": self.from_entity(entity="city", intent=["weather", "give_city"]),
#         }
#
#
# class ActionSearchAttributeValue(Action):
#     def name(self) -> Text:
#         return "action_search_attribute_value"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#         name = tracker.get_slot('object_name')
#         attribute = tracker.get_slot('attribute')
#         try:
#             api_address = 'http://acnextagile01.bomdimensions.com:8762/search?type=Part&name={}&attribute={}'.format(
#                 name, attribute)
#             json_data = requests.get(api_address).json()
#             dispatcher.utter_message(text=json_data['sQueryResponse'])
#         except:
#             dispatcher.utter_message(
#                 text='Something went wrong cannot retrieve the attibute value')
#
#         return [AllSlotsReset()]
#
#
# class ActionCreateObject(Action):
#     def name(self) -> Text:
#         return "action_create_object"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#         name = tracker.get_slot('object_name')
#         object_type = tracker.get_slot('object_type')
#         try:
#             api_address = 'http://acnextagile01.bomdimensions.com:8762/create?type={}&name={}'.format(
#                 object_type, name)
#             json_data = requests.get(api_address).json()
#             dispatcher.utter_message(text=json_data['sQueryResponse'])
#         except:
#             dispatcher.utter_message(
#                 text='Something went wrong please make sure you entered the values correctly')
#
#         return [AllSlotsReset()]
#
#
# class ActionGetDocuments(Action):
#     def name(self) -> Text:
#         return "action_get_documents"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#         question = tracker.get_slot('question')
#         corpus = elastic_search(question)
#         return [SlotSet("corpus", corpus)]
#
#
# class ActionGiveAnswers(Action):
#     def name(self) -> Text:
#         return "action_give_answers"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#
#         question = tracker.get_slot('question')
#         corpus = tracker.get_slot('corpus')
#         document = corpus.pop(0)
#         request_answer = {"Question": question, "Corpus": document}
#         url = 'http://127.0.0.1:5000/api'
#         response = requests.post(url, json=request_answer)
#         answer = json.loads(response.text)['Answer']
#         dispatcher.utter_message(text=answer)
#         return [SlotSet("corpus", corpus)]
