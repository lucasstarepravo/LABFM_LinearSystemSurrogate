# LABFM_LinearSystemSurrogate

LABFM_LinearSystemSurrogate is a project that implements pretrained neural networks to surrogate the linear system of the Laplace operator in the local anisotropic basis function method (LABFM). The intended application is to conduct a convergence analysis of the results obtained with the neural networks, evaluating the quality of these results.

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Requirements](#requirements)
- [Customization](#customization)


## Features

- **Pretrained Neural Networks:** Implements neural networks that surrogate the linear system of the Laplace operator in LABFM.
- **Convergence Analysis:** Designed to facilitate convergence analysis to assess the quality of the surrogate results.
- **Object-Oriented Design:** Developed using object-oriented programming for modularity and ease of maintenance.
- **Flexible Model Importing:** Change the imported ML model in `functions.discrete_operator` as needed.
- **Domain Resolution Control:** The `total_nodes_list` parameter allows you to adjust the domain resolution, while `polynomial_list` should remain unchanged.

## Installation

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/lucasstarepravo/LABFM_LinearSystemSurrogate.git
   ```
2. **Install Dependencies:**
     ```bash
     pip install -r requirements.txt
     ```
     
## Usage

The main entry point is `main.py`. This script requires the following input parameters:

- **total_nodes_list:** A list controlling the resolution of the domain (e.g., `[10, 20, 50, 100, 200, 400]`).
- **polynomial_list:** A list of polynomial degrees that should only contain the value `2` (e.g., `[2, 2, 2, 2, 2, 2]`) (for the current code version). **Note:** Only `total_nodes_list` affects the domain resolution; `polynomial_list` is used for compatibility. The lengths of both lists must be equal.


To run the project, update these parameters in `main.py` as needed and then execute:

```bash
python main.py
```
the result can be plotted with any plot_convergence{1,2,3} imported in the main script

# Requirements
Please refer to the `requirements.txt` file for a complete list of dependencies.

## Customization

- **ML Model:** You can modify the imported machine learning model by editing the code in `functions.discrete_operator`.
- **Domain Resolution:** Adjust the `total_nodes_list` in `main.py` to change the resolution of the domain. The `polynomial_list` is provided for compatibility and should contain the value `2`(for the current code version).
- **List Lengths:** Ensure that the length of `total_nodes_list` and `polynomial_list` are the same.



