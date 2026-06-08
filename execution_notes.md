
## dependencies: 
- needed dependencies in this project are : 
numpy
torch
torchvision
Pillow
tqdm
transformers
vllm: for linux only
qwen_vl_utils 
decord  
- I added them in the requirements.txt file. 
- I am comfortable using uv, so after creating venv, I installed them using the command: 
```CMD
uv pip install numpy torch torchvision Pillow tqdm transformers vllm qwen_vl_utils decord
```
- SO the first issue I encountered is vllm package, the project use it, but it doesn't support windows. So I had to discard it. 
- Also, I loaded a dummpy dataset similar to Disasterm3 using the extract Dataset Interface requested in task 5 and printed the first 10 objects. The dummy dataset, I generated in a script outside the repo.
- **Issue**: In the previous execution, I found that the load function is made for linux, so I adapt it to windows, of course we have to make device-agnostic. 
- Also, I executed the get_messages_from_data, and it worked fine. 
- I wanted to experement with other aspects of project, but it takes downloading models, I don't have much time to do so.