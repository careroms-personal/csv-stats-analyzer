import pandas as pd

from typing import Dict
from models.analyzer_config_models import *

class StatsAnalyzeExecutor:
  def __init__(self, analyzer_config: AnalyzerConfig, raw_data: Dict[str, pd.DataFrame]):
    self.analyzer_config = analyzer_config
    self.stats_config = analyzer_config.stats_config
    self.raw_data = raw_data

  def _analyze_data(self) -> Dict[str, pd.DataFrame]:
    return {
      key: self._compute_stats(df, key.split("::")[-1])
      for key, df in self.raw_data.items()
    }

  def _compute_stats(self, df: pd.DataFrame, value_col: str) -> pd.DataFrame:
    results = []

    for keys, group_df in df.groupby(self.analyzer_config.export_column_name):
      result = {}
      series = group_df[value_col]

      for col, key in zip(self.analyzer_config.export_column_name, keys):
        result[col] = key

      if self.stats_config.avg:
        result["avg"] = series.mean()
      if self.stats_config.std:
        result["std"] = series.std()
      if self.stats_config.min:
        result["min"] = series.min()
      if self.stats_config.max:
        result["max"] = series.max()
      if self.stats_config.cov:
        result["cov"] = series.std() / series.mean()
      if self.stats_config.percentiles:
        for pct in self.stats_config.percentiles:
          result[f"p{pct}"] = series.quantile(pct/100)

      results.append(result)

    return pd.DataFrame(results)

  def execute(self) -> Dict[str, pd.DataFrame]:
    return self._analyze_data()