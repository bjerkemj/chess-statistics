from difflib import Differ

with open('Stockfish_15_64-bit.commented.[2600].pgn', 'r') as file:
    lines1 = file.readlines()
          
          
with open("./tests/saveTestGames.pgn", 'r') as file2:
    lines2 = file2.readlines()

file1 = open('Stockfish_15_64-bit.commented.[2600].pgn','r')
file2 = open("./tests/saveTestGames.pgn",'r')
# file2 = open('Stockfish_15_64-bit.commented.[2600]2.pgn','r')

file1_lines = file1.readlines()
file2_lines = file2.readlines()

print(f'file1 max line length =', max([len(line) for line in file1_lines]))
print(f'file2 max line length =', max([len(line) for line in file2_lines]))

index = 413

print('index =', index)
print('line1 length', len(file1_lines[index]))
print('line2 length', len(file2_lines[index]))
print('@@@@')
for i in range(len(file1_lines[index])):
    print(file1_lines[index][i])

print('line1', file1_lines[index])
print('line2', file2_lines[index])

index = 412
print('index =', index)
print('line1 length', len(file1_lines[index]))
print('line2 length', len(file2_lines[index]))

print('line1', file1_lines[index])
print('line2', file2_lines[index])


print('-----')
lines = []
lines_before = []
indexes = []

for i, line in enumerate(file1_lines):
    if "1/2-1/2" in line:
        lines.append(line)
        lines_before.append(line)
        indexes.append(i)

# for line in lines_before:
#     print(len(line))

print(len(lines))

print(len([line for line in lines if len(line) == 8]))

# print(len(file2_lines[618]))
# print((file2_lines[618]))

# print(len(file1_lines[619]))
# print((file1_lines[619]))

# c = 0
# for i in range(len(file1_lines)):
#     if file1_lines[i] != file2_lines[i]:
#         print("Line " + str(i+1) + " doesn't match.")
#         print("------------------------")
#         print("File1: " + file1_lines[i])
#         print("File2: " + file2_lines[i])
#         c+= 1
#         if c > 3:
#             break

file1.close()
file2.close()