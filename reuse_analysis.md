# Reuse Analysis

- I will talk about what can be reused in both of MONITRS and EarthVQA, because honestly, after reviewing them I don't have much about what can be reused. 
- Also, the overall architecture suggested in the internship file is better than all ones I came over. 

## MONITRS 
- So this dataset has to be integrated into the evaluation framework, because it's kind of relevant to natural disasture anaylsis. But some mapping to DisasterM3 format has to be done. 
- the evaluation part is missing in the DisasterM3 code, but it's available in the /Evalute in the MONITRS, and it covers the metrics mentioned in the DisasterM3 paper (e.g. accuracy and VLM as a judge). so I guess we can reuse this part.

## EarthVQA
- At first, I thought this dataset is irrelevant to our case, I mean it's not for natural disasters, but turned out that it could be really valuable in some evaluation tasks for example counting. 
- It's a dataset for "kind of" general queries about satellite images, you could ask questions related to counting like "What is the area of the forest?", or judging like "Is it a rural or urban scene?", and plenty of other things. 
- This dataset could be integrated in the project, but it has to be mapped and used in evaluation carefully"Honeslty, I need to familarize with it more". 
### Normalized Representation <sup> 1 </sup>
- EarthVQA can be mapped into the following unified structure:

```python
{
    "id": "...",
    "images": ["image.jpg"],
    "question": "...",
    "options": ["A", "B", "C", "D"],  # optional depending on task variant
    "answer": "B",
    "task_type": "vqa"
}
```
### Reusability Analysis <sup>2</sup>

#### Components Reused Without Modification

| Component           | Reusable  | Explanation                                |
| ------------------- | --------- | ------------------------------------------ |
| Model Runner        | Yes       | EarthVQA uses same VLM input format        |
| Prompt Structure    | Partially | Can reuse VQA prompt templates             |
| Evaluation Logic    | Yes       | Accuracy-based evaluation applies directly |
| Experiment Tracking | Yes       | Independent of dataset                     |

#### Components Requiring Adaptation

| Component       | Change Required | Reason                          |
| --------------- | --------------- | ------------------------------- |
| Dataset Loader  | Yes             | EarthVQA file structure differs |
| Prompt Template | Minor           | Question formatting differences |



## References
1. https://github.com/yusra-yt2209005/DisasterM3/blob/master/reuse_analysis.md#normalized-representation 
2. https://github.com/yusra-yt2209005/DisasterM3/blob/master/reuse_analysis.md#4-reusability-analysis 
