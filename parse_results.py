import matplotlib.pyplot as plt
import numpy as np
import os
import argparse
# import pandas as pd

def convert_from_prefix(number: str):
    number = number.lower().strip()
    if number[-1] == 'k':
        return float(number[:-1]) * 1000
    elif number[-1] == 'm':
        return float(number[:-1]) * 1000000
    elif number[-1] == 'g':
        return float(number[:-1]) * 1000000000
    else:
        return float(number)

mapper = {
    '1': '[1] ./lorem/lorem -c 1000000000',
    '2': '[2] head -c 1G /dev/urandom',
    '3': '[3] od --format=x /dev/urandom',
    '4': '[4] base64 /dev/urandom | head -c 1G',
    '5': "[5] cat /dev/urandom | tr -dc 'a-zA-Z0-9' | head -c 1G",
    '6': '[6] openssl rand -out myfile "$( echo 1G | numfmt --from=iec )"'
    }

formats = ["x1", "x2", "x4", "x8", "a", "c", "d1", "d2", "d4", "d8", "f", "o", "u1", "u2", "u4", "u8"]
for i in range(10, 26):
    mapper[str(i)] = f'[{str(i)}] od --format={formats[i-10]} /dev/urandom'

argparser = argparse.ArgumentParser()
argparser.add_argument('--path', type=str, default='results.csv')
args = argparser.parse_args()

# Path: results.csv
with open('results.csv', 'r') as f:
    lines = f.readlines()

# data = pd.read_csv('results.csv', columns=["function","level","size_uncompressed","compression_time","size_compressed","decompression_time"])
# data.function
# data.plot(x='level', y='decompression_time')
# exit(1)

func = {}
for line in lines:
    fc, x, _, _, _, y = line.split(',')
    if fc not in func:
        func[fc] = {}
    x = float(x.strip())
    if x not in func[fc]:
        func[fc][x] = []
    func[fc][x].append(convert_from_prefix(y))
 
print(func)

plt.figure(figsize=(10, 10))
for fc in func:
    plt.plot(func[fc].keys(), [np.mean(func[fc][x]) for x in func[fc]], label=mapper[fc])
plt.legend()
plt.xlabel('gzip compression level')
plt.ylabel('decompression time (s)')

res = {}
for fc in func:
    mean = np.mean([np.mean(func[fc][x]) for x in func[fc]])
    mean_6 = np.mean(func[fc][6])
    std = np.mean([np.std(func[fc][x]) for x in func[fc]])
    res[mean_6] = f'{mapper[fc]}: {mean:.3f} +- {std:.3f} (x6: {mean_6:.3f})'
    # plt.annotate(f'{mean:.3f} +- {std:.3f}', (list(func[fc].keys())[-1], mean))

# print sorted by key
print("\n".join([res[x] for x in sorted(res, reverse=True)]))
plt.savefig('results.png')

