import yaml
import pandas as pd

from pathlib import Path

from models.analyzer_config_models import AnalyzerConfig

from processor.output_exporter import OutputExecutor
from processor.raw_data_manage_executor import RawDataManageExecutor
from processor.stats_analyze_executor import StatsAnalyzeExecutor

from global_test_config import *

def test_config_template_matches_model():
  template_path = Path(CONFIG_TEMPLATES_PATH)

  with open(template_path, 'r') as f:
    yaml_data = yaml.safe_load(f)

  test_config = AnalyzerConfig(**yaml_data)

  assert test_config is not None

def test_stats_analyzer_executor():
  raw_data = RawDataManageExecutor(SAMPLE_ANALYZER_CONFIG).execute()
  result = StatsAnalyzeExecutor(SAMPLE_ANALYZER_CONFIG, raw_data).execute()

  assert result is not None
  assert isinstance(result, dict)

  for file, df in result.items():
    assert isinstance(df, pd.DataFrame)
    assert len(df) > 0

def test_output_exporter():
  raw_data = RawDataManageExecutor(SAMPLE_ANALYZER_CONFIG).execute()
  result = StatsAnalyzeExecutor(SAMPLE_ANALYZER_CONFIG, raw_data).execute()

  ope = OutputExecutor(result, SAMPLE_ANALYZER_CONFIG.output_config)
  ope.execute()

def test_stats_analyzer_executor_multi_value_column():
  raw_data = RawDataManageExecutor(SAMPLE_MULTI_VALUE_ANALYZER_CONFIG).execute()
  result = StatsAnalyzeExecutor(SAMPLE_MULTI_VALUE_ANALYZER_CONFIG, raw_data).execute()

  assert result is not None
  assert isinstance(result, dict)

  expected_keys = [
    "sample_data_cpu_memory.csv::cpu",
    "sample_data_cpu_memory.csv::memory",
  ]

  for key in expected_keys:
    assert key in result, f"Expected key '{key}' not found in result"
    df = result[key]
    assert isinstance(df, pd.DataFrame)
    assert len(df) > 0
    assert "avg" in df.columns
    assert "max" in df.columns
    assert "p25" in df.columns
    assert "p50" in df.columns
    assert "p95" in df.columns

def test_raw_data_manage_merge_false():
  raw_data = RawDataManageExecutor(SAMPLE_MERGE_FALSE_ANALYZER_CONFIG).execute()
  result = StatsAnalyzeExecutor(SAMPLE_MERGE_FALSE_ANALYZER_CONFIG, raw_data).execute()

  assert result is not None
  assert isinstance(result, dict)

  # merge=false produces one key per (file, value_col)
  expected_keys = [
    "sample_data_cpu.csv::value",
    "sample_data_mem.csv::value",
  ]

  for key in expected_keys:
    assert key in result, f"Expected key '{key}' not found in result"
    df = result[key]
    assert isinstance(df, pd.DataFrame)
    assert len(df) > 0
    assert "avg" in df.columns
    assert "max" in df.columns

def test_raw_data_manage_merge_true():
  raw_data = RawDataManageExecutor(SAMPLE_MERGE_TRUE_ANALYZER_CONFIG).execute()
  result = StatsAnalyzeExecutor(SAMPLE_MERGE_TRUE_ANALYZER_CONFIG, raw_data).execute()

  assert result is not None
  assert isinstance(result, dict)

  # merge=true produces one key per value_col only
  assert "value" in result, "Expected key 'value' not found in result"
  assert "sample_data_cpu.csv::value" not in result
  assert "sample_data_mem.csv::value" not in result

  df = result["value"]
  assert isinstance(df, pd.DataFrame)
  assert len(df) > 0
  assert "avg" in df.columns
  assert "max" in df.columns