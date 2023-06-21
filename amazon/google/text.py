import asyncio
import difflib

class TextComparator:
    def __init__(self, text1: str, text2: str):
        self.text1 = text1
        self.text2 = text2

    def calculate_similarity(self):
        seq_matcher = difflib.SequenceMatcher(None, self.text1, self.text2)
        return seq_matcher.ratio()

    async def compare(self, threshold=0.85):
        try:
            loop = asyncio.get_running_loop()
            similarity = await loop.run_in_executor(None, self.calculate_similarity)
            print(f'Similarity of two text: {similarity * 100:.2f}%')
            return similarity >= threshold
        except Exception as e:
            print('Text compare error:', str(e))
            return False
        


async def main():
    text1 = "Mielle Organics Rosemary Mint Scalp & Hair Strengthening Oil With Biotin & Essential Oils, Nourishing Treatment for Split Ends and Dry Scalp for All Hair Types, 2-Fluid Ounces"
    text2 = "Mielle Organics Rosemary Mint Scalp And Hair Strengthening Oil, 2 Oz By MyOTCStore"
    textComp = TextComparator(text1, text2)
    print('result:', await textComp.compare())

if __name__ == '__main__':
    asyncio.run(main())
