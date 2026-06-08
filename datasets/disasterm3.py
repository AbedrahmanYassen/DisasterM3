


import json
from ntpath import join
from pathlib import Path

from pyscripts.run_vllm import PROJECT_ROOT
from .base import BaseDataset

class DisasterM3Dataset(BaseDataset):
    def __init__(self , subset , finish_ids):
        super().__init__()
        self.subset = subset
        self.finish_ids = finish_ids

    def load(self):
        PROJECT_ROOT = Path(__file__).resolve().parent.parent.absolute()
        print("PROJECT_ROOT: {}".format(PROJECT_ROOT))
        subset_json = PROJECT_ROOT / "data" / f"{self.subset}.json"
        print("Reading data from {}".format(subset_json))
        with open(subset_json, "r") as f:
            ds = json.load(f)
            ds = [dict(id=f"{self.subset}_{data_idx}", **data_dict) for data_idx, data_dict in enumerate(ds)]
            ds = [data_dict for data_dict in ds if data_dict["id"] not in self.finish_ids]

        return ds
