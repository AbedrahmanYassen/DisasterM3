


from datasets.disasterm3 import DisasterM3Dataset
from pyscripts.run_vllm import *
from models import *

disaster_object = DisasterM3Dataset( "bearing_body" , [])

dataset = disaster_object.load()


print(dataset[:10])
for data in dataset[:10]:
    print(data["id"])
    messages , images = get_messages_from_data(data, "bearing_body")
    print(messages)
    print(images)