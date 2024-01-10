import os
from dotenv import load_dotenv
from agents.get_agents import get_er_agent


load_dotenv()
if __name__ == "__main__":
    pass

def triage_patient(symtoms: str , patients_id: str, max_er_capacity: int, current_er_patients: int):
    json_format = {
        "symptoms": "symtoms of the patient",
        "patient_id": "id of the patient",
        "max_er_capacity": "maximum capacity of the ER room",
        "current_er_patients": "number of current patients in the ER room",
        "triage_level": "selected triage",
        "reasoning": "reasoning for triage"
    }
    task = "You are a ER triage agent that helps nurses triage patients that come to the hospital. You need to find the patients history with the followint ID: "+ patients_id+ ". You need to find the profile of the patient to know it's age with the following Patient ID: "+ patients_id+ ". The levels of Triage are Low, Medium, High in priority. Take into account the current patients in the ER room to perform your triage." + symtoms+ ". The current patients in the ER room are: "+ str(current_er_patients)+ " and the maximum capacity of the ER room is: "+ str(max_er_capacity)+"\n The formant should be as follows: " + str(json_format) + "\n Do not use single quotes for this JSON. Use double quotes."

    agent = get_er_agent(0)
    return agent.run(task)
    