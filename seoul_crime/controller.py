from seoul_crime.cctv_pop import CCTVModel

class Controller:
    def __init__(self):
        self._cctv = CCTVModel()

    def execute(self):
        cctv = self._cctv
        cctv.hook_process()
