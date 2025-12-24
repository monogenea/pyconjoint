''' PyConjoint class '''

import json
import numpy as np
import pandas as pd

class PyConjoint():
    def __init__(self, config_fname="config.json"):
        with open(config_fname) as f:
            config = json.load(f)
        self.attrlevels = config["attrlevels"]
        self.n_tasks = config["n_tasks"]
        self.n_concepts = config["n_concepts"]
        self.n_versions = config["n_versions"]
        self.none_option = config["none_option"]
    def design(self, method="random", seed=999):
        np.random.seed(seed)
        design_list = []
        for version in range(1, self.n_versions + 1):
            for task in range(1, self.n_tasks + 1):
                for concept in range(1, self.n_concepts + 1):
                    specs = {"version": version, "task": task, "concept": concept}
                    if method == "random":
                        profile = {attr: np.random.choice(len(levels)) + 1 for attr, levels in self.attrlevels.items()}
                    specs.update(profile)
                    design_list.append(specs)
        design_df = pd.DataFrame(design_list)
        self.design = design_df
    def response_sim(self, n_respondents=10, seed=999):
        assert self.design is not None, "User must build design first"
        np.random.seed(seed)
        driver = np.random.choice(list(self.attrlevels.keys()))
        versions = np.random.choice(range(1, self.n_versions + 1), size=n_respondents)
        pop_choices = []
        for i in range(n_respondents):
            resp_choices = []
            for task in range(1, self.n_tasks + 1):
                idx = (self.design["task"] == task) & (self.design["version"] == versions[i])
                choice = int(self.design.loc[idx, driver].argmax()) + 1
                resp_choices.append(choice)
            pop_choices.append(resp_choices)
        pop_choices_df = pd.DataFrame(pop_choices,
                                      index=[f"respid_{i}" for i in range(1, n_respondents + 1)],
                                      columns=[f"task_{j}" for j in range(1, self.n_tasks + 1)])
        self.response = pop_choices_df
            