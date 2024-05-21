import vertexai
# from google.auth.transport.requests import Request
# from google.oauth2.credentials import Credentials
# from google_auth_oauthlib.flow import InstalledAppFlow
import base64
import vertexai
from vertexai.generative_models import GenerativeModel, Part, FinishReason
import vertexai.preview.generative_models as generative_models
import os
from vertexai.generative_models import (
    FunctionDeclaration,
    GenerativeModel,
    Tool,
)
from langchain.agents import AgentExecutor
from langchain.agents.format_scratchpad import format_to_openai_function_messages
from langchain.agents.output_parsers import OpenAIFunctionsAgentOutputParser
from langchain.memory import ConversationBufferWindowMemory
from langchain.tools.retriever import create_retriever_tool
# from langchain_chroma import Chroma
from langchain_community.document_loaders.csv_loader import CSVLoader
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.pydantic_v1 import BaseModel, Field
# from langchain_google_vertexai import ChatVertexAI, VertexAIEmbeddings
from langchain_google_vertexai import ChatVertexAI
from langchain_community.document_loaders import PyPDFLoader
from langchain.pydantic_v1 import BaseModel, Field
from langchain.tools import BaseTool, StructuredTool, tool


os.environ["LANGCHAIN_API_KEY"] = "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"
LANGCHAIN_TRACING_V2=True
LANGCHAIN_ENDPOINT="https://api.smith.langchain.com"
LANGCHAIN_API_KEY= "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"
from langsmith import traceable


from vertexai.generative_models._generative_models import ToolConfig
from langchain_core.messages import AIMessage, HumanMessage

safety_settings = {
    generative_models.HarmCategory.HARM_CATEGORY_HATE_SPEECH: generative_models.HarmBlockThreshold.BLOCK_ONLY_HIGH,
    generative_models.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: generative_models.HarmBlockThreshold.BLOCK_ONLY_HIGH,
    generative_models.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: generative_models.HarmBlockThreshold.BLOCK_ONLY_HIGH,
    generative_models.HarmCategory.HARM_CATEGORY_HARASSMENT: generative_models.HarmBlockThreshold.BLOCK_ONLY_HIGH,
}
class SearchInput(BaseModel):
    search_text: str = Field(description="Debe ser una pregunta sobre el Google Cloud Summit Madrid.")

@tool("search-tool", args_schema=SearchInput, return_direct=True)
def search_in_pdf(search_text):
    """Busca informacion en un documento PDF sobre el Google Cloud Summit Madrid."""
    # vertexai.init(project="gen-ai-igngar", location="us-central1")
    model = GenerativeModel(
        "gemini-1.5-flash-preview-0514",
    )
    document1 = Part.from_uri(
        mime_type="application/pdf",
        uri="gs://madrid-summit-24-igngar/cloudonair_withgoogle.pdf")
    
    generation_config = {
        "max_output_tokens": 8192,
        "temperature": 1,
        "top_p": 0.95,
    }

    safety_settings = {
        generative_models.HarmCategory.HARM_CATEGORY_HATE_SPEECH: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
        generative_models.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
        generative_models.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
        generative_models.HarmCategory.HARM_CATEGORY_HARASSMENT: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
    }
    responses = model.generate_content(
        [document1, "Responde siempre en Español y usando muchos emojis: "+ search_text],
        generation_config=generation_config,
        safety_settings=safety_settings,
        stream=False,
    )
    return responses.candidates[0].content.parts[0].text

tools= [search_in_pdf]

langchain_prompt_nosp = ChatPromptTemplate.from_messages(
    [
        MessagesPlaceholder(variable_name="chat_history", optional=True),
        ("user", "{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ]
)

langchain_model_g15_nosp = ChatVertexAI(
    model_name="gemini-1.5-pro-preview-0514",
    temperature=0,
    safety_settings=safety_settings,
)

langchain_model_g15_nosp_tools = langchain_model_g15_nosp.bind(functions=tools)

memory = ConversationBufferWindowMemory(
    K=6,
    return_messages=True,
    memory_key="chat_history",
    output_key="output",
)
chat_history = []

class AgentInput(BaseModel):
    input: str
    chat_history: list[tuple[str, str]] = Field(
        ..., extra={"widget": {"type": "chat", "input": "input", "output": "output"}}
    )


agent_g15_nosp = (
    {
        "input": lambda x: x["input"],
        "chat_history": lambda x: x["chat_history"],
        "agent_scratchpad": lambda x: format_to_openai_function_messages(
            x["intermediate_steps"]
        ),
    }
    | langchain_prompt_nosp
    | langchain_model_g15_nosp_tools
    | OpenAIFunctionsAgentOutputParser()
)

agent_executor_g15_nosp = AgentExecutor(
    agent=agent_g15_nosp,
    tools=tools,
    memory=memory,
    return_intermediate_steps=True,
    verbose=True,
).with_types(input_type=AgentInput)

@traceable
def agent_executor_function(message):
    result = agent_executor_g15_nosp.invoke(
        {"input": message, "chat_history": memory.buffer_as_messages}
    )
    chat_history.extend(
        [
            HumanMessage(content=message),
            AIMessage(content=result["output"]),
        ]
    )
    print(result["output"])
    return result["output"]

# test_message_1 = "¿Cuál es la sesión a la que debo ir si quiero ver algo sobre VMware?"
# agent_executor_function(agent_executor_g15_nosp, test_message_1, memory)


