import redis
import json
import logging

class PostHandler:
    def __init__(self, host='redis', port=6379, db=0, password=''):
        self.redis_client = redis.StrictRedis(host=host, port=port, db=db, password=password, decode_responses=True)

    def save_post(self, post, expiration_time):
        is_needs_to_post = False
        post_id = post.get('id')
        new_roi = self.get_roi_from_post(post)
        post_info = {'roi': new_roi}
        if self.redis_client.exists(post_id):
            old_post_info = json.loads(self.redis_client.get(post_id))

            old_roi = old_post_info.get('roi')

            if old_roi != new_roi:
                self.redis_client.delete(post_id)
                is_needs_to_post = True
        else:
            is_needs_to_post = True

        if is_needs_to_post:
            self.redis_client.setex(name=post_id, value=json.dumps(post_info), time=expiration_time)
            return post

        return None

    def check_post(self, post, expiration_time=86400):
        try:
            post = self.save_post(post, expiration_time)
        except redis.RedisError as e:
            logging.error(f'An error occurred while fetching data from Redis in PostHandler: {e}')
            post = None
        except json.JSONDecodeError as e:
            logging.error(f'An error occurred while decoding JSON data from Redis in PostHandler: {e}')
            post = None
        except Exception as e:
            logging.error(f'An error occurred in PostHandler: {e}')
            post = None

        return post

    @staticmethod
    def get_roi_from_post(post):
        fields = post.get('fields', [])
        for field in fields:
            if 'ROI' in field.get('name', ''):
                return field.get('value')
        return None
