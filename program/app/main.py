import argparse

def main():
  parser = argparse.ArgumentParser(description="Query Prometheus from config file")
  parser.add_argument("-c", "--config", required=True, help="Path to config Yaml file")
  args = parser.parse_args()

if __name__ == "__main__":
  main()