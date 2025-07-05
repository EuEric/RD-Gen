# RD-Gen
<!-- <p align="center">
  <img src="https://user-images.githubusercontent.com/55824710/208731888-be3e320a-4148-46cc-983c-f8ee6fe27b9d.png" width="300px">&emsp;&emsp;&emsp;&emsp;<img src="https://user-images.githubusercontent.com/55824710/228999914-af1f5be9-fffe-4b3b-b988-76379389f46b.png" width="420px">
</p>
<p align="center">
  <img src="https://img.shields.io/badge/-Python-F9DC3E.svg?logo=python&style=flat">
  <img src="https://img.shields.io/badge/-Github-black.svg?logo=github&style=flat"><img src="https://img.shields.io/badge/-pytest passing-gleen.svg">
</p> -->

## About
This code represents a fork of **RD-Gen** from https://github.com/azu-lab/RD-Gen. The tool is used for generating random DAGs using different input parameters. The original fork contains the following functionalities:
- **Leverage existing random DAG generation methods:**, Fan-in/Fan-out [1] and G(n, p) [2] methods.
- Create a new **Chain-based method** to generate chain-based multi-rate DAGs.
- Automatically generate batches of random DAGs using input files.

Our modifications extend the functionalities to also include:
- Ray DAGs: Generate Ray DAGs using a 'ForkJoin' method.

## Compiling
To start, run the following bash program (from the root of the project):
```bash
$ ./setup.bash
```

This bash script will install the necessary Python libraries to run the code.

## Modifications

Our code created a new generation method called **ForkJoin**.
### Input files

A sample config file explaining how this can be used is in `sample_config/fork_join/ray_fork_join.yaml`. This method adds the following **new** parameters:
- **Number of source nodes:** Specify the number of source nodes. For Ray DAGs this value should be *1**.
- **Number of sink nodes:** Specify the number of sink nodes. For Ray DAGs this value should be *1**.
- **Fork-depth:** Determines the depth of forks.
- **Nr-fork:** Determines the **maximum** number of children per fork. For each fork, a random value in the range [1, Nr-fork] will be chosen.
- **Early-termination-prob:** Determines the probability of a path terminating early, meaning that such a path won't reach the depth determined by the **Fork-depth** value.
- **Graph-deadline:** To be specified in conjunction with **Graph-period**, but never with **Graph-utilization**. This value specifies the deadline of a DAG.
- **Graph-period:** To be specified in conjunction with **Graph-deadline**, but never with **Graph-utilization**. This value specifies the period of a DAG.
- **Graph-utilization:** This value specifies the utilization of a graph, by setting the **period** equals to the **deadline**, and computing the **volume** of a graph. Never use this value in conjuction with **Graph-deadline** or **Graph-period**.
- **Ensure weakly connected:** This value does nothing and should be removed in the future.

All these variables are based on the usage from the fork, meaning that they use the same format and data types as the original code. [See Documents section](#documents). Specifically, check the [wiki](https://github.com/azu-lab/RD-Gen/wiki) for a full usage guide for the variables.




## Running application

To run the application call `python run_generator.py`.
To run any config file, use the `-c` variable, followed by the respective location. For example:


### Fork Join (Ray DAGs)
`$ python3 run_generator.py -c ./sample_config/fork_join/ray_fork_join.yaml`

## Documents
- [wiki](https://github.com/azu-lab/RD-Gen/wiki)
- [API list (for developer)](https://azu-lab.github.io/RD-Gen/)
- RD-Gen is presented in the following paper:
  - A. Yano and T. Azumi, "RD-Gen: Random DAG Generator Considering Multi-rate Applications for Reproducible Scheduling Evaluation", the 26th IEEE International Symposium on Real-Time Distributed Computing (ISORC), 2023
  
    <details>
    <summary>BibTeX</summary>

    ```bibtex
    @inproceedings{RD-Gen,
      title={{RD-Gen}: Random {DAG} Generator Considering Multi-rate Applications for Reproducible Scheduling Evaluation},
      author={Atsushi, Yano and Takuya, Azumi},
      booktitle={Proceedings of the 26th IEEE International Symposium on Real-Time Distributed Computing (ISORC)},
      year={2023},
      organization={IEEE}
    }
    ```

    </details>

## References
- [1] R. P. Dick, D. L. Rhodes, and W. Wolf. TGFF: task graphs for free. In Proc. of Workshop on CODES/CASHE, 1998.
- [2] Daniel Cordeiro, Gregory Mounie, Swann Perarnau, Denis Trystram, Jean-Marc Vincent, and Frederic Wagner. Random graph generation for scheduling simulations. In Proc. of SIMUTools, 2010.
