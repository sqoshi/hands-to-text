import logging
import warnings


def setup_logging():
    warnings.filterwarnings(
        "ignore", category=DeprecationWarning, module="google.protobuf.symbol_database"
    )
    warnings.filterwarnings(
        "ignore", category=UserWarning, module="google.protobuf.symbol_database"
    )

    logging.basicConfig(level=logging.DEBUG)
    return logging.getLogger(__name__)
