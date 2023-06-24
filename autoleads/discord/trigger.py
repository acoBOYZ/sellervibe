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
            if not domainId or domainId not in nested_list[0]:
                continue

            asin = product.get('asin', None)
            title = product.get('title', None)

            exchangeRate = product.get('exchangeRate', 1.0)
            exchangeSymbol = product.get('domainExchangeSymbol', 'N/A')
            if (exchangeRate == 'N/A') or (exchangeSymbol == 'N/A'):
                continue
            exchangeRate = float(exchangeRate)

            price = int(product.get('buyBoxPrice', 0))
            fbaFees = 0
            fbaFees_dict = product.get('fbaFees', None)
            if fbaFees_dict and isinstance(fbaFees_dict, dict):
                fbaFees = fbaFees_dict.get('pickAndPackFee', 0)
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
            # print('domainId:', domainId, 'asin:', asin, 'title:', title, 'price:', price, 'inStock:', inStock, 'buyBoxAvailabilityMessage:', product.get('buyBoxAvailabilityMessage', None))
            if (asin) and (title) and (price) and (price > 0) and (inStock): # and (isAmazon)
                for rp in bulk_data:
                    rp_domainId = rp.get('domainId', None)
                    if (not rp_domainId) or (rp_domainId not in nested_list[1]) or (rp_domainId == domainId):
                        continue

                    rp_asin = rp.get('asin', None)
                    if (not rp_asin) or (rp_asin != asin):
                        continue

                    rp_isFBA = rp.get('buyBoxIsFBA', None)
                    # if (not rp_isFBA):
                    #     continue

                    rp_exchangeRate = rp.get('exchangeRate', 1.0)
                    rp_exchangeSymbol = rp.get('domainExchangeSymbol', 'N/A')
                    if (rp_exchangeRate == 'N/A') or (rp_exchangeSymbol == 'N/A'):
                        continue
                    rp_exchangeRate = float(rp_exchangeRate)

                    rp_price = int(rp.get('buyBoxPrice', 0))
                    if (not rp_price) or (rp_price <= 0):
                        continue

                    key = f'{domainId}_to_{rp_domainId}'

                    co_price = (price * rp_exchangeRate) / exchangeRate
                    co_fbaFees = (fbaFees * rp_exchangeRate) / exchangeRate
                    depoFee = config.get(key).get('depoFee', 0) * rp_exchangeRate
                    costOfInvestment = co_price + co_fbaFees + depoFee
                    netReturnOnInvestment = rp_price - costOfInvestment
                    roi = round((100 * netReturnOnInvestment) / costOfInvestment, 2)
                    
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

                            rp_rank = rp.get('salesRanks', None)
                            if rp_rank and isinstance(rp_rank, dict):
                                rp_rank = rp_rank.get('rank', -1)
                                rp_rank = rp_rank if rp_rank > 0 else 'N/A'
                            else:
                                rp_rank = 'N/A'

                            color = cls.interpolate_color(low_profit_color, high_profit_color, roi / 100)
                            # print('color:', color, int(color, 16))
                                
                            cpy_config = temp_config.copy()
                            related_keys = {
                                f"__id__": f"{key}/{asin}/{rp_asin}",

                                f"{domainId}_asin": asin,
                                f"{rp_domainId}_asin": rp_asin,

                                f"{domainId}_title": title,
                                f"{rp_domainId}_title": title,

                                f"{domainId}_price_org": f'{exchangeSymbol}{round(price / 100, 2)}',
                                f"{domainId}_price": f'{rp_exchangeSymbol}{round(co_price / 100, 2)}',
                                f"{rp_domainId}_price": f'{rp_exchangeSymbol}{round(rp_price / 100, 2)}',

                                f"{domainId}_seller": 'FBM' if isAmazon else 'FBA',
                                f"{rp_domainId}_seller": 'FBM' if not rp_isFBA else 'FBA',

                                f"{domainId}_stock": product.get('buyBoxAvailabilityMessage', ''),
                                f"{rp_domainId}_stock": rp.get('buyBoxAvailabilityMessage', ''),

                                f"{domainId}_image": image,
                                f"{rp_domainId}_image": image,

                                f"{domainId}_brand": brand,
                                f"{rp_domainId}_brand": brand,

                                f"{domainId}_category": category,
                                f"{rp_domainId}_category": category,

                                f"{domainId}_rank": f"{rank}",
                                f"{rp_domainId}_rank": f"{rp_rank}",

                                f"x_roi": roi,
                                f"x_color": f"{color}"
                            }
                            cpy_config = cls.deep_replace(cpy_config, related_keys)
                            response.append(cpy_config)

        return response
    
    @classmethod
    def get_all_keys_from_config(cls, config):
        pairs = [key.split("_to_") for key in config.keys()]

        first_values = [int(pair[0]) for pair in pairs]
        second_values = [int(pair[1]) for pair in pairs]

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