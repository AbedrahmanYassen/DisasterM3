


from datasets.disasterm3 import DisasterM3Dataset 
from datasets.monitrs import MONITRSDataset
from pyscripts.run_vllm import *
from models import *

disaster_object = DisasterM3Dataset( "bearing_body" , [])

dataset = disaster_object.load()

print("DisasterM3Dataset bearing_body samples:")
print(dataset[:5])
for data in dataset[:10]:
    print(data["id"])
    messages , images = get_messages_from_data(data, "bearing_body")
    print(messages)
    print(images)

monitrs_object = MONITRSDataset( "test" , [])

dataset = monitrs_object.load()
print("MONITRSDataset test samples:")
print(dataset[:5])
for data in dataset[:10]:
    print(data["id"])
    print(data["conversations"])