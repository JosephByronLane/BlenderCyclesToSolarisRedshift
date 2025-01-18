class ExporterConfig:
    """Exporter configuration singleton returning the data needed for nodes at run-time.

    """
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ExporterConfig, cls).__new__(cls)
            cls._instance.properties = {}
        return cls._instance

    def set_property(self, key, value):
        self.properties[key] = value

    def get_property(self, key, default=None):
        return self.properties.get(key, default)

config = ExporterConfig()
