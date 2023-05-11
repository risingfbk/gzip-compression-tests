import matplotlib.pyplot as plt
import matplotlib as mpl
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
    
def convert_to_prefix(number: float):
    if number < 1000:
        return f'{number:.0f}'
    elif number < 1000000:
        return f'{number/1000:.0f}k'
    elif number < 1000000000:
        return f'{number/1000000:.0f}M'
    else:
        return f'{number/1000000000:.0f}G'

mapper = {
    1: './lorem/lorem -c 1000000000',
    2: 'head -c 1G /dev/urandom',
    3: 'od --format=x /dev/urandom',
    4: 'base64 /dev/urandom | head -c 1G',
    5: "cat /dev/urandom | tr -dc 'a-zA-Z0-9' | head -c 1G",
    6: 'openssl rand -out myfile \$(echo 1G | numfmt --from=iec)'
    }

style = {
    1: 'solid',
    2: 'solid',
    3: 'solid',
    4: 'solid',
    5: 'solid',
    6: 'solid'   
}

cmap = plt.get_cmap('tab10')

colours = {
    1: cmap(0),
    2: cmap(1),
    3: cmap(3),
    4: cmap(2),
    5: cmap(4),
    6: cmap(5)
}

formats = ["x", "a", "c", "d1", "d2", "d4", "d8", "f", "o", "u1", "u2", "u4", "u8"]
for i in range(13, 26):
    mapper[i] = f'od --format={formats[i-13]} /dev/urandom'
    style[i] = 'solid'

style[17] = style[23] = 'dotted'
style[18] = style[24] = 'dashed'
style[19] = style[25] = 'dashdot'
style[20] = 'dashdot'

colours[13] = cmap(3)
colours[14] = cmap(8)
colours[15] = cmap(9)
colours[16] = colours[17] = colours[18] = colours[19] = cmap(6)
colours[20] = cmap(0)
colours[21] = cmap(2)
colours[22] = colours[23] = colours[24] = colours[25] = cmap(7)


argparser = argparse.ArgumentParser()
argparser.add_argument('--path', type=str, default='results.csv')
argparser.add_argument('--pgf', dest='pgf', action='store_true')
argparser.add_argument('--od', dest='od', action='store_true')

args = argparser.parse_args()

if args.pgf:
    mpl.use("pgf")
    mpl.rcParams.update({
        "pgf.texsystem": "pdflatex",
        'font.family': 'serif',
        'text.usetex': True,
        'pgf.rcfonts': False,
    })
    EXT="pgf"
else:
    EXT="png"

if not os.path.exists(args.path):
    raise ValueError('Given path does not exist')

with open(args.path, 'r') as f:
    lines = f.readlines()

# data = pd.read_csv('results.csv', columns=["function","level","size_uncompressed","compression_time","size_compressed","decompression_time"])
# data.function
# data.plot(x='level', y='decompression_time')
# exit(1)

functions = set()
for line in lines:
    fc, *_ = line.split(',')
    fc = int(fc.strip())
    functions.add(fc)

compr_time = {fc: {level: [] for level in range(1, 10)} for fc in functions}
decompr_time = {fc: {level: [] for level in range(1, 10)} for fc in functions}
uncompressed = {fc: {level: [] for level in range(1, 10)} for fc in functions}
compressed = {fc: {level: [] for level in range(1, 10)} for fc in functions}

print(compr_time)

for line in lines:
    fc, level, unc, ctime, com, dtime = line.split(',')
    fc = int(fc.strip())
    level = int(level.strip())
    try:
        ctime = float(ctime.strip())
        compr_time[fc][level].append(ctime)
    except:
        pass
    try:
        dtime = float(dtime.strip())
        decompr_time[fc][level].append(dtime)
    except:
        pass
    if unc != '':
        unc = convert_from_prefix(unc.strip())
        uncompressed[fc][level].append(unc)
    if com != '':
        com = convert_from_prefix(com.strip())
        compressed[fc][level].append(com)
 
print(decompr_time)

res = {}
means = {}
for fc in decompr_time:
    mean = np.mean([np.mean(decompr_time[fc][x]) for x in decompr_time[fc]])
    mean_6 = np.mean(decompr_time[fc][6])
    std = np.mean([np.std(decompr_time[fc][x]) for x in decompr_time[fc]])
    res[mean_6] = f'{mapper[fc]}: {mean:.3f} +- {std:.3f} (x6: {mean_6:.3f})'
    means[fc] = mean_6
    # plt.annotate(f'{mean:.3f} +- {std:.3f}', (list(func[fc].keys())[-1], mean))

# print sorted by key
print("\n".join([res[x] for x in sorted(res, reverse=True)]))
decompr_time = {k: v for k, v in sorted(decompr_time.items(), key=lambda item: means[item[0]], reverse=True)}

with open(f'{args.path.split(".")[0]}.tex', 'w') as f:
    for fc in decompr_time:
        for x in decompr_time[fc]:
            f.write(f"{mapper[fc]} & {x} & {convert_to_prefix(np.mean(uncompressed[fc][x]))} & {convert_to_prefix(np.mean(compressed[fc][x]))} & {np.mean(compr_time[fc][x]):.3f} & {np.mean(decompr_time[fc][x]):.3f} \\\\\n")

func = decompr_time

if args.pgf:
    plt.figure(figsize=(3.25949, 3.95949))
    plt.tight_layout(pad=0.1)
else:
    plt.figure(figsize=(10, 10))
for fc in func:
    if args.pgf:
        if args.od:
            label = mapper[fc].split("=")[1].split("/")[0].strip()
        else:
            label = mapper[fc][:40] + '...' if len(mapper[fc]) > 40 else mapper[fc]
            # label = label.split("]")[1].strip()
    else:
        label = mapper[fc]
        # label = label.split("]")[1].strip()
    plt.plot(func[fc].keys(), [np.mean(func[fc][x]) for x in func[fc]], label=label, ls=style[fc], color=colours[fc])

if args.pgf:
    # Put the legend out of the figure, down below
    cols = 4 if args.od else 1
    lgd = plt.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc='lower left', ncol=cols, mode="expand", borderaxespad=0.,
                     fontsize=7)
else:
    lgd = plt.legend()

plt.xlabel('gzip compression level')
plt.ylabel('decompression time (s)')
plt.xticks([1, 2, 3, 4, 5, 6, 7, 8, 9])

# draw a dashed line at place 6
plt.axvline(x=6, color='k', linestyle='--', alpha=0.5)

if args.pgf:
    plt.savefig(args.path.replace('.csv', f'.{EXT}'), bbox_inches='tight', bbox_extra_artists=(lgd,))
else:
    plt.savefig(args.path.replace('.csv', f'.{EXT}'))

