import os
from dotenv import load_dotenv
from agent import triage_patient
import json

load_dotenv()
if __name__ == "__main__":
    pass

verbose = False
temp = 0
patient_id = "abbd3c1b-3048-49f2-95c9-9303b3b73d34"
symptoms = "Twisted ankle"
symptoms = "High fever and cough"
max_er_capacity = 20
current_er_patients = 20
result = triage_patient(symptoms,patient_id,max_er_capacity,current_er_patients)
print(json.loads(result))

