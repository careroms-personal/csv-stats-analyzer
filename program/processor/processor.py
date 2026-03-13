import yaml, sys

from pathlib import Path
from pydantic import ValidationError

from .stats_analyze_executor import StatsAnalyzeExecutor
from .raw_data_manage_executor import RawDataManageExecutor
from models.analyzer_config_models import *

from .output_exporter import OutputExecutor

class Processor:
  def __init__(self, config_path: str):
    self._load_and_validate_config(config_path=config_path)

  def _load_and_validate_config(self, config_path: str):
    if not Path(config_path).exists():
      print(f"❌ Config file not found: {config_path}")
      sys.exit(1)
    
    try:
      with open(config_path, 'r') as f:
        yaml_data = yaml.safe_load(f)
        self.analyzer_config = AnalyzerConfig(**yaml_data)
    except ValidationError as e:
      print(f"❌ Invalid config file:")

      for error in e.errors():
        print(f"   - {error['loc']}: {error['msg']}")
      
      sys.exit(1)

  def execute(self):
    self.raw_data_manage_executor = RawDataManageExecutor(self.analyzer_config)
    self.raw_data = self.raw_data_manage_executor.execute()

    self.stats_analyze_executor = StatsAnalyzeExecutor(self.analyzer_config, self.raw_data)
    self.stats_analyzed_result = self.stats_analyze_executor.execute()

    self.output_executor = OutputExecutor(self.stats_analyzed_result, self.analyzer_config.output_config)
    self.output_executor.execute()