# MLOps Engineering Internship - Technical Assessment

## Overview
This project implements a deterministic, reproducible MLOps-style batch pipeline for cryptocurrency OHLCV data processing.

## Setup Instructions

```bash
pip install -r requirements.txt

```bash
python run.py --input data.csv --config config.yaml --output metrics.json --log-file run.log

```bash
docker build -t mlops-task .

```bash
docker run --rm mlops-task
