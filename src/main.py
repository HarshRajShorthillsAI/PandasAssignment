
from etl_pipeline import ETLPipeline
import gc
import pandas as pd

class Main:

    @classmethod
    def run_pipeline(cls):
        # ETLPipeline('./Data').task3()
        # ETLPipeline('./Data').task4()
        # ETLPipeline('./Data').task5()
        ETLPipeline('./Data').task6()

if __name__ == "__main__":
    Main.run_pipeline()