import argparse
import json
import logging
import os
import sys
import time

import numpy as np
import pandas as pd
import yaml


def setup_logging(log_file):
    logging.basicConfig(
        filename=log_file,
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
    )


def load_config(config_path):
    if not os.path.exists(config_path):
        raise FileNotFoundError("Configuration file not found.")

    with open(config_path, "r") as f:
        config = yaml.safe_load(f)

    required_fields = ["seed", "window", "version"]
    for field in required_fields:
        if field not in config:
            raise ValueError(f"Missing required config field: {field}")

    return config


def validate_input_file(input_path):
    if not os.path.exists(input_path):
        raise FileNotFoundError("Input CSV file not found.")

    if os.path.getsize(input_path) == 0:
        raise ValueError("Input CSV file is empty.")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--config", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--log-file", required=True)

    args = parser.parse_args()

    start_time = time.time()

    try:
        setup_logging(args.log_file)
        logging.info("Job started")

        # Load config
        config = load_config(args.config)
        seed = config["seed"]
        window = config["window"]
        version = config["version"]

        logging.info(f"Config loaded: seed={seed}, window={window}, version={version}")

        np.random.seed(seed)

        # Validate input
        validate_input_file(args.input)

        # Load CSV
        df = pd.read_csv(args.input)

        if df.empty:
            raise ValueError("Input CSV contains no rows.")

        if "close" not in df.columns:
            raise ValueError("Required column 'close' not found in dataset.")

        rows_processed = len(df)
        logging.info(f"Data loaded: {rows_processed} rows")

        # Rolling mean
        df["rolling_mean"] = df["close"].rolling(window=window).mean()
        logging.info(f"Rolling mean calculated with window={window}")

        # Signal generation
        df["signal"] = np.where(df["close"] > df["rolling_mean"], 1, 0)
        logging.info("Signals generated")

        # Metrics
        signal_rate = float(df["signal"].mean())
        latency_ms = int((time.time() - start_time) * 1000)

        metrics = {
            "version": version,
            "rows_processed": rows_processed,
            "metric": "signal_rate",
            "value": round(signal_rate, 4),
            "latency_ms": latency_ms,
            "seed": seed,
            "status": "success",
        }

        with open(args.output, "w") as f:
            json.dump(metrics, f, indent=4)

        logging.info(
            f"Metrics: signal_rate={round(signal_rate,4)}, rows_processed={rows_processed}"
        )
        logging.info(f"Job completed successfully in {latency_ms}ms")

        print(json.dumps(metrics, indent=4))
        sys.exit(0)

    except Exception as e:
        error_output = {
            "version": config["version"] if "config" in locals() and "version" in config else "unknown",
            "status": "error",
            "error_message": str(e),
        }

        with open(args.output, "w") as f:
            json.dump(error_output, f, indent=4)

        logging.error(f"Error occurred: {str(e)}")
        print(json.dumps(error_output, indent=4))
        sys.exit(1)


if __name__ == "__main__":
    main()