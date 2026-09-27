import subprocess
import sys

from logger import setup_logger


logger = setup_logger()


PIPELINE_STEPS = [
    "src/ingestion.py",
    "src/cleaning.py",
    "src/transformation.py",
    "src/validation.py",
    "src/load_data.py",
]


def run_pipeline():
    """Run all JobPulse pipeline stages in sequence."""

    logger.info("===== JOBPULSE PIPELINE STARTED =====")

    for step in PIPELINE_STEPS:

        logger.info(f"Starting pipeline step: {step}")
        print(f"\n===== RUNNING: {step} =====")

        try:
            subprocess.run(
                [sys.executable, step],
                check=True
            )

            logger.info(f"Completed pipeline step: {step}")

        except subprocess.CalledProcessError:
            logger.error(f"Pipeline step failed: {step}")
            print(f"\nPipeline failed at: {step}")
            raise

    logger.info("===== JOBPULSE PIPELINE COMPLETED =====")
    print("\n===== JOBPULSE PIPELINE COMPLETED =====")


if __name__ == "__main__":
    run_pipeline()