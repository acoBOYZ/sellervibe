import aiohttp
import os
from pathlib import Path
from skimage import io
from skimage.metrics import structural_similarity as ssim
from PIL import Image
import aiofiles
import logging

class ImageComparator:
    def __init__(self, asin: str, img_url_1: str, img_url_2: str, threshold: float):
        self.asin = asin
        self.img_url_1 = img_url_1
        self.img_url_2 = img_url_2
        self.threshold = threshold / 100
        APP_DIR = Path(__file__).resolve().parent
        self.media_path = os.path.join(APP_DIR, 'media')
        self.amazon_img_path = os.path.join(self.media_path, f'{self.asin}/{self.asin}.png')
        self.product_img_path = os.path.join(self.media_path, f'{self.asin}/product.png')

    async def download_image(self, url, path):
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as resp:
                    if resp.status == 200:
                        f = await aiofiles.open(path, mode='wb')
                        await f.write(await resp.read())
                        await f.close()
        except Exception as e:
            logging.error('Image download error:', str(e))
            logging.warning('Image url:', url)

    async def compare(self):
        try:
            if not os.path.exists(self.media_path):
                os.makedirs(self.media_path)

            await self.download_image(self.img_url_1, self.amazon_img_path)
            await self.download_image(self.img_url_2, self.product_img_path)

            if os.path.exists(self.amazon_img_path) and os.path.exists(self.product_img_path):
                img1 = io.imread(self.amazon_img_path, as_gray=True)
                img2 = io.imread(self.product_img_path, as_gray=True)

                similarity = ssim(img1, img2)
                logging.info(f'Similarity of two image: {similarity * 100:.2f}%')

                os.remove(self.product_img_path)

                return similarity >= self.threshold
            return False
        except Exception as e:
            logging.error('Image compare error:', str(e))
            return False

async def main():
    text1 = "Mielle Organics Rosemary Mint Scalp & Hair Strengthening Oil With Biotin & Essential Oils, Nourishing Treatment for Split Ends and Dry Scalp for All Hair Types, 2-Fluid Ounces"
    text2 = "Mielle Organics Rosemary Mint Scalp And Hair Strengthening Oil, 2 Oz By MyOTCStore"
    textComp = TextComparator(text1, text2)
    print('result:', await textComp.compare())

if __name__ == '__main__':
    asyncio.run(main())
