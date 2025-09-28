from functions.run_python_file import run_python_file

def tests():
    print(f"Result of test case 1: \n{run_python_file("calculator", "main.py")}")
    print(f"Result of test case 2: \n{run_python_file("calculator", "main.py", ["3 + 5"])}")
    print(f"Result of test case 3: \n{run_python_file("calculator", "tests.py")}")
    print(f"Result of test case 4: \n{run_python_file("calculator", "../main.py")}")
    print(f"Result of test case 5: \n{run_python_file("calculator", "nonexistent.py")}")

if __name__ == "__main__":
    tests()
