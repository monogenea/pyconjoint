''' TEST PYCONJOINT FUNCTIONALITIES '''

from src.pyconjoint import PyConjoint

cbc_obj = PyConjoint()

cbc_obj.design(method="random", seed=999)

cbc_obj.design

cbc_obj.response_sim(n_respondents=50, seed=999)
cbc_obj.response