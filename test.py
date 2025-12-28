''' TEST PYCONJOINT FUNCTIONALITIES '''

from src.pyconjoint import PyConjoint

cbc_obj = PyConjoint()

cbc_obj.create_study()

cbc_obj.create_design(method="random", seed=999)

cbc_obj.design

cbc_obj.simulate_response(driver_attr="price", n_resp=50, seed=999)
cbc_obj.response