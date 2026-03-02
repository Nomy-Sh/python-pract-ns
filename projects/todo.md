# TODO

## Python tools/libraries integration
* **Redis**: `redis-py`
* **Kafka**: `confluent-kafka` or `kafka-python`
* **Sidekiq Alternatives** (Ruby specific):
    - **Celery**: The most powerful and widely used task queue in Python. It supports Redis, RabbitMQ, and Amazon SQS as brokers.
    - **RQ (Redis Queue)**: A simpler, lightweight alternative to Celery that is strictly backed by Redis.
    - **Huey**: Another "little" task queue for Python that supports Redis and is easy to set up. 

    **NOTE**: There are still ways to interact with Sidekiq from Python. If you have an existing Ruby application using Sidekiq and want a Python script to trigger jobs for it, you can push JSON-formatted job data directly into Redis.

## For a Python-based stack
There are excellent libraries that serve the same roles as Redis, Sidekiq, and Kafka in the Ruby ecosystem.

### Python Task Queues (Sidekiq Alternatives)
While Sidekiq is Ruby-specific, Python has several mature frameworks for background processing:
- **Celery**: The most popular and feature-rich asynchronous task queue. It is often considered the industry standard for Python, similar to how Sidekiq is for Ruby. It supports Redis as a broker and provides advanced features like task scheduling and retries.
- **RQ (Redis Queue)**: A lightweight, simple alternative that is strictly backed by Redis. It is easier to set up than Celery if you only need basic background processing.
- **Dramatiq**: A modern, high-performance background task library that focuses on simplicity and reliability over the complex feature set of Celery. 

### Redis Libraries for Python
To interact with Redis directly for caching or data storage:
- **redis-py**: The official and most widely used client for Redis in Python. For increased performance, you can install it with the hiredis parser.
- **RedisOM Python**: Provides high-level object mapping, allowing you to model your Redis data like an ORM.
- **RedisVL**: A specialized library if you are using Redis as a vector database for AI and LLM applications. 

### Kafka Libraries for Python
For event streaming and real-time data pipelines:
- **confluent-kafka-python**: The recommended choice for high-performance and production environments. It is a thin wrapper around the high-speed C-based librdkafka library.
- **kafka-python**: A pure Python implementation that is easy to install and use for smaller projects or environments where C-extensions are difficult to manage.
- **FastStream**: A modern asynchronous framework designed specifically for working with Kafka, Redis, and RabbitMQ with a syntax similar to FastAPI.
- **Quix Streams**: A Pythonic stream processing library that offers a Pandas-like DataFrame API for processing Kafka data.