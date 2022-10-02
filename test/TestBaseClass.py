import inspect
import os
import pickle
from pathlib import Path

from finance import Utils

class TestBaseClass:
    IN_PICKLE_GENERATION_MODE = os.environ.get("MODE") == Utils.PICKLE_GENERATION_MODE
    IN_TESTING_MODE = os.environ.get("MODE") is None

    def run(self, **kwargs):
        for name, var in kwargs.items():
            if self.IN_PICKLE_GENERATION_MODE:
                self.store_pickle(name, var)
            else:
                rick = self.get_pickle(name)
                if rick is None:
                    raise FileNotFoundError(
                        f"No pickle file associated with test class: '{self.test_class}', "
                        f"test case: '{self.test_case}', and variable: '{name}'.\n"
                        f"NOTE: Run 'generate_pickles.py' to create pickles for the current functionality."
                    )
                assert var == rick, f"'{name}' data did not match pickle data"

    @property
    def test_dir_path(self):
        return Path(__file__).parent

    @property
    def test_class(self):
        return self.__class__.__name__

    @property
    def test_case(self):
        stack = inspect.stack()
        for i in range(1, len(stack)):
            function = stack[i].function
            if function.startswith("test_"):
                return function
        return None

    @property
    def pickle_jar_path(self):
        return self.test_dir_path.joinpath(self.test_class).joinpath(self.test_case)

    def get_pickle_path(self, name):
        return self.pickle_jar_path.joinpath(f"{name}.pickle")

    def get_pickle(self, name):
        try:
            with open(self.get_pickle_path(name), "rb") as f:
                return pickle.load(f)
        except FileNotFoundError:
            return None
        
    def store_pickle(self, name, var):
        self.pickle_jar_path.mkdir(parents=True, exist_ok=True)
        with open(self.get_pickle_path(name), "wb") as f:
            pickle.dump(var, f)
