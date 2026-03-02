from models.analyzer_config_models import *

CONFIG_TEMPLATES_PATH = "../config_templates/config.yaml"

SAMPLE_ANALYZER_CONFIG = AnalyzerConfig(
  base_directory="./",
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
        output_dir="./result"
      ),
      AnalyzerOutputWriteConfig(
        format=OutputFormatType.JSON,
        output_dir="./result"
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