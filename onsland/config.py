import os
import sys
import logging
from typing import Dict
from pathlib import Path
from yacs.config import CfgNode as CN

# from util.base_util import validate_config

logger = logging.getLogger(__name__)

__all__ = ["cfg"]

MAIN_PATH = Path(__file__).parent
CONFIG_FILE = Path(MAIN_PATH, "config", "config.yml")
CONFIG_OVERRIDE = Path(MAIN_PATH, "config", "config-local.yml")
VALID_ENV_VARS: Dict[str, str] = {}

cfg = CN(new_allowed=True)
if CONFIG_FILE.exists():
    cfg.merge_from_file(CONFIG_FILE)
else:
    logger.error("A required 'config/config.yml' configuration file is missing.")
    sys.exit(1)

# override with custom config
if CONFIG_OVERRIDE.exists():
    cfg.merge_from_file(CONFIG_OVERRIDE)

# finally override with env vars
for k in VALID_ENV_VARS.keys():
    cfg[k] = os.environ[k]

# # Validate config before starting
# config_valid, config_error = validate_config(cfg)
# if config_valid is not True:
#     logger.error(f"Config not valid: {config_error}\nExiting..")
#     sys.exit(1)
