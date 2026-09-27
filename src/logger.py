import logging
import os


LOG_DIR = "logs"
LOG_FILE = os.path.join(LOG_DIR, "jobpulse.log")


def setup_logger():
    """Create and configure the JobPulse logger."""

    os.makedirs(LOG_DIR, exist_ok=True)

    logging.basicConfig(
        filename=LOG_FILE,
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s"
    )

    return logging.getLogger("JobPulse")