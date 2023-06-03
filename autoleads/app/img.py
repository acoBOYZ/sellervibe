import aiohttp
import os
from pathlib import Path
from skimage import io
from skimage.metrics import structural_similarity as ssim
from PIL import Image
import aiofiles
from logger import Logger

class ImageComparator:
    def __init__(self, asin: str, amazon_img_url: str, product_img_url: str, threshold: float, logger: Logger):
        self.asin = asin
        self.amazon_img_url = amazon_img_url
        self.product_img_url = product_img_url
        self.threshold = threshold / 100
        APP_DIR = Path(__file__).resolve().parent
        self.media_path = os.path.join(APP_DIR, 'media')
        self.amazon_img_path = os.path.join(self.media_path, f'{self.asin}/{self.asin}.png')
        self.product_img_path = os.path.join(self.media_path, f'{self.asin}/product.png')
        self.logger = logger

    async def download_image(self, url, path):
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as resp:
                    if resp.status == 200:
                        f = await aiofiles.open(path, mode='wb')
                        await f.write(await resp.read())
                        await f.close()
        except Exception as e:
            self.logger.log_and_write_error('Image download error:', str(e))
            self.logger.log_and_write_error('Image url:', url)

    async def compare(self):
        try:
            if not os.path.exists(self.media_path):
                os.makedirs(self.media_path)

            await self.download_image(self.amazon_img_url, self.amazon_img_path)
            await self.download_image(self.product_img_url, self.product_img_path)

            if os.path.exists(self.amazon_img_path) and os.path.exists(self.product_img_path):
                img1 = io.imread(self.amazon_img_path, as_gray=True)
                img2 = io.imread(self.product_img_path, as_gray=True)

                similarity = ssim(img1, img2)
                self.logger.debug_log(f'Similarity of two image: {similarity * 100:.2f}%')

                os.remove(self.product_img_path)

                return similarity >= self.threshold
            return False
        except Exception as e:
            self.logger.log_and_write_error('Image compare error:', str(e))
            return False
