import pandas as pd

from typing import Dict
from pathlib import Path
from models.analyzer_config_models import AnalyzerOutputConfig

class OutputExecutor:
  def __init__(self, export_data: Dict[str, pd.DataFrame], output_config: AnalyzerOutputConfig):
    self.export_data = export_data
    self.output_config = output_config

  def _process_output(self):
    if self.output_config is None:
      return

    if self.output_config.print_output:
      print(self.export_data)

    if self.output_config.write_output:
      for key, value in self.export_data.items():
        for write_option in self.output_config.write_output:
          new_filename = f"{Path(key).stem}-analyze"

          Path(write_option.output_dir).mkdir(parents=True, exist_ok=True)

          if write_option.format == "csv":
            value.to_csv(Path(write_option.output_dir) / f"{new_filename}.csv", index=False)
          if write_option.format == "json":
            value.to_json(Path(write_option.output_dir) / f"{new_filename}.json", orient="records", indent=2)

  def execute(self):
    self._process_output()