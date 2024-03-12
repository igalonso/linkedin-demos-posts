from dotenv import load_dotenv
import os
import vertexai
from vertexai.language_models import TextGenerationModel
load_dotenv()
import urllib
import warnings
from pathlib import Path as p

import pandas as pd
from langchain.prompts import PromptTemplate
from langchain.chains.summarize import load_summarize_chain
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.llms import VertexAI
from vertexai.preview.generative_models import GenerativeModel, Part

def text_summarization(
    text: str, challenge: str
) -> str:
    """Summarization Example with a Large Language Model"""
    prompt = f"You are a legal liaison that helps people with low educational resources understand legal documents. You need to answer without using any legal wording. The challenge the reader is facing is this: \n CHALLENGE: {challenge} \n TEXT: {text} \n SUMMARY:"
    parameters = {
        "candidate_count": 1,
        "max_output_tokens": 1024,
        "temperature": 0,
        "top_k": 40
    }
    model = TextGenerationModel.from_pretrained("text-unicorn@001")
    response = model.predict(
        prompt,
        **parameters
    )
    return response.text
def summarize_pdf_refine(filepath): 
    vertexai.init(project=os.getenv("PROJECT_ID"), location=os.getenv("REGION"))
    vertex_llm_text = VertexAI(model_name="text-bison@002")
    pdf_loader = PyPDFLoader(filepath)
    pages = pdf_loader.load_and_split()
    question_prompt_template = """
                    Make a summary of this text:
                    TEXT: {text}
                    SUMMARY:
                    """
    question_prompt = PromptTemplate(
        template=question_prompt_template, input_variables=["text"]
    )

    refine_prompt_template = """
                Write a concise summary of the following text delimited by triple backquotes.
                ```{text}```
                SUMMARY:
                """
    refine_prompt = PromptTemplate(
        template=refine_prompt_template, input_variables=["text"]
    )

    refine_chain = load_summarize_chain(
        vertex_llm_text,
        chain_type="refine",
        question_prompt=question_prompt,
        refine_prompt=refine_prompt,
        return_intermediate_steps=True,
    )

    refine_outputs = refine_chain({"input_documents": pages})

    final_refine_data = []
    for doc, out in zip(
        refine_outputs["input_documents"], refine_outputs["intermediate_steps"]
    ):
        output = {}
        output["file_name"] = p(doc.metadata["source"]).stem
        output["file_type"] = p(doc.metadata["source"]).suffix
        output["page_number"] = doc.metadata["page"]
        output["chunks"] = doc.page_content
        output["concise_summary"] = out
        final_refine_data.append(output)
    pdf_refine_summary = pd.DataFrame.from_dict(final_refine_data)
    pdf_refine_summary = pdf_refine_summary.sort_values(
        by=["file_name", "page_number"]
    )
    pdf_refine_summary.reset_index(inplace=True, drop=True)
    pdf_refine_summary.head()
    summary = ""
    for text_summary in pdf_refine_summary.values:
        summary = summary + text_summary[4] + "\n"
    return summary

def summarize_pdf(filepath, method_type):
    if method_type == "map_reduce":
        return summarize_pdf_mapreduce(filepath)
    elif method_type == "refine":
        return summarize_pdf_refine(filepath)


def summarize_pdf_mapreduce(filepath):
    vertexai.init(project=os.getenv("PROJECT_ID"), location=os.getenv("REGION"))
    vertex_llm_text = VertexAI(model_name="text-bison@002")
    pdf_loader = PyPDFLoader(filepath)
    pages = pdf_loader.load_and_split()
    map_prompt_template = """
                      Write a summary of this chunk of text that includes the main points and any important details.
                      {text}
                      """
    
    map_prompt = PromptTemplate(template=map_prompt_template, input_variables=["text"])
    combine_prompt_template = """
                      Write a concise summary of the following text delimited by triple backquotes.
                      Return your response in bullet points which covers the key points of the text.
                      ```{text}```
                      BULLET POINT SUMMARY:
                      """
    combine_prompt = PromptTemplate(template=combine_prompt_template, input_variables=["text"])
    map_reduce_chain = load_summarize_chain(vertex_llm_text,chain_type="map_reduce",map_prompt=map_prompt,combine_prompt=combine_prompt, return_intermediate_steps=True)
    map_reduce_outputs = map_reduce_chain({"input_documents": pages})
    final_mp_data = []
    for doc, out in zip(map_reduce_outputs["input_documents"], map_reduce_outputs["intermediate_steps"]):
        output = {}
        output["file_name"] = p(doc.metadata["source"]).stem
        output["file_type"] = p(doc.metadata["source"]).suffix
        output["page_number"] = doc.metadata["page"]
        output["chunks"] = doc.page_content
        output["concise_summary"] = out
        final_mp_data.append(output)
    pdf_mp_summary = pd.DataFrame.from_dict(final_mp_data)
    pdf_mp_summary = pdf_mp_summary.sort_values(
        by=["file_name", "page_number"]
    )  # sorting the dataframe by filename and page_number
    pdf_mp_summary.reset_index(inplace=True, drop=True)
    print(pdf_mp_summary["concise_summary"])
    summary = ""
    for summary in pdf_mp_summary["concise_summary"]:
        summary = summary + summary + "\n"
    return summary


    