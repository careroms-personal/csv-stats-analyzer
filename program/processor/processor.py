import yaml, sys

from pathlib import Path
from pydantic import ValidationError

from .stats_analyze_executor import StatsAnalyzeExecutor
from models.analyzer_config_models import *

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
    self.stats_analyze_executor = StatsAnalyzeExecutor(self.analyzer_config)
    self.stats_analyzed_result = self.stats_analyze_executor.execute()
    