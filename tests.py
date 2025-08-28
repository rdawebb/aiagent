# import run_python_file function
from functions.run_python import run_python_file

# test run_python_file function
def tests():
    print(f"Result of test case 1: \n{run_python_file("calculator", "main.py")}") # test case 1
    print(f"Result of test case 2: \n{run_python_file("calculator", "main.py", ["3 + 5"])}") # test case 2
    print(f"Result of test case 3: \n{run_python_file("calculator", "tests.py")}") # test case 3
    print(f"Result of test case 4: \n{run_python_file("calculator", "../main.py")}") # test case 4
    print(f"Result of test case 5: \n{run_python_file("calculator", "nonexistent.py")}") # test case 5

# run tests
if __name__ == "__main__":
    tests()
