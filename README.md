# BSEN10040 — Python Data Analysis

A beginner-friendly practical on analysing fruit juice storage data with Python. The notebook walks through a complete workflow using **pandas** and **Matplotlib**, with a food science example.

**Start here:** [Fruit Juice Storage Analysis notebook](fruit_juice_storage_analysis.ipynb)

## What you will learn

- Read a CSV file into a pandas DataFrame.
- Inspect rows, columns, data types and missing values.
- Select a subset of data and clean missing values for a specific purpose.
- Use `groupby()` and `mean()` to summarise results.
- Create and interpret line charts, grouped bar charts and scatter plots.

The practical assumes basic Python syntax and familiarity with VS Code.

## Repository contents

```text
BSEN10040-python-data-analysis/
├── README.md
├── fruit_juice_storage_analysis.ipynb   # Guided analysis notebook
└── data/
    ├── fruit_juice_storage.csv         # Synthetic teaching dataset
    ├── generate_fruit_juice_storage.py # Dataset generator
    └── README.md                      # Detailed dataset notes
```

An `outputs/` folder is created when you run the notebook.

## Getting started in VS Code

1. Download the repository using **Code → Download ZIP**, then extract it. Alternatively, clone it:

   ```bash
   git clone https://github.com/dzjxzyd/BSEN10040-python-data-analysis.git
   cd BSEN10040-python-data-analysis
   ```

2. Open the extracted or cloned **repository folder** in VS Code. Install Python and the VS Code **Python** and **Jupyter** extensions if needed.

3. Open `fruit_juice_storage_analysis.ipynb` and use **Select Kernel** to choose your Python environment.

4. Install the required packages in that notebook environment. You can run this in a notebook code cell:

   ```python
   %pip install numpy pandas matplotlib
   ```

5. Run the notebook cells **from top to bottom**. Read each explanation, inspect the tables and discuss the plots before continuing.

**Working directory:** the notebook expects its current working directory to be the repository root, containing the `data/` folder. If you get `FileNotFoundError`, check that you downloaded the whole repository and opened the correct folder. You can check the current directory with `Path.cwd()` after running the import cell.

## Dataset

The imagined experiment contains **108 samples and 9 columns**:

- **Juice types:** orange, apple and berry
- **Storage temperatures:** 4, 20 and 35 °C
- **Storage days:** 0, 2, 4 and 6
- **Batches:** 3 per combination

| Column | Description |
|---|---|
| `sample_id` | Unique sample identifier |
| `juice_type` | Orange, apple or berry |
| `storage_temp_C` | Storage temperature in °C |
| `storage_day` | Storage time in days |
| `batch` | Batch number, 1–3 |
| `vitamin_c_mg_per_100ml` | Simulated vitamin C concentration, mg per 100 mL |
| `pH` | Simulated pH |
| `microbial_load_log10` | Simulated microbial load on a log10 CFU/mL scale |
| `turbidity_NTU` | Simulated turbidity in NTU |

The data deliberately include missing pH and turbidity values, plus a high microbial-load value in sample `S108`, for inspection and cleaning exercises.

**These data are synthetic and created for teaching.** They are not real laboratory measurements and should not be used to draw food-safety, health or causal scientific conclusions.

## Analysis and outputs

The notebook follows this workflow:

**Read → inspect → check missing values → clean for a purpose → summarise → visualise → interpret**

It saves three figures in `outputs/`:

| Figure | File |
|---|---|
| Vitamin C in orange juice over time, by temperature | `vitamin_c_over_time_notebook.png` |
| Mean microbial load by storage day and temperature, across juice types and batches | `microbial_load_by_temperature_notebook.png` |
| Vitamin C versus turbidity for complete pairs | `vitamin_c_vs_turbidity_notebook.png` |

The cleaning example removes rows missing pH or turbidity from a separate copy. Each plot uses only the variables it needs, so an unrelated missing value does not unnecessarily remove an observation.

## Practice questions

1. How does vitamin C change with storage time at different temperatures?
2. How does microbial load vary across storage days and temperatures?
3. Why might different plots use different numbers of observations?

Describe patterns as observations **in these synthetic data**. A visual association alone does not establish causation.
