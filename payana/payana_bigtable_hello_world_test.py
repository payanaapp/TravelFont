from TravelFont.payana.payana_bl.bigtable_utils.constants import bigtable_constants
from payana.payana_bl.bigtable_utils.test.bigtable_orchestration_test import bigtable_orchestration

import os

bigtable_orchestration(
    os.path.join(bigtable_constants.travelfont_home, "payana/payana_bl/bigtable_utils/config/client_config.yaml"))
