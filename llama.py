from clarifai_grpc.channel.clarifai_channel import ClarifaiChannel
from clarifai_grpc.grpc.api import resources_pb2, service_pb2, service_pb2_grpc
from clarifai_grpc.grpc.api.status import status_code_pb2
import os
######################################################################################################
# In this section, we set the user authentication, user and app ID, model details, and the URL of
# the text we want as an input. Change these strings to run your own example.
######################################################################################################

# Your PAT (Personal Access Token) can be found in the portal under Authentification

PAT = os.getenv('PAT')
# Specify the correct user_id/app_id pairings
# Since you're making inferences outside your app's scope

# Change these to whatever model and text URL you want to use

USER_ID = 'meta'
APP_ID = 'Llama-2'
# Change these to whatever model and text URL you want to use
MODEL_ID = 'llama2-7b-chat'

############################################################################
# YOU DO NOT NEED TO CHANGE ANYTHING BELOW THIS LINE TO RUN THIS EXAMPLE
############################################################################



channel = ClarifaiChannel.get_grpc_channel()
stub = service_pb2_grpc.V2Stub(channel)

metadata = (('authorization', 'Key ' + PAT),)
template = """<s>[INST] <<SYS>> You are a virtual psychologist trained in Cognitive Behavioral Therapy (CBT) principles. 
Your primary function is to guide users in identifying, understanding, and challenging their cognitive distortions and unhelpful beliefs. 
Help users recognize the links between their thoughts, feelings, and behaviors. Encourage them to develop healthier thinking patterns and coping mechanisms. 
Remember to maintain empathy, confidentiality, and respect, but also note that you are not a substitute for professional, human-led therapy. 
Always refer users to seek help from licensed professionals when necessary. Keep the answers short and simple. <</SYS>>
Patient: {patient} [/INST]"""
userDataObject = resources_pb2.UserAppIDSet(user_id=USER_ID, app_id=APP_ID)
def get_response( user_prompt):
    RAW_TEXT = template.format(patient=user_prompt)
    post_model_outputs_response = stub.PostModelOutputs(
        service_pb2.PostModelOutputsRequest(
            user_app_id=userDataObject,
            # The userDataObject is created in the overview and is required when using a PAT
            model_id=MODEL_ID,
            # version_id=MODEL_VERSION_ID,  # This is optional. Defaults to the latest model version
            inputs=[
                resources_pb2.Input(
                    data=resources_pb2.Data(
                        text=resources_pb2.Text(
                            raw=RAW_TEXT
                        )
                    )
                )
            ]
        ),
        metadata=metadata
    )
    if post_model_outputs_response.status.code != status_code_pb2.SUCCESS:
        print(post_model_outputs_response.status)
        raise Exception(f"Post model outputs failed, status: {post_model_outputs_response.status.description}")
    print(post_model_outputs_response)
    result = post_model_outputs_response.outputs[0].data.text.raw
    return result

