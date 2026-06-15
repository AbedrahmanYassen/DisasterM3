"""
config.py
---------
Loads a YAML config file and maps every section to a typed Python dataclass.

Usage
-----
    from config import load_config

    cfg = load_config("configs/disasterm3_qwen_vqa.yaml")

    print(cfg.model.model_id)          # "Qwen/Qwen2.5-VL-7B-Instruct"
    print(cfg.dataset.subset)          # "disaster_type"
    print(cfg.tracking.backend)        # "mlflow"
"""

from __future__ import annotations

import yaml
from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Optional


# ─────────────────────────────────────────────────────────────────────────────
# Section dataclasses
# Each class mirrors one top-level key in the YAML file.
# ─────────────────────────────────────────────────────────────────────────────

@dataclass
class ExperimentConfig:
    """Metadata that identifies the run in the experiment tracker."""
    name: str
    description: str = ""
    tags: List[str] = field(default_factory=list)
    seed: int = 42

    VALID_SUBSETS = {
        "bearing_body", "building_damage_counting", "disaster_type",
        "road_damage_counting", "landuse", "relational_reasoning_qa",
        "caption", "recovery",
    }

    @classmethod
    def from_dict(cls, d: dict) -> "ExperimentConfig":
        return cls(
            name=d["name"],
            description=d.get("description", ""),
            tags=d.get("tags", []),
            seed=d.get("seed", 42),
        )


@dataclass
class DatasetConfig:
    """
    Controls which dataset/subset is loaded and how samples are pre-processed.

    dataset.name   → selects the DatasetLoader class (e.g. DisasterM3Dataset)
    dataset.subset → selects the JSON file and prompt template inside that dataset
    """
    name: str                          # disasterm3 | earthvqa | monitrs
    subset: str                        # disaster_type | bearing_body | …
    data_root: str = "data"            # path that contains images/ and *.json
    max_samples: Optional[int] = None  # None = full split
    overwrite: bool = False            # re-run even if results already exist
    image_size: Optional[int] = None   # None = model-native resolution

    @classmethod
    def from_dict(cls, d: dict) -> "DatasetConfig":
        return cls(
            name=d["name"],
            subset=d["subset"],
            data_root=d.get("data_root", "data"),
            max_samples=d.get("max_samples"),
            overwrite=d.get("overwrite", False),
            image_size=d.get("image_size"),
        )


@dataclass
class ModelConfig:
    """
    Identifies the VLM backend and its vLLM engine parameters.

    model_id is passed directly to build_model_config(), which uses substring
    matching ("qwen"+"vl", "intern"+"vl", "llava") to pick the right runner.
    """
    model_id: str                               # HuggingFace model path / local dir
    max_tokens: int = 8192                      # max new tokens per generation
    max_model_len: Optional[int] = None         # vLLM context window (None = auto)
    tensor_parallel_size: Optional[int] = None  # None = set by build_model_config()
    batch_size: int = 8

    # QwenVL-specific — ignored by InternVL and Llava runners
    max_num_frames: int = 32
    video_min_pixels: int = 256 * 28 * 28       # 200 704
    video_max_pixels: int = 2048 * 28 * 28      # 1 605 632

    @classmethod
    def from_dict(cls, d: dict) -> "ModelConfig":
        return cls(
            model_id=d["model_id"],
            max_tokens=d.get("max_tokens", 8192),
            max_model_len=d.get("max_model_len"),
            tensor_parallel_size=d.get("tensor_parallel_size"),
            batch_size=d.get("batch_size", 8),
            max_num_frames=d.get("max_num_frames", 32),
            video_min_pixels=d.get("video_min_pixels", 256 * 28 * 28),
            video_max_pixels=d.get("video_max_pixels", 2048 * 28 * 28),
        )

    def to_builder_kwargs(self) -> dict:
        """Return only the kwargs accepted by build_model_config()."""
        return dict(
            max_tokens=self.max_tokens,
            max_model_len=self.max_model_len,
            max_num_frames=self.max_num_frames,
            video_min_pixels=self.video_min_pixels,
            video_max_pixels=self.video_max_pixels,
        )


@dataclass
class EvaluationConfig:
    """Controls which evaluator runs after inference and what it measures."""

    # vqa            → accuracy + F1  (choice-based subsets)
    # damage_assessment → accuracy + F1 per damage level
    # captioning     → BLEU / ROUGE   (caption + recovery subsets)
    task: str
    metrics: List[str] = field(default_factory=lambda: ["accuracy", "f1"])
    results_dir: str = "results"       # results/{subset}/{model_id}/
    save_predictions: bool = True      # write finished.jsonl + finished.json

    VALID_TASKS = {"vqa", "damage_assessment", "captioning"}

    @classmethod
    def from_dict(cls, d: dict) -> "EvaluationConfig":
        return cls(
            task=d["task"],
            metrics=d.get("metrics", ["accuracy", "f1"]),
            results_dir=d.get("results_dir", "results"),
            save_predictions=d.get("save_predictions", True),
        )


