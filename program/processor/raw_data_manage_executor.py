import pandas as pd

from typing import Dict
from pathlib import Path
from models.analyzer_config_models import AnalyzerConfig


class RawDataManageExecutor:
  def __init__(self, analyzer_config: AnalyzerConfig):
    self.analyzer_config = analyzer_config

  def _prepare_separate(self) -> Dict[str, pd.DataFrame]:
    result = {}

    for file in self.analyzer_config.csv_files:
      df = pd.read_csv(Path(self.analyzer_config.base_directory) / file)

      for value_col in self.analyzer_config.value_column_name:
        result[f"{file}::{value_col}"] = df

    return result

  def _prepare_merged(self) -> Dict[str, pd.DataFrame]:
    merged_by_value_col: Dict[str, list] = {
      value_col: [] for value_col in self.analyzer_config.value_column_name
    }

    for file in self.analyzer_config.csv_files:
      df = pd.read_csv(Path(self.analyzer_config.base_directory) / file)
      df["_source_file"] = Path(file).stem

      for value_col in self.analyzer_config.value_column_name:
        merged_by_value_col[value_col].append(df)

    return {
      value_col: pd.concat(frames, ignore_index=True)
      for value_col, frames in merged_by_value_col.items()
    }

  def execute(self) -> Dict[str, pd.DataFrame]:
    if self.analyzer_config.merge_csv:
      return self._prepare_merged()
    return self._prepare_separate()
