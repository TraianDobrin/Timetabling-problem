import Encoding
def read_numbers_from_file(file_path):
    numbers = []
    try:
        with open(file_path, 'r') as file:
            for line in file:
                # Split the line by whitespace and convert each part to a number
                # Assuming each line contains numbers separated by spaces
                for part in line.split():
                    numbers.append(int((part))  )# Use int(part) if you want integers
    except FileNotFoundError:
        print(f"File {file_path} not found.")
    except ValueError:
        print("File contains non-numeric data.")
    return numbers
numbers=read_numbers_from_file('assignment.txt')
ans=[]
for x in numbers:
    for key, value in Encoding.S.items():
        if abs(x) in value:
            ans.append(x)
            print(x)
            break
print(len(ans))
with open('file.txt', 'w') as file:
        for number in ans:
            file.write(str(number) + ' ')