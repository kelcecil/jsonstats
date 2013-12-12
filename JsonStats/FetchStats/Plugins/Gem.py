import datetime
import re
from JsonStats.FetchStats import Fetcher


class Gem(Fetcher):

    def __init__(self):
        """
        Returns a list of gems available on the system.
        """
        self.context = 'gem'
        self.regex = re.compile('([A-Za-z0-9_\-]*)\s*(\([0-9\.,\s]*\))')
        self._load_data()

    def _load_data(self):
        self._refresh_time = datetime.datetime.utcnow()
        self._gems = {}

        cmd = 'gem list'

        try:
            for line in self._exec(cmd).split('\n')[:-1]:
                gem = self.regex.match(line)
                if (gem is not None):
                    gem_name = gem.group(1)
                    gem_version = gem.group(2)
                    self._gems[gem_name] = gem_version
            self._loaded(True)
        except Exception, e:
            self._loaded(False, str(e))

    def dump(self):
        # poor mans cache, refresh cache in an hour
        if (datetime.datetime.utcnow() -
                datetime.timedelta(minutes=1)) > self._refresh_time:
            self._load_data()
        return self._gems

    def dump_json(self):
        return self.json.dumps(self.dump(), sort_keys=True, separators=(',', ': '))
