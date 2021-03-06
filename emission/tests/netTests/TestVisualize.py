# Standard imports
import unittest
import json
import logging
from datetime import datetime, timedelta
import datetime as pydt
import arrow

# Our imports
import emission.core.get_database as edb
from emission.net.api import visualize
import emission.tests.common as etc
import emission.analysis.intake.segmentation.trip_segmentation as eaist
import emission.analysis.intake.segmentation.section_segmentation as eaiss
import emission.analysis.intake.cleaning.filter_accuracy as eaicf
import emission.storage.timeseries.format_hacks.move_filter_field as estfm
import emission.core.wrapper.motionactivity as ecwm
import emission.storage.decorations.local_date_queries as esdldq


class TestVisualize(unittest.TestCase):
    def setUp(self):
        etc.setupRealExample(self,
                             "emission/tests/data/real_examples/shankari_2015-aug-27")
        eaicf.filter_accuracy(self.testUUID)
        estfm.move_all_filters_to_data()
        logging.info(
            "After loading, timeseries db size = %s" % edb.get_timeseries_db().count())
        self.day_start_ts = 1440658800
        self.day_end_ts = 1440745200
        self.day_start_dt = esdldq.get_local_date(self.day_start_ts, "America/Los_Angeles")
        self.day_end_dt = esdldq.get_local_date(self.day_end_ts, "America/Los_Angeles")

    def tearDown(self):
        self.clearRelatedDb()

    def clearRelatedDb(self):
        edb.get_timeseries_db().remove({"user_id": self.testUUID})
        edb.get_analysis_timeseries_db().remove({"user_id": self.testUUID})


    def testCommutePopRoute(self):
        points = visualize.range_mode_heatmap(["BICYCLING"],
                                          self.day_start_dt,
                                          self.day_end_dt, None)
        self.assertTrue(len(['latlng']) > 0)
        # I have to add test data with modes, I will do that tomorrow.


    def testBerkeleyPopRoute(self):
        points = visualize.Berkeley_pop_route(self.day_start_ts,
                                          self.day_end_ts)
        self.assertTrue(len(['latlng']) > 0)


if __name__ == '__main__':
    import emission.tests.common as etc
    etc.configLogging()

    unittest.main()
