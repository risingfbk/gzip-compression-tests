# On Exploiting `gzip`’s Content-Dependent Compression

This repository contains a small side project developed during research on Kubernetes and `containerd` security.

It aims to investigate the behaviour of the `gzip` program when random data is fed to it. Indeed, due to how the DEFLATE algorithm is implemented, different types of random data generated with different tools result in different output size, compression time, and decompression time.

The repository contains the following files:

- `report.pdf` - the report
- `src`
  - `generate-od.sh` and `generate.sh` - Bash scripts for automatically generating the files 
  - `execute.sh` - Bash script for automating the tests described in the report
  - `time.sh` - companion script that monitors whenever gzip is invoked
  - `parse_results.py` and `automate_parse_results.sh` - scripts that generate automatic images (and LaTeX files) from the results
- `results` - the results of our findings

## Authors

- [Luis Augusto Dias Knob](https://github.com/luisdknob), Fondazione Bruno Kessler - `l.diasknob@fbk.eu`
- [Matteo Franzil](https://github.com/mfranzil), Fondazione Bruno Kessler - `mfranzil@fbk.eu`
