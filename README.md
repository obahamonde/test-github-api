Please write a Dataclass Subclass called ApiClient that will take `aiohttp.ClientSession` configuration parameters with field descriptor providing sensible defaults or default factories if system contrained, feel free to import the modules needed.
Also this class must implement lazy loading of the client session and sharing a single instance of it across all instances of the subclasses of ApiClient with the configuration parameters provided that are mutable and idempotent. The required configuration parameters are: headers and base_url. The class must also implement Lazy Loading of the ClientSession object via a LazyProxy Generic, the class must implement an intuitive api for the methods to interact with external apis, by implementing [get post put delete patch](Return Json) [websocket](Return a websocket session) [stream](Return an async generator of str) [blob](Returns a bytes or BynaryIO) [text](Returns a str or TextIO), also it must be implicitly implemented the closing of the client session when the event loop is closed.