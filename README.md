# On Exploiting `gzip`’s Content-Dependent Compression

This repository contains a small side project developed during the *Exploiting Kubernetes' Image Pull Implementation to Deny Node Availability* research effort, whose code is available [here](https://github.com/risingfbk/magi).

It aims to investigate the behaviour of the `gzip` program when random data is fed to it. Indeed, due to how the DEFLATE algorithm is implemented, different types of random data generated with different tools result in different output size, compression time, and decompression time.

The repository contains the following files:

- `report.pdf` - the report
- `src`
  - `generate-od.sh` and `generate.sh` - Bash scripts for automatically generating the files 
  - `execute.sh` - Bash script for automating the tests described in the report
  - `time.sh` - companion script that monitors whenever gzip is invoked
  - `parse_results.py` and `automate_parse_results.sh` - scripts that generate automatic images (and LaTeX files) from the results
- `results` - the results of our findings

## License

This software is licensed under the Apache 2.0 license. See [LICENSE](LICENSE) for more details.

## Contributing

All contributions are welcome. If you have any doubts or questions feel free to open an issue or contact the maintainers.

## Acknowledgements

This work was partially supported by project SERICS (PE00000014), MUR National Recovery and Resilience Plan funded by the European Union - NextGenerationEU, and by project FLUIDOS (grant agreement No 101070473), European Union’s Horizon Europe Programme.

The author list is the following:

- [Luis Augusto Dias Knob](https://github.com/luisdknob), Fondazione Bruno Kessler - `l.diasknob@fbk.eu`
- [Matteo Franzil](https://github.com/mfranzil), Fondazione Bruno Kessler - `mfranzil@fbk.eu`
- Domenico Siracusa, Fondazione Bruno Kessler - `dsiracusa@fbk.eu`

If you wish to cite this work for scientific research, do it as follows:

> L. A. D. Knob, M. Franzil, and D. Siracusa, “Exploiting Kubernetes’ Image Pull Implementation to Deny Node Availability.” arXiv. Preprint available: http://arxiv.org/abs/2401.10582. [Accessed: Jan. 23, 2024]
