import re

class UriPattern(object):
    def __init__(self, regex, maps):
        self._regex = re.compile(regex, re.UNICODE)
        self._handlers= {}

        for k, v in maps.iteritems():
            self._handlers[k] = v

    def resolve(self, path, method):
        match = self._regex.match(path)

        if match:
            kwargs = match.groupdict()

            try:
                return self._handlers[method]
            except KeyError:
                pass
        return None

class Map(object):
    """Maps between uri/methods and handlers."""
    def __init__(self):
        self._routes = []

    def add(self, regex, maps):
        """Add a new route to the map.

        :param: regex: string, A regular expression to match uri paths against
        :param: maps: dictionary, Maps HTTP methods to callbacks
        """
        self._routes.append(UriPattern(regex, maps))

    def resolve(self, path, method):
        """Iterate over the routes and return the first match."""
        match = None
        for i in self._routes:
            match = i.resolve(path, method)
            if match != None:
                break

        return match

    @property
    def routes(self):
        """Return all stored map routes."""
        return self._routes

