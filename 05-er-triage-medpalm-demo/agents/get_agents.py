from langchain.llms import VertexAI
from langchain.agents import initialize_agent, Tool, AgentExecutor
from langchain.agents import AgentType
from tools.tools import get_patient_conditions, determine_triage_level, get_patient_profile


from dotenv import load_dotenv
import os
load_dotenv()
if __name__ == "__main__":
    pass


patient_history = Tool(
    name="patient_history",
    func=get_patient_conditions,
    description="Get patient history from FHIR using the patient's ID",
)
patients_triage = Tool(
    name="patients_triage",
    func=determine_triage_level,
    description="useful for triage patients in the ER room based on the current patients in the ER room, the maximum capacity of the ER room, the symptoms of the patient, the patient's history and the patient's profile",
)
patient_profile = Tool(
    name="patient_profile",
    func=get_patient_profile,
    description="Get patient profile from FHIR using the patient's ID",
)

def get_er_agent(temp):
    print("*" * 79)
    print("AGENT: ER agent!")
    print("*" * 79)
    llm = VertexAI(temperature=temp, verbose=True, max_output_tokens=8192,model_name=os.environ["MODEL_NAME"])
    tools_for_agent = [patient_history, patients_triage,patient_profile]
    agent = initialize_agent(
        tools_for_agent,
        llm,
        agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        verbose=True,
        handle_parsing_errors=True
    )

    return agent
