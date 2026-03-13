from pathlib import Path
from models.analyzer_config_models import *

_TEST_DIR = str(Path(__file__).parent)
CONFIG_TEMPLATES_PATH = str(Path(__file__).parent.parent / "config_templates" / "config.yaml")

SAMPLE_MERGE_FALSE_ANALYZER_CONFIG = AnalyzerConfig(
  base_directory=_TEST_DIR,
  csv_files=[
    "sample_data_cpu.csv",
    "sample_data_mem.csv",
  ],
  merge_csv=False,
  value_column_name=["value"],
  export_column_name=["namespace", "app_name"],
  stats_config=AnalyzerStatsConfig(
    percentiles=[25, 50, 95],
    avg=True,
    max=True,
  )
)

SAMPLE_MERGE_TRUE_ANALYZER_CONFIG = AnalyzerConfig(
  base_directory=_TEST_DIR,
  csv_files=[
    "sample_data_cpu.csv",
    "sample_data_mem.csv",
  ],
  merge_csv=True,
  value_column_name=["value"],
  export_column_name=["namespace", "app_name"],
  stats_config=AnalyzerStatsConfig(
    percentiles=[25, 50, 95],
    avg=True,
    max=True,
  )
)

SAMPLE_MULTI_VALUE_ANALYZER_CONFIG = AnalyzerConfig(
  base_directory=_TEST_DIR,
  csv_files=[
    "sample_data_cpu_memory.csv",
  ],
  value_column_name=[
    "cpu",
    "memory",
  ],
  export_column_name=[
    "namespace",
    "app_name",
  ],
  stats_config=AnalyzerStatsConfig(
    percentiles=[25, 50, 95],
    avg=True,
    max=True,
  )
)

SAMPLE_ANALYZER_CONFIG = AnalyzerConfig(
  base_directory=_TEST_DIR,
  csv_files=[
    "sample_data_cpu.csv",
    "sample_data_mem.csv",
  ],
  value_column_name=[
    "value",
  ],
  export_column_name=[
    "namespace",
    "app_name",
  ],
  output_config=AnalyzerOutputConfig(
    print_output=True,
    write_output=[
      AnalyzerOutputWriteConfig(
        format=OutputFormatType.CSV,
        output_dir=str(Path(_TEST_DIR) / "result")
      ),
      AnalyzerOutputWriteConfig(
        format=OutputFormatType.JSON,
        output_dir=str(Path(_TEST_DIR) / "result")
      ),
    ]
  ),
  stats_config=AnalyzerStatsConfig(
    percentiles=[
      25,
      50,
      95,
    ],
  )
)