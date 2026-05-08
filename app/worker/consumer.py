import json
import time
import uuid

import pika
from pika.adapters.blocking_connection import BlockingChannel

from app.core.config import settings
from app.domain.schemas import CourseCompletedEvent
from app.infrastructure.db import SessionLocal
from app.services.dependencies import get_certification_service


class CourseCompletedConsumer:
    def __init__(self):
        self.connection = self._connect_with_retry()
        self.channel: BlockingChannel = self.connection.channel()
        self.channel.queue_declare(queue=settings.rabbitmq_queue, durable=True)

    def _connect_with_retry(self):
        last_error = None
        for _ in range(30):
            try:
                return pika.BlockingConnection(pika.URLParameters(settings.rabbitmq_url))
            except Exception as exc:
                last_error = exc
                time.sleep(2)
        raise last_error

    def on_message(self, ch, method, properties, body):
        payload = json.loads(body)
        event = CourseCompletedEvent(**payload)

        db = SessionLocal()
        try:
            service = get_certification_service(db)
            service.issue_from_course_completed(
                user_id=uuid.UUID(str(event.user_id)),
                course_id=uuid.UUID(str(event.course_id)),
            )
            ch.basic_ack(delivery_tag=method.delivery_tag)
        except Exception:
            ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)
        finally:
            db.close()

    def run(self):
        self.channel.basic_qos(prefetch_count=1)
        self.channel.basic_consume(
            queue=settings.rabbitmq_queue,
            on_message_callback=self.on_message,
        )
        self.channel.start_consuming()


if __name__ == "__main__":
    consumer = CourseCompletedConsumer()
    consumer.run()
