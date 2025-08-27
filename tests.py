# import write_file function
from functions.write_file import write_file

# test write_file function
def tests():
    print(f"Result of test case 1: \n{write_file("calculator", "lorem.txt", "wait, this isn't lorem ipsum")}") # test case 1
    print(f"Result of test case 2: \n{write_file("calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet")}") # test case 2
    print(f"Result of test case 3: \n{write_file("calculator", "/tmp/temp.txt", "this should not be allowed")}") # test case 3

# run tests
if __name__ == "__main__":
    tests()
