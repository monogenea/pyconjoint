''' PyConjoint module '''

import os
import re
import json
import numpy as np
import pandas as pd
from datetime import datetime

class PyConjoint():
    def __init__(self, json_config="config.json"):
        """Initialize PyConjoint object.
        
        Args:
            json_config: Path to JSON configuration file
        """
        with open(json_config) as f:
            config = json.load(f)
        self.study_name = config["study_name"]
        self.attrlevels = config["attrlevels"]
        self.n_tasks = config["n_tasks"]
        self.n_concepts = config["n_concepts"]
        self.n_versions = config["n_versions"]
        self.none_option = config["none_option"]
    
    def create_study(self):
        """Create study directory.
        
        Returns:
            Path to study directory
        """
        std_study_name = re.sub(pattern="[^a-z0-9]", repl="_", string=self.study_name.lower())
        folder_name = datetime.now().strftime(f"%Y%m%d_{std_study_name}")
        study_folder = os.path.join(os.getcwd(), "studies/" + folder_name)
        print(f"Study folder created: {study_folder}")
        os.makedirs(study_folder, exist_ok=True)
        self.study_folder = study_folder
        self.folder_created = True

    def create_design(self, method="random", seed=999):
        """Generate experimental design for conjoint analysis.
        
        Args:
            method: Design method ("random" or "orthogonal")
            seed: Random seed for reproducibility
            
        Returns:
            DataFrame with experimental design
        """
        np.random.seed(seed)
        design_list = []
        for version in range(1, self.n_versions + 1):
            for task in range(1, self.n_tasks + 1):
                for concept in range(1, self.n_concepts + 1):
                    specs = {"version": version, "task": task, "concept": concept}
                    if method == "random":
                        profile = {attr: np.random.choice(len(levels)) + 1 for attr, levels in self.attrlevels.items()}
                    elif method == "orthogonal":
                        profile = {attr: ((concept + task + version) % len(levels)) + 1 for attr, levels in self.attrlevels.items()}
                    specs.update(profile)
                    design_list.append(specs)
                # If none option is enabled, add a dummy concept for the none option
                if self.none_option:
                    specs = {"version": version, "task": task, "concept": self.n_concepts + 1}
                    specs.update({attr: 0 for attr in self.attrlevels.keys()})
                    design_list.append(specs)
        design_df = pd.DataFrame(design_list)
        # Write design to study directory
        if self.folder_created:
            design_df.to_csv(os.path.join(self.study_folder, "design.csv"), index=False)
        self.design = design_df
    
    def simulate_response(self, driver_attr=None, n_resp=10, seed=999):
        """Simulate respondent choices based on design.
        
        Args:
            n_resp: Number of respondents to simulate
            seed: Random seed for reproducibility
            
        Returns:
            DataFrame with simulated responses
        """
        assert self.design is not None, "User must generate design first"
        np.random.seed(seed)
        if not driver_attr:
            driver_attr = np.random.choice(list(self.attrlevels.keys()))
        versions = np.random.choice(range(1, self.n_versions + 1), size=n_resp)
        pop_choices = []
        for i in range(n_resp):
            resp_choices = []
            for task in range(1, self.n_tasks + 1):
                idx = (self.design["task"] == task) & (self.design["version"] == versions[i])
                choice = int(self.design.loc[idx, driver_attr].argmax()) + 1
                resp_choices.append(choice)
            pop_choices.append(resp_choices)
        pop_choices_df = pd.DataFrame(pop_choices,
                                      index=[f"respid_{i}" for i in range(1, n_resp + 1)],
                                      columns=[f"task_{j}" for j in range(1, self.n_tasks + 1)])
        if self.folder_created:
            pop_choices_df.reset_index().to_csv(os.path.join(self.study_folder, "response_sim.csv"), index=False)
        self.response = pop_choices_df
    