@dataclass
class MLflowConfig:
    tracking_uri: str = "http://localhost:5000"
    experiment_name: str = "disaster-vlm-eval"

    @classmethod
    def from_dict(cls, d: dict) -> "MLflowConfig":
        return cls(
            tracking_uri=d.get("tracking_uri", "http://localhost:5000"),
            experiment_name=d.get("experiment_name", "disaster-vlm-eval"),
        )


@dataclass
class WandbConfig:
    project: str = "disaster-vlm-eval"
    entity: str = ""

    @classmethod
    def from_dict(cls, d: dict) -> "WandbConfig":
        return cls(
            project=d.get("project", "disaster-vlm-eval"),
            entity=d.get("entity", ""),
        )


@dataclass
class TrackingConfig:
    """Experiment tracking backend configuration."""
    backend: str = "mlflow"           # mlflow | wandb | none
    mlflow: MLflowConfig = field(default_factory=MLflowConfig)
    wandb: WandbConfig = field(default_factory=WandbConfig)
    log_artifacts: bool = True        # upload prediction files
    log_system_metrics: bool = True   # GPU memory, runtime

    VALID_BACKENDS = {"mlflow", "wandb", "none"}

    @classmethod
    def from_dict(cls, d: dict) -> "TrackingConfig":
        return cls(
            backend=d.get("backend", "mlflow"),
            mlflow=MLflowConfig.from_dict(d.get("mlflow", {})),
            wandb=WandbConfig.from_dict(d.get("wandb", {})),
            log_artifacts=d.get("log_artifacts", True),
            log_system_metrics=d.get("log_system_metrics", True),
        )


# ─────────────────────────────────────────────────────────────────────────────
# Root config
# ─────────────────────────────────────────────────────────────────────────────

@dataclass
class Config:
    """
    Top-level configuration object.  One instance per YAML file.

    Attributes mirror the four top-level YAML sections:
        experiment / dataset / model / evaluation / tracking
    """
    experiment: ExperimentConfig
    dataset: DatasetConfig
    model: ModelConfig
    evaluation: EvaluationConfig
    tracking: TrackingConfig

    @classmethod
    def from_dict(cls, d: dict) -> "Config":
        return cls(
            experiment=ExperimentConfig.from_dict(d["experiment"]),
            dataset=DatasetConfig.from_dict(d["dataset"]),
            model=ModelConfig.from_dict(d["model"]),
            evaluation=EvaluationConfig.from_dict(d["evaluation"]),
            tracking=TrackingConfig.from_dict(d["tracking"]),
        )

    def validate(self) -> None:
        """
        Raise ValueError for any field whose value is not in the allowed set.
        Call this right after load_config() to catch typos early.
        """
        if self.dataset.subset not in ExperimentConfig.VALID_SUBSETS:
            raise ValueError(
                f"Unknown dataset.subset '{self.dataset.subset}'. "
                f"Valid options: {sorted(ExperimentConfig.VALID_SUBSETS)}"
            )

        if self.evaluation.task not in EvaluationConfig.VALID_TASKS:
            raise ValueError(
                f"Unknown evaluation.task '{self.evaluation.task}'. "
                f"Valid options: {sorted(EvaluationConfig.VALID_TASKS)}"
            )

        if self.tracking.backend not in TrackingConfig.VALID_BACKENDS:
            raise ValueError(
                f"Unknown tracking.backend '{self.tracking.backend}'. "
                f"Valid options: {sorted(TrackingConfig.VALID_BACKENDS)}"
            )


# ─────────────────────────────────────────────────────────────────────────────
# Public loader
# ─────────────────────────────────────────────────────────────────────────────

def load_config(path: str | Path, validate: bool = True) -> Config:
    """
    Parse a YAML config file and return a fully typed Config object.

    Parameters
    ----------
    path : str | Path
        Path to the YAML config file.
    validate : bool
        If True (default), run Config.validate() before returning.

    Returns
    -------
    Config

    Example
    -------
        cfg = load_config("configs/disasterm3_qwen_vqa.yaml")
        print(cfg.model.model_id)
    """
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"Config file not found: {path}")

    with open(path, "r") as f:
        raw = yaml.safe_load(f)

    cfg = Config.from_dict(raw)

    if validate:
        cfg.validate()

    return cfg