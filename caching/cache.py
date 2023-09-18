import cachetools

class MyCache(cachetools.Cache):
    # Create a cache with a TTL of 4 hours
    cache = cachetools.TTLCache(maxsize=100, ttl=4 * 3600)  # 4 hours in seconds