import yaml
import pandas as pd

from pathlib import Path

from models.analyzer_config_models import AnalyzerConfig

from processor.output_exporter import OutputExecutor
from processor.stats_analyze_executor import StatsAnalyzeExecutor

from global_test_config import *

def test_config_template_matches_model():
  template_path = Path(CONFIG_TEMPLATES_PATH)

  with open(template_path, 'r') as f:
    yaml_data = yaml.safe_load(f)

  test_config = AnalyzerConfig(**yaml_data)

  assert test_config is not None

def test_stats_analyzer_executor():
  sae = StatsAnalyzeExecutor(SAMPLE_ANALYZER_CONFIG)
  result = sae.execute()

  assert result is not None
  assert isinstance(result, dict)

  for file, df in result.items():
    assert isinstance(df, pd.DataFrame)
    assert len(df) > 0
  
def test_output_exporter():
  sae = StatsAnalyzeExecutor(SAMPLE_ANALYZER_CONFIG)
  result = sae.execute()

  ope = OutputExecutor(result, SAMPLE_ANALYZER_CONFIG.output_config)
  ope.execute()