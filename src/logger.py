import logging
from environ import LOG_LEVEL

logging.basicConfig(
    level=LOG_LEVEL,
    datefmt="%d/%m/%Y %H:%M:%S",
    format="%(asctime)s, %(levelname)s [%(filename)s:%(lineno)d] %(funcName)s(): %(message)s",
)

logger = logging.getLogger(__name__)