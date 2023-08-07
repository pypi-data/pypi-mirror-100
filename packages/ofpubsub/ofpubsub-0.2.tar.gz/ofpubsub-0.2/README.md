# Onlyfunction Pubsub

## RabbitMQ
```python
from of-pubsub import RabbitMQ

rabbit = RabbitMQ('access_key', 'secretkey')

rabbit.publish('topic', 'key', 'message')

```

## License
MIT License