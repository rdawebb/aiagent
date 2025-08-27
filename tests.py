# import get_file_content function
from functions.get_file_content import get_file_content

# test get_file_content function
def tests():
    print(f"Result for test case 1: \n{get_file_content("calculator", "main.py")}") # test case 1
    print(f"Result for test case 2: \n{get_file_content("calculator", "pkg/calculator.py")}") # test case 2
    print(f"Result for test case 3: \n{get_file_content("calculator", "/bin/cat")}") # test case 3
    print(f"Result for test case 4: \n{get_file_content("calculator", "pkg/does_not_exist.py")}") # test case 4

# run tests
if __name__ == "__main__":
    tests()
