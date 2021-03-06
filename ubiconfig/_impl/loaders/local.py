import logging
import os

import yaml

from ubiconfig.utils.config_validation import validate_config
from ubiconfig.config_types import UbiConfig


LOG = logging.getLogger('ubiconfig')


class LocalLoader(object):
    """Load configuration from a local directory tree."""
    def __init__(self, path):
        self._path = path

    def load(self, file_name):
        file_path = os.path.join(self._path, file_name)
        LOG.info("Loading configuration file locally: %s", file_path)

        try:
            with open(file_path, 'r') as f:
                config_dict = yaml.safe_load(f)

        except yaml.YAMLError:
            LOG.error('There is syntax error in your config file %s, please fix', file_name)
            raise

        # validate input data
        validate_config(config_dict)

        return UbiConfig.load_from_dict(config_dict, file_name)

    def load_all(self, recursive=False):
        ubi_configs = []

        file_list = self._get_local_file_list(recursive)
        for file in file_list:
            LOG.debug("Now loading %s", file)
            ubi_configs.append(self.load(file))

        return ubi_configs

    def _get_local_file_list(self, recursive):
        """
        Get the config file list from local. If recusive is set, then it would walk
        through the sub-modules.
        """
        LOG.info('Getting the local config file list')
        file_list = []
        if recursive:
            for root, _, files in os.walk(self._path):
                files = [os.path.join(root, f) for f in files if f.endswith(('.yaml', '.yml'))]
                file_list.extend(files)
        else:
            file_list = [file for file in os.listdir(self._path)
                         if file.endswith(('yaml', '.yml'))]

        return file_list
