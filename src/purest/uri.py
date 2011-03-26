import re


class UriPattern(object):
    """A single URI pattern. Its mainly a regex that gets matched."""
    def __init__(self, regex, maps):
        self._regex = re.compile(regex, re.UNICODE)
        self._handlers = {}

        for k, v in maps.iteritems():
            self._handlers[k] = v

    def resolve(self, path, method):
        """Lookup a URI and http method and return the right handler if it
        matches.

        :param path: string, the path of the uri
        :param method: string, the http method of the request
        :rtype: A tupel consisting of the handler callable and the dictionary
                of the regex named groups.
        """
        match = self._regex.match(path)

        if match:
            #The regex matched the path
            kwargs = match.groupdict()

            #Does a handler exist for this path in combination with the http
            #method of the request?
            try:
                return (self._handlers[method], kwargs)
            except KeyError:
                pass

        #If the path couldn't be matched, return None and an empty dictionary
        return (None, {})


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
        """Iterate over the routes and return the first match.

        :param path: string, the path of the uri
        :param method: string, the http method of the request
        :rtype: A tupel consisting of the handler callable and the dictionary
                of the regex named groups.
        """
        match = None
        kwargs = {}
        for uri_pattern in self._routes:
            match, kwargs = uri_pattern.resolve(path, method)
            if match != None:
                break

        return (match, kwargs)

    @property
    def routes(self):
        """Return all stored map routes.

        :rtype: A list of URIPattern's.
        """
        return self._routes
