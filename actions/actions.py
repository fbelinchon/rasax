# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.forms import FormValidationAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
import requests


key='3df4137afb5038ed8b916a7cff9e76bd'
api_address='https://api.openweathermap.org/data/2.5/weather?q=ciudad&lang=es&units=metric&appid='+key

ESTACIONES = ["coslada","móstoles","mostoles","villarejo","alcalá","alcala","aranjuez"]


class ActionHelloWorld(Action):

    

    def name(self) -> Text:
        return "action_weather"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        texto=""
        lugar =next(tracker.get_latest_entity_values("LOC"), None)

        if (lugar == None):
            texto="no he entendido el nombre de la ciudad. ¿puedes repetirlo, porfavor?"
        else:

            temperatura,desc = self.temperatura(lugar)
            texto="el tiempo en "+lugar+" es " +desc+" , la temperatura es de "+ temperatura +" grados centígrados"
            
        dispatcher.utter_message(text=texto)

        return []

    def temperatura(self,ciudad= "Madrid"):
        url = api_address.replace('ciudad',ciudad)
       
        json_data=requests.get(url).json()
        temperature = str(round(json_data["main"]["temp"]))
        desc=json_data["weather"][0]["description"]
        return temperature,desc

class ValidateCitaForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_cita_form"
    def validate_estacion(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text,Any]:
        """Valida estaciones"""
        if slot_value.lower() not in ESTACIONES:
            dispatcher.utter_message(text=f"{slot_value.lower()} no es una estación conocida")
            return {"estacion": None}
        else:
            dispatcher.utter_message(text=f"Perfecto, quieres información para la estación de {slot_value}")
            return{"estacion": slot_value}

    def validate_time(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text,Any]:
        """Valida time"""
        dispatcher.utter_message(text=f"Perfecto, quieres información para el día {slot_value}")
        return{"time": slot_value}

    def validate_turno(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text,Any]:
        """Valida turno"""
        dispatcher.utter_message(text=f"Perfecto, quieres información para el turno {slot_value}")
        return{"turno": slot_value}

class ValidateHorarioForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_horario_form"
    def validate_estacion(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text,Any]:
        """Valida estaciones"""
        if slot_value.lower() not in ESTACIONES:
            dispatcher.utter_message(text=f"{slot_value.lower()} no es una estación conocida")
            return {"estacion": None}
        else:
            dispatcher.utter_message(text=f"Perfecto, quieres información sobre el horario de la estación de {slot_value}")
            dispatcher.utter_message(text=f"la estación de {slot_value} abre de 8:00 a 14:00 y de 15:00 a 22:00")
            return{"estacion": None}

   