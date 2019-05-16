import arguments
from comet_ml import Experiment, OfflineExperiment
import model
from pathlib import Path
import functions.param
import functions.train
import functions.cv
import functions.embed
import functions.predict
import pandas as pd
import sys
import json

import tensorflow as tf

def prerun(args, run_dir=True, exp=True):
    if run_dir:
        p = Path(args["run_dir"])
        if p.exists():
            raise ValueError("Rundir exists, please remove.")
        p.mkdir()

        with open(Path(p, "args.json"), "w") as fp:
            json.dump(args, fp)
    
    if exp:
        experiment = Experiment(
            api_key="pJ6UYxQwjYoYbCmmutkqP66ni",
            project_name=args["comet_project"],
            workspace="mlippie",
            auto_metric_logging=True,
            auto_param_logging=False,
            log_graph=True,
            disabled=True
        )

        experiment.log_parameters(args)

        return experiment
    else:
        return None


def main():
  
    args = arguments.get_args()
    
    from tensorflow.keras.backend import set_session
    config = tf.ConfigProto()
    config.gpu_options.per_process_gpu_memory_fraction = args["gpu_mem_fraction"]
    config.gpu_options.allow_growth = True
    set_session(tf.Session(config=config))

    meta = pd.read_csv(args["meta"])
        
    def summary():
        m = model.model_map(args["model"])(args)
        m.summary()

    def train():
        functions.train.run(args, meta)

    def cv():
        functions.cv.run(args, meta)

    def predict():
        functions.predict.run(args, meta)

    def param():
        functions.param.run(args, meta)

    def embed():
        functions.embed.run(args, meta)

    function_map = {
        "train": train,
        "cv": cv,
        "predict": predict,
        "summary": summary,
        "param": param,
        "embed": embed
    }
    
    function_map[args["function"]]()


if __name__ == "__main__":
    tf.enable_eager_execution()

    main()
