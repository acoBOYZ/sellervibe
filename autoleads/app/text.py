import asyncio
import difflib
from logger import Logger

class TextComparator:
    def __init__(self, text1: str, text2: str, threshold: float, logger: Logger):
        self.text1 = text1
        self.text2 = text2
        self.threshold = threshold / 100
        self.logger = logger

    def calculate_similarity(self):
        seq_matcher = difflib.SequenceMatcher(None, self.text1, self.text2)
        return seq_matcher.ratio()

    async def compare(self, threshold=0.85):
        try:
            loop = asyncio.get_running_loop()
            similarity = await loop.run_in_executor(None, self.calculate_similarity)
            self.logger.debug_log(f'Similarity of two text: {similarity * 100:.2f}%')
            return similarity >= threshold
        except Exception as e:
            self.logger.log_and_write_error('Text compare error:', str(e))
            return False