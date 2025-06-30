# Performance Optimization Standards

## Database Optimization

### Query Optimization
```python
from sqlalchemy import func, and_, or_
from sqlalchemy.orm import joinedload, selectinload

# Efficient queries with proper joins
def get_user_with_messages(user_id):
    """Get user with all messages in single query"""
    return db.session.query(User)\
        .options(selectinload(User.messages))\
        .filter(User.id == user_id)\
        .first()

# Use aggregation functions in database
def get_message_stats():
    """Get message statistics efficiently"""
    return db.session.query(
        func.count(Message.id).label('total_messages'),
        func.avg(func.length(Message.content)).label('avg_length'),
        func.max(Message.created_at).label('latest_message')
    ).first()

# Batch operations for multiple records
def bulk_update_messages(message_ids, status):
    """Update multiple messages efficiently"""
    db.session.query(Message)\
        .filter(Message.id.in_(message_ids))\
        .update({Message.status: status}, synchronize_session=False)
    db.session.commit()
```

### Connection Pooling
```python
from sqlalchemy import create_engine
from sqlalchemy.pool import QueuePool

# Configure connection pool
engine = create_engine(
    DATABASE_URL,
    poolclass=QueuePool,
    pool_size=10,
    max_overflow=20,
    pool_recycle=3600,  # Recycle connections after 1 hour
    pool_pre_ping=True  # Validate connections before use
)
```

### Database Indexing
```sql
-- Create indexes for frequently queried columns
CREATE INDEX idx_messages_user_id ON messages(user_id);
CREATE INDEX idx_messages_created_at ON messages(created_at);
CREATE INDEX idx_messages_status ON messages(status);

-- Composite indexes for complex queries
CREATE INDEX idx_messages_user_status ON messages(user_id, status);
CREATE INDEX idx_messages_created_user ON messages(created_at, user_id);
```

## Memory Management

### Efficient Data Structures
```python
import sys
from collections import deque, defaultdict
import weakref

class MessageBuffer:
    """Efficient message buffering with automatic cleanup"""
    def __init__(self, max_size=1000):
        self.messages = deque(maxlen=max_size)
        self.user_messages = defaultdict(list)
        self.max_size = max_size
    
    def add_message(self, user_id, message):
        """Add message with automatic cleanup"""
        self.messages.append((user_id, message))
        self.user_messages[user_id].append(message)
        
        # Cleanup old user messages
        if len(self.user_messages[user_id]) > 100:
            self.user_messages[user_id] = self.user_messages[user_id][-50:]
    
    def get_memory_usage(self):
        """Get current memory usage"""
        return sys.getsizeof(self.messages) + sys.getsizeof(self.user_messages)
```

### Memory Monitoring
```python
import psutil
import gc
from memory_profiler import profile

class MemoryMonitor:
    @staticmethod
    def get_memory_usage():
        """Get current memory usage"""
        process = psutil.Process()
        return {
            'rss': process.memory_info().rss / 1024 / 1024,  # MB
            'vms': process.memory_info().vms / 1024 / 1024,  # MB
            'percent': process.memory_percent()
        }
    
    @staticmethod
    def force_garbage_collection():
        """Force garbage collection"""
        collected = gc.collect()
        return collected
    
    @profile
    def memory_intensive_function(self):
        """Example of memory profiling"""
        # Your memory-intensive code here
        pass
```

## Caching Strategies

### Redis Caching
```python
import redis
import json
import pickle
from functools import wraps

redis_client = redis.Redis(host='localhost', port=6379, db=0)

def cache_result(expiration=3600, key_prefix='ada'):
    """Decorator for caching function results"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Generate cache key
            cache_key = f"{key_prefix}:{func.__name__}:{hash(str(args) + str(kwargs))}"
            
            # Try to get from cache
            cached_result = redis_client.get(cache_key)
            if cached_result:
                return pickle.loads(cached_result)
            
            # Execute function and cache result
            result = func(*args, **kwargs)
            redis_client.setex(
                cache_key, 
                expiration, 
                pickle.dumps(result)
            )
            return result
        return wrapper
    return decorator

# Usage
@cache_result(expiration=1800)  # Cache for 30 minutes
def get_weather_data(location):
    """Get weather data with caching"""
    # Expensive API call
    return fetch_weather_from_api(location)
```

### Application-Level Caching
```python
from cachetools import TTLCache, LRUCache
import threading

class ApplicationCache:
    def __init__(self):
        self.ttl_cache = TTLCache(maxsize=1000, ttl=3600)  # 1 hour TTL
        self.lru_cache = LRUCache(maxsize=500)  # LRU cache for frequently accessed data
        self.lock = threading.RLock()
    
    def get_or_set(self, key, value_func, cache_type='ttl'):
        """Get from cache or set if not exists"""
        with self.lock:
            cache = self.ttl_cache if cache_type == 'ttl' else self.lru_cache
            
            if key in cache:
                return cache[key]
            
            value = value_func()
            cache[key] = value
            return value
```

## Asynchronous Processing

### Task Queue Implementation
```python
from celery import Celery
from kombu import Queue

# Configure Celery
celery_app = Celery('ada_tasks',
                   broker='redis://localhost:6379/0',
                   backend='redis://localhost:6379/0')

celery_app.conf.update(
    task_routes={
        'ada_tasks.process_data': {'queue': 'data_processing'},
        'ada_tasks.send_notification': {'queue': 'notifications'},
    },
    task_default_queue='default',
    task_queues=(
        Queue('default', routing_key='default'),
        Queue('data_processing', routing_key='data_processing'),
        Queue('notifications', routing_key='notifications'),
    ),
)

@celery_app.task(bind=True, max_retry=3)
def process_large_dataset(self, data_id):
    """Process large dataset asynchronously"""
    try:
        # Your processing logic here
        result = heavy_data_processing(data_id)
        return result
    except Exception as exc:
        # Retry with exponential backoff
        raise self.retry(exc=exc, countdown=60 * (2 ** self.request.retries))
```

