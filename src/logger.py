import logging
from environ import LOG_LEVEL

logging.basicConfig(
    level=LOG_LEVEL,
    datefmt="%d/%m/%Y %H:%M:%S",
    format="%(asctime)s, %(levelname)s: %(message)s",
)

logger = logging.getLogger(__name__)