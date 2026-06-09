
import json
from pathlib import Path
from .base import BaseDataset
# loading the dataset is very easy the trick will be in mapping the dataset \
# to the format we want for training and evaluation.
# I didn't implement the mapping for the lack of time, I would need to understand more 
# about the field
# I tested this code on a sample of the dataset that I downloaded using the 
# get_monitrs_sample.py script, and it works fine,
# it loads the data and prints the first 5 samples and the id and conversations of the first 10 samples.
class MONITRSDataset(BaseDataset):
    def __init__(self , subset , finish_ids):
        super().__init__()
        self.subset = subset
        self.finish_ids = finish_ids

    def load(self):
        PROJECT_ROOT = Path(__file__).resolve().parent.parent.absolute()
        print("PROJECT_ROOT: {}".format(PROJECT_ROOT))
        subset_json = PROJECT_ROOT / "monitrs_sample" / f"monitrs_test_first_100.json"
        print("Reading data from {}".format(subset_json))
        with open(subset_json, "r") as f:
            ds = json.load(f)
            ds = [data_dict for data_dict in ds if data_dict["id"] not in self.finish_ids]

        return ds
