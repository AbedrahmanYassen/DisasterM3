
# Analysis:
- DisasterM3 has a minimal architecture where all model implementations, preprocessing utilities, and model-selection logic are centralized in `models/__init__.py`, while the entire benchmarking pipeline—prompt generation, dataset loading, inference, and result storage—is handled by a single script (`pyscripts/run_vllm.py`). 
- Although the code uses a useful abstraction for model-specific prompt formatting, it tightly couples dataset logic, prompts, and inference, relies on hardcoded dataset structures, and lacks a dedicated evaluation module, meaning it generates predictions but does not compute benchmark metrics such as accuracy, F1, or IoU.
- There is plenty of evaluation and benchmarking that we can get inspiration from like **[VLMEvalKit](https://github.com/open-compass/VLMEvalKit)** for evaluating VLMs, but I love the one in the internship docuement. 
## Things to reuse: 
- Model Abstraction Layer: The framework provides a common interface for multiple Vision-Language Models, making it easier to add or switch between supported model families.
- The implementation uses an abstract base class and a factory pattern to standardize model creation and interaction. This improves code organization and reduces duplication.
- The framework includes support for both image and video inputs, making it flexible enough to support different benchmark tasks.
- Bad design: Strong Dataset coupling,  Mixed Responsibilities , Missing evaluation layer, Limited experiment management and Limited extensibility. 
- The key reusable design pattern is the **Dataset Adapter Pattern**, where dataset-specific logic is encapsulated behind a unified interface. 
- Most of the benchmarking infrastructure (model runner, evaluation pipeline, and experiment tracking) can be reused directly from EarthVQA, while only the prompt templates may require adaptation to the new dataset and tasks.
- To run a different dataset through this codebase, a developer would need to:
1. Add new entries to the `prompt_libs` dictionary for the new dataset's task prompts
2. Add new `elif` branches inside `get_messages_from_data()` for the new subset names
3. Ensure the new dataset's JSON file matches the field names expected by the script (`pre_image_path`, `post_image_path`, `prompts`, `options_str`)
4. Place the dataset files in the hardcoded `data/` directory structure
5. Manually verify that none of these changes break the existing DisasterM3 workflow

## Proposed Modular Redesign<sup>1</sup>
- To improve maintainability and extensibility, the repository could be reorganized into dedicated modules:

datasets/
    base_dataset.py
    disasterm3.py
    monitrs.py

models/
    base_model.py
    qwen.py
    internvl.py
    llava.py

prompts/
    templates.py

evaluation/
    metrics.py

experiments/
    tracking.py

pyscripts/
    run_benchmark.py
3.1 Dataset Abstraction Layer
A common dataset interface should be introduced:

class BaseDataset:
    def load_data(self):
        pass

    def build_prompt(self):
        pass
Each dataset would implement its own loading and prompt-generation logic while exposing the same interface to the benchmarking pipeline.

3.2 Separation of Responsibilities
The redesigned architecture separates dataset handling, prompt generation, model execution, evaluation, and experiment tracking into dedicated modules.

This reduces coupling and improves maintainability.

3.3 Proposed Workflow
The redesigned benchmarking workflow would be:

Dataset
   ↓
Prompt Builder
   ↓
Model Runner
   ↓
Evaluator
   ↓
Experiment Tracker

### Expected Benefits
The proposed redesign would provide:

Easier integration of new datasets.
Improved code maintainability.
Dedicated support for evaluation metrics.
Better experiment management and reproducibility.
Clearer separation of responsibilities across the framework.
4. Conclusion
The DisasterM3 repository provides a functional benchmarking framework with a well-designed model abstraction layer and support for multiple Vision-Language Models. The existing model architecture is a strong foundation for future development.

However, the current implementation is tightly coupled to the DisasterM3 dataset and lacks dedicated dataset, evaluation, and experiment-management components. Introducing dataset abstractions and separating responsibilities into dedicated modules would improve scalability, maintainability, and support for future benchmarking tasks.


## Reference 
1. https://github.com/yusra-yt2209005/DisasterM3/blob/master/analysis.md#3-proposed-modular-redesign

