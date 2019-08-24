from seoul_crime.cctv_pop import CCTVModel
from seoul_crime.crime_police import CrimeModel

class Controller:
    def __init__(self):
        self._cctv = CCTVModel()
        self._crime = CrimeModel()

    def execute(self):
      #  cctv = self._cctv
      #  cctv.hook_process()
        crime = self._crime
        crime.hook_process()

