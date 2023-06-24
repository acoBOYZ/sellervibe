class TriggerService:
    @classmethod
    def control_loop(cls, bulk_data:list, config:dict, compare_value:int):
        nested_list = cls.get_all_keys_from_config(config)
        # print('nested_list:', nested_list)

        low_profit_color = (237, 27, 37)
        high_profit_color = (99, 188, 70)

        response = []

        for product in bulk_data:
            domainId = product.get('domainId', None)
            if not domainId or str(domainId) not in nested_list[1]:
                continue

            asin = product.get('asin', None)
            title = product.get('title', None)

            exchangeRate = product.get('exchangeRate', 1.0)
            exchangeSymbol = product.get('domainExchangeSymbol', 'N/A')
            if (exchangeRate == 'N/A') or (exchangeSymbol == 'N/A'):
                continue
            exchangeRate = float(exchangeRate)

            price = 0
            try:
                price = int(product.get('buyBoxPrice', 0))
            except:
                pass
            isAmazon = product.get('buyBoxIsAmazon', None)
            inStock = (str(product.get('buyBoxAvailabilityMessage', '')).lower() == "in stock.")
            image = ''
            image_list = str(product.get('imagesCSV', '')).split(',')
            if image_list:
                image = image_list[0]
            brand = product.get('brand', '')
            category = ''
            category_list = product.get('categoryTree', [])
            if category_list:
                category = category_list[0].get('name', '')

            if (asin) and (title) and (price) and (price > 0):
                walmartProdutc = product.get('walmartProduct', [])
                if not walmartProdutc:
                    continue
                for walmart in walmartProdutc:
                    w_code = walmart.get('walmartCode', None)
                    w_source = walmart.get('source', None)
                    w_title = walmart.get('title', None)
                    w_price = 0
                    try:
                        w_price = float(walmart.get('priceCurrent', 0))
                    except:
                        pass
                    w_image = walmart.get('imageUrl', None)
                    w_exchangeRate = 1.0

                    if not w_code or not w_source or not w_title or not w_price or not w_image:
                        continue

                    w_price *= 100
                    key = f'{w_source}_to_{domainId}'

                    p_price = (price * w_exchangeRate) / exchangeRate
                    co_price = (w_price * exchangeRate) / w_exchangeRate
                    depoFee = config.get(key).get('depoFee', 0) * w_exchangeRate
                    costOfInvestment = co_price + depoFee
                    netReturnOnInvestment = price - costOfInvestment
                    roi = round((100 * netReturnOnInvestment) / costOfInvestment, 2)

                    # print('w_price:', w_price, 'price:', price)
                    # print(co_price, depoFee, costOfInvestment, netReturnOnInvestment)
                    # print('roi:', roi)
                    
                    if roi < 0:
                        continue

                    if (roi > compare_value):
                        temp_config = config.get(key, None)
                        if temp_config:

                            rank = product.get('salesRanks', None)
                            if rank and isinstance(rank, dict):
                                rank = rank.get('rank', -1)
                                rank = rank if rank > 0 else 'N/A'
                            else:
                                rank = 'N/A'

                            color = cls.interpolate_color(low_profit_color, high_profit_color, roi / 100)
                            # print('color:', color, int(color, 16))
                                
                            cpy_config = temp_config.copy()
                            related_keys = {
                                f"__id__": f"{key}/{w_code}/{asin}",

                                f"{domainId}_asin": asin,
                                f"walmart_code": w_code,

                                f"{domainId}_title": title,
                                f"walmart_title": w_title,

                                f"{domainId}_price": f'{exchangeSymbol}{round(p_price / 100, 2)}',
                                f"walmart_price": f'{exchangeSymbol}{round(w_price / 100, 2)}',

                                f"{domainId}_seller": 'FBM' if isAmazon else 'FBA',

                                f"{domainId}_stock": product.get('buyBoxAvailabilityMessage', ''),

                                f"{domainId}_image": image,
                                f"walmart_image": w_image,

                                f"{domainId}_brand": brand,

                                f"{domainId}_category": category,

                                f"x_roi": roi,
                                f"x_rank": f"{rank}",
                                f"x_color": f"{color}"
                            }
                            cpy_config = cls.deep_replace(cpy_config, related_keys)
                            response.append(cpy_config)

        return response
    
    @classmethod
    def get_all_keys_from_config(cls, config):
        pairs = [key.split("_to_") for key in config.keys()]

        first_values = [pair[0] for pair in pairs]
        second_values = [pair[1] for pair in pairs]

        first_values = sorted(list(set(first_values)))
        second_values = sorted(list(set(second_values)))

        return [first_values, second_values]
    
    @classmethod
    def deep_replace(cls, obj, replacements):
        if isinstance(obj, dict):
            return {k: cls.deep_replace(v, replacements) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [cls.deep_replace(elem, replacements) for elem in obj]
        elif isinstance(obj, str):
            for k, v in replacements.items():
                obj = obj.replace('{' + k + '}', str(v))
            return obj
        else:
            return obj
        
    @classmethod
    def interpolate_color(cls, color1, color2, factor):
        """Interpolate between two RGB colors."""
        r1, g1, b1 = color1
        r2, g2, b2 = color2

        factor = factor if factor <= 1 else 1
        # print('factor:', factor)

        r = r1 + (r2 - r1) * factor
        g = g1 + (g2 - g1) * factor
        b = b1 + (b2 - b1) * factor

        return cls.rgb_to_hex((int(r), int(g), int(b)))
        
    @classmethod
    def rgb_to_hex(cls, rgb_color):
        """Convert RGB color to hex string."""
        return ''.join('{:02x}'.format(c) for c in rgb_color)