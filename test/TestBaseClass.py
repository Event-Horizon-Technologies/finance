import inspect
import os
from pathlib import Path
import pickle

from finance import Utils

GENERATE_PICKLES = os.environ.get("MODE") == Utils.PICKLE_GENERATION_MODE

class TestBaseClass:
    def run(self, **kwargs):
        test_dir_path = Path(__file__).parent
        test_class = self.__class__.__name__
        test_case = str(inspect.currentframe().f_back.f_code.co_name)
        pickle_jar_path = test_dir_path.joinpath(test_class).joinpath(test_case)

        for name, var in kwargs.items():
            pickle_path = os.path.join(pickle_jar_path, f"{name}.pickle")
            if GENERATE_PICKLES:
                pickle_jar_path.mkdir(parents=True, exist_ok=True)
                with open(pickle_path, "wb") as f:
                    pickle.dump(var, f)
            else:
                try:
                    with open(pickle_path, "rb") as f:
                        assert var == pickle.load(f)
                except FileNotFoundError: raise FileNotFoundError(
                    f"No pickle file associated with test class: '{test_class}', test case: '{test_case}', "
                    f"and variable: '{name}'.\n"
                    f"NOTE: Run 'generate_pickles.py' to create pickles for the current functionality."
                )