### Async/Await Patterns
```python
import asyncio
import aiohttp
import aiofiles

class AsyncAPIClient:
    def __init__(self):
        self.session = None
    
    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.session.close()
    
    async def fetch_multiple_urls(self, urls):
        """Fetch multiple URLs concurrently"""
        tasks = [self.fetch_url(url) for url in urls]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        return results
    
    async def fetch_url(self, url):
        """Fetch single URL"""
        async with self.session.get(url) as response:
            return await response.text()

# Usage
async def main():
    urls = ['http://api1.com', 'http://api2.com', 'http://api3.com']
    async with AsyncAPIClient() as client:
        results = await client.fetch_multiple_urls(urls)
        return results
```

## Resource Optimization

### File Handling
```python
import os
import mmap
from contextlib import contextmanager

@contextmanager
def efficient_file_reader(filename):
    """Memory-efficient file reading using memory mapping"""
    try:
        with open(filename, 'rb') as f:
            with mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ) as mm:
                yield mm
    except Exception as e:
        raise e

def process_chunk(chunk_data):
    """Process a single chunk of data"""
    # Example processing logic - customize based on your needs
    processed_lines = []
    for line in chunk_data.decode('utf-8', errors='ignore').splitlines():
        # Process each line
        processed_line = line.strip().upper()  # Example transformation
        if processed_line:  # Skip empty lines
            processed_lines.append(processed_line)
    return processed_lines

def process_large_file(filename):
    """Process large files efficiently"""
    with efficient_file_reader(filename) as mm:
        # Process file in chunks
        chunk_size = 1024 * 1024  # 1MB chunks
        for i in range(0, len(mm), chunk_size):
            chunk = mm[i:i + chunk_size]
            # Process chunk
            yield process_chunk(chunk)
```

### Image Processing Optimization
```python
from PIL import Image
import io

class ImageOptimizer:
    @staticmethod
    def optimize_image(image_data, max_size=(800, 600), quality=85):
        """Optimize image for web display"""
        img = Image.open(io.BytesIO(image_data))
        
        # Resize if too large
        img.thumbnail(max_size, Image.Resampling.LANCZOS)
        
        # Convert to RGB if necessary
        if img.mode in ('RGBA', 'P'):
            img = img.convert('RGB')
        
        # Save optimized image
        output = io.BytesIO()
        img.save(output, format='JPEG', quality=quality, optimize=True)
        return output.getvalue()
    
    @staticmethod
    def generate_thumbnail(image_data, size=(150, 150)):
        """Generate thumbnail"""
        img = Image.open(io.BytesIO(image_data))
        img.thumbnail(size, Image.Resampling.LANCZOS)
        
        output = io.BytesIO()
        img.save(output, format='JPEG', quality=75)
        return output.getvalue()
```

## Performance Monitoring

### Application Metrics
```python
import time
from functools import wraps
from collections import defaultdict
import threading

class PerformanceMonitor:
    def __init__(self):
        self.metrics = defaultdict(list)
        self.lock = threading.Lock()
    
    def time_function(self, func_name=None):
        """Decorator to time function execution"""
        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                start_time = time.time()
                try:
                    result = func(*args, **kwargs)
                    execution_time = time.time() - start_time
                    
                    with self.lock:
                        name = func_name or func.__name__
                        self.metrics[name].append(execution_time)
                    
                    return result
                except Exception as e:
                    execution_time = time.time() - start_time
                    with self.lock:
                        name = f"{func_name or func.__name__}_error"
                        self.metrics[name].append(execution_time)
                    raise
            return wrapper
        return decorator
    
    def get_stats(self):
        """Get performance statistics"""
        with self.lock:
            stats = {}
            for func_name, times in self.metrics.items():
                if times:
                    stats[func_name] = {
                        'count': len(times),
                        'avg': sum(times) / len(times),
                        'min': min(times),
                        'max': max(times),
                        'total': sum(times)
                    }
            return stats

# Global monitor instance
monitor = PerformanceMonitor()

# Usage
@monitor.time_function()
def expensive_operation():
    """Example of monitored function"""
    time.sleep(0.1)  # Simulate work
    return "result"
```

### Database Performance Monitoring
```python
import logging
import time
from sqlalchemy import event
from sqlalchemy.engine import Engine

# Log slow queries
@event.listens_for(Engine, "before_cursor_execute")
def receive_before_cursor_execute(conn, cursor, statement, parameters, context, executemany):
    context._query_start_time = time.time()

@event.listens_for(Engine, "after_cursor_execute")
def receive_after_cursor_execute(conn, cursor, statement, parameters, context, executemany):
    total = time.time() - context._query_start_time
    
    if total > 0.1:  # Log queries taking more than 100ms
        logging.warning(f"Slow query: {total:.2f}s - {statement[:100]}...")
```

## Best Practices Checklist

- [ ] Database queries optimized with proper indexes
- [ ] Connection pooling configured
- [ ] Caching implemented for expensive operations
- [ ] Asynchronous processing for heavy tasks
- [ ] Memory usage monitored and optimized
- [ ] File operations use efficient methods
- [ ] Images optimized for web delivery
- [ ] Performance metrics collected
- [ ] Slow operations identified and optimized
- [ ] Resource cleanup implemented
- [ ] Garbage collection tuned if needed
- [ ] Background tasks use task queues
