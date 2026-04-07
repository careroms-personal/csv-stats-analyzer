# csv-stats-analyzer

A config-driven CLI tool for computing statistical metrics (percentiles, mean, min, max, std, CoV) from CSV files, grouped by specified columns, with CSV and JSON export.

## Overview

This tool loads one or more CSV files, groups rows by specified columns, computes statistical metrics on value columns, and exports the results. It is designed for analyzing time-series metric exports — for example, Prometheus CSV dumps grouped by namespace or service.

## Requirements

- Python >= 3.9

```bash
pip install .
```

## Usage

```bash
python program/app/main.py -c <path-to-config.yaml>
```

**Arguments:**

| Flag | Description |
|------|-------------|
| `-c`, `--config` | Path to the YAML configuration file (required) |

**Example:**

```bash
python program/app/main.py -c ./my_config.yaml
```

## Configuration

A template is provided at [program/config_templates/config.yaml](program/config_templates/config.yaml).

### Full Structure

```yaml
base_directory: "/data/metrics"      # Base directory for input CSV files

csv_files:                           # CSV filenames relative to base_directory
  - cpu_metrics.csv
  - memory_metrics.csv

value_column_name:                   # Columns containing values to analyze
  - value

export_column_name:                  # Columns to group results by
  - namespace
  - app_name

merge_csv: false                     # false: analyze each CSV separately
                                     # true: merge all CSVs before analysis

stats_config:                        # At least one stat must be enabled
  percentiles:
    - 25
    - 50
    - 95
  avg: false
  min: false
  max: false
  std: false
  cov: false                         # Coefficient of variation (std / mean)

output_config:                       # Optional
  print_output: false                # Print results to stdout
  write_output:
    - output_dir: "./results"
      format: csv
    - output_dir: "./results"
      format: json
```

### Configuration Fields

#### Top-level

| Field | Required | Description |
|-------|----------|-------------|
| `base_directory` | Yes | Directory where input CSV files are located |
| `csv_files` | Yes | List of CSV filenames to process |
| `value_column_name` | Yes | Columns whose values will be statistically analyzed |
| `export_column_name` | Yes | Columns used to group rows before computing stats |
| `merge_csv` | No | Merge all CSVs into one before analysis (default: `false`) |

#### `stats_config`

At least one statistic must be enabled.

| Field | Description |
|-------|-------------|
| `percentiles` | List of percentile values (0–100), e.g. `[25, 50, 95]` |
| `avg` | Mean of the group |
| `min` | Minimum value |
| `max` | Maximum value |
| `std` | Standard deviation |
| `cov` | Coefficient of variation (`std / mean`) |

#### `output_config` (optional)

| Field | Description |
|-------|-------------|
| `print_output` | `true` to print results to stdout (default: `false`) |
| `write_output` | List of output destinations |

#### `write_output[]`

| Field | Description |
|-------|-------------|
| `output_dir` | Directory where output files are written |
| `format` | `"csv"` or `"json"` |

Output files are named after the input CSV: `<csv_stem>-analyze.csv` or `<csv_stem>-analyze.json`.

## Merge Behavior

| `merge_csv` | Behavior | Output key |
|-------------|----------|------------|
| `false` | Each (file, value column) pair is analyzed separately | `filename.csv::value_col` |
| `true` | All CSVs are concatenated per value column | `value_col` |

Use `merge_csv: true` when multiple CSV files contain the same schema and you want combined statistics.

## Output Formats

### CSV

Grouping columns appear first, followed by statistic columns.

```
namespace,app_name,p25,p50,p95
monitoring,alertmanager,31.6,40.0,100.7
monitoring,prometheus,202.7,244.1,289.4
```

### JSON

Array of objects with grouping columns and statistic values.

```json
[
  {
    "namespace": "monitoring",
    "app_name": "alertmanager",
    "p25": 31.6,
    "p50": 40.0,
    "p95": 100.7
  },
  {
    "namespace": "monitoring",
    "app_name": "prometheus",
    "p25": 202.7,
    "p50": 244.1,
    "p95": 289.4
  }
]
```

## Examples

### Analyze a single CSV with percentiles

```yaml
base_directory: "/data/metrics"

csv_files:
  - cpu_usage.csv

value_column_name:
  - value

export_column_name:
  - namespace
  - app_name

stats_config:
  percentiles:
    - 25
    - 50
    - 95

output_config:
  write_output:
    - output_dir: "./results"
      format: csv
```

```bash
python program/app/main.py -c ./config.yaml
# Output: ./results/cpu_usage-analyze.csv
```

### Merge multiple CSVs and export JSON

```yaml
base_directory: "/data/metrics"

csv_files:
  - week1.csv
  - week2.csv
  - week3.csv

value_column_name:
  - value

export_column_name:
  - namespace

merge_csv: true

stats_config:
  avg: true
  min: true
  max: true
  percentiles:
    - 50
    - 95

output_config:
  print_output: true
  write_output:
    - output_dir: "./results"
      format: json
```

```bash
python program/app/main.py -c ./config.yaml
# Output: ./results/value-analyze.json (merged from all 3 files)
```

### Analyze multiple value columns in one CSV

```yaml
base_directory: "/data"

csv_files:
  - services.csv      # Has both "cpu" and "memory" columns

value_column_name:
  - cpu
  - memory

export_column_name:
  - namespace
  - app_name

stats_config:
  percentiles:
    - 50
    - 95
  avg: true

output_config:
  write_output:
    - output_dir: "./results"
      format: csv
```

```bash
python program/app/main.py -c ./config.yaml
# Output: ./results/services-analyze.csv (for each value column separately)
```
