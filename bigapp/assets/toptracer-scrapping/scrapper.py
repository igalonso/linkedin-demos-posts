from google.cloud import documentai_v1beta3 as documentai
from google.api_core.client_options import ClientOptions
import os
import json

def process_images(folder_path, project_id, location, processor_id):
    opts = ClientOptions(api_endpoint=f"{location}-documentai.googleapis.com")
    client = documentai.DocumentProcessorServiceClient(client_options=opts)
    statistics = []
    for filename in os.listdir(folder_path):
        
        if filename.endswith(".jpg") or filename.endswith(".png") or filename.endswith(".jpeg") or filename.endswith(".PNG"):
            file_path = os.path.join(folder_path, filename)
            with open(file_path, 'rb') as image:
                image_content = image.read()

            # The full resource name of the processor, e.g.:
            # projects/project-id/locations/location/processor/processor-id
            name = f"projects/{project_id}/locations/{location}/processors/{processor_id}"

            request = documentai.types.ProcessRequest(
                name=name,
                raw_document=documentai.types.RawDocument(
                    content=image_content,
                    mime_type="image/png"
                )
            )

            result = client.process_document(request=request)
            document = result.document

            # print(f"Processed {filename}")
            # print("Document Labels:")
            hit = []
            for entity in document.entities:
                hit.append(f"{entity.type} : {entity.mention_text}")
                # print(f"- {entity.type}")
                # print(f"- {entity.mention_text}")
            statistics.append(hit)
            
    with open('statistics_toptracer.json', 'w') as json_file:
        json.dump(statistics, json_file)
    print(statistics)
# Call the function with the path to your images folder
# process_images("path_to_your_images_folder", "your_project_id", "your_location", "toptracer_processor")
# https://eu-documentai.googleapis.com/v1/projects/399208747454/locations/eu/processors/831d69ede1c9b057/processorVersions/pretrained-foundation-model-v1.0-2023-08-22:process
process_images("images", "gen-ai-igngar", "eu", "831d69ede1c9b057")

def list_processors(project_id, location):
    opts = ClientOptions(api_endpoint=f"{location}-documentai.googleapis.com")
    client = documentai.DocumentProcessorServiceClient(client_options=opts)

    parent = f"projects/{project_id}/locations/{location}"
    response = client.list_processors(parent=parent)

    for processor in response:
        print(f"Processor name: {processor.name}")
        print(f"Processor display name: {processor.display_name}")
        print(f"Processor type: {processor.type}")
        print(f"Processor state: {processor.state}")
        print()

# Call the function with your project ID and location
# list_processors("gen-ai-igngar", "eu")