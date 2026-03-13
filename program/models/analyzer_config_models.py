from pydantic import BaseModel, model_validator
from typing import List, Optional
from enum import StrEnum

class OutputFormatType(StrEnum):
  CSV = "csv"
  JSON = "json"

class AnalyzerOutputWriteConfig(BaseModel):
  output_dir: str
  format: OutputFormatType

class AnalyzerOutputConfig(BaseModel):
  print_output: Optional[bool] = False
  write_output: Optional[List[AnalyzerOutputWriteConfig]] = None

class AnalyzerStatsConfig(BaseModel):
  percentiles: Optional[List[int]] = None
  min: Optional[bool] = False
  max: Optional[bool] = False
  std: Optional[bool] = False
  cov: Optional[bool] = False
  avg: Optional[bool] = False

  @model_validator(mode="after")
  def at_least_one_stat(self) -> "AnalyzerStatsConfig":
    has_pct = bool(self.percentiles)
    has_any_stat = any([self.min, self.max, self.std, self.cov, self.avg])

    if not has_pct and not has_any_stat:
      raise ValueError("At least one stat must be enabled or percentile must be provided")
    return self

class AnalyzerConfig(BaseModel):
  base_directory: str
  csv_files: List[str]
  value_column_name: List[str]
  export_column_name: Optional[List[str]] = None
  merge_csv: bool = False
  output_config: Optional[AnalyzerOutputConfig] = None
  stats_config: AnalyzerStatsConfig