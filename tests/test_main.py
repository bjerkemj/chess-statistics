import os
# RUN FROM FOLDER chess-statistics
if __name__ == '__main__':
    path = os.path.dirname(os.path.abspath(__file__))
    for file in os.listdir(path):
        if 'main' not in file and file.endswith('.py') and 'test' in file:
            print('Running testfile', file)
            os.system(f'python {os.path.join(path,file)}')

    print('ALL TESTS PASSED')