from django.db import models
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import F, Value, CharField, IntegerField, JSONField, BooleanField, Count, Q, Case, When
from django.db.models.functions import Coalesce
from .models_keys import ValidKeys
from django.contrib.postgres.fields import ArrayField
from django.forms.models import model_to_dict

class DomainExchangeRate(models.Model):
    DOMAIN_CHOICES = [
        (1, "US"),  # United States
        (2, "GB"),  # United Kingdom
        (3, "DE"),  # Germany
        (4, "FR"),  # France
        (5, "JP"),  # Japan
        (6, "CA"),  # Canada
        (7, "CN"),  # China
        (8, "IT"),  # Italy
        (9, "ES"),  # Spain
        (10, "IN"), # India
        (11, "MX"), # Mexico
        (12, "BR"), # Brazil
    ]
    CURRENCY_CODES = {
        "US": "USD",  # United States
        "GB": "GBP",  # United Kingdom
        "DE": "EUR",  # Germany
        "FR": "EUR",  # France
        "JP": "JPY",  # Japan
        "CA": "CAD",  # Canada
        "CN": "CNY",  # China
        "IT": "EUR",  # Italy
        "ES": "EUR",  # Spain
        "IN": "INR",  # India
        "MX": "MXN",  # Mexico
        "BR": "BRL",  # Brazil
    }
    CURRENCY_SYMBOLS = {
        "US": "$",    # United States
        "GB": "£",    # United Kingdom
        "DE": "€",    # Germany
        "FR": "€",    # France
        "JP": "¥",    # Japan
        "CA": "C$",   # Canada
        "CN": "¥",    # China
        "IT": "€",    # Italy
        "ES": "€",    # Spain
        "IN": "₹",    # India
        "MX": "$",    # Mexico
        "BR": "R$",   # Brazil
    }
    domain_code = models.IntegerField(choices=DOMAIN_CHOICES, unique=True)
    domain_name = models.CharField(max_length=2)
    currency_code = models.CharField(max_length=3)
    exchange_rate = models.DecimalField(max_digits=10, decimal_places=4)

    class Meta:
        app_label = 'amazon'

class Product(models.Model):
    DOMAIN_CHOICES = [
        (1, "US"),  # United States
        (2, "GB"),  # United Kingdom
        (3, "DE"),  # Germany
        (4, "FR"),  # France
        (5, "JP"),  # Japan
        (6, "CA"),  # Canada
        (7, "CN"),  # China
        (8, "IT"),  # Italy
        (9, "ES"),  # Spain
        (10, "IN"), # India
        (11, "MX"), # Mexico
        (12, "BR"), # BRAZIL
    ]
    updated = models.BooleanField(default=True)
    #after this line is standart data but dont forget convert to KeepaTime to Date
    productType = models.IntegerField(blank=True, null=True)
    asin = models.CharField(max_length=10)
    title = models.TextField(null=True)
    domainId = models.PositiveSmallIntegerField(choices=DOMAIN_CHOICES)
    type = models.CharField(max_length=255, null=True, blank=True)
    hasReviews = models.BooleanField(default=False)
    trackingSince = models.BigIntegerField(null=True, blank=True)
    listedSince = models.BigIntegerField(null=True, blank=True)
    lastUpdate = models.BigIntegerField(null=True, blank=True)
    lastRatingUpdate = models.BigIntegerField(null=True, blank=True)
    lastPriceChange = models.BigIntegerField(null=True, blank=True)
    lastEbayUpdate = models.BigIntegerField(null=True, blank=True)
    imagesCSV = models.TextField(null=True)
    rootCategory = models.BigIntegerField(null=True, blank=True)
    categories = models.JSONField(null=True, blank=True)
    parentAsin = models.CharField(max_length=10, blank=True, null=True)
    variationCSV = models.TextField(blank=True, null=True)
    frequentlyBoughtTogether = models.JSONField(blank=True, null=True)
    eanList = models.JSONField(blank=True, null=True)
    upcList = models.JSONField(blank=True, null=True)
    manufacturer = models.CharField(max_length=255, blank=True, null=True)
    brand = models.CharField(max_length=255, blank=True, null=True)
    productGroup = models.CharField(max_length=255, blank=True, null=True)
    partNumber = models.CharField(max_length=255, blank=True, null=True)
    binding = models.CharField(max_length=255, blank=True, null=True)
    numberOfItems = models.IntegerField(null=True, blank=True)
    numberOfPages = models.IntegerField(null=True, blank=True)
    publicationDate = models.BigIntegerField(null=True, blank=True)
    releaseDate = models.BigIntegerField(null=True, blank=True)
    contributors = models.JSONField(null=True, blank=True)
    languages = models.JSONField(null=True, blank=True)
    model = models.CharField(max_length=255, blank=True, null=True)
    color = models.CharField(max_length=255, blank=True, null=True)
    size = models.CharField(max_length=255, blank=True, null=True)
    edition = models.CharField(max_length=255, blank=True, null=True)
    format = models.CharField(max_length=255, blank=True, null=True)
    features = models.JSONField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    packageHeight = models.IntegerField(null=True, blank=True)
    packageLength = models.IntegerField(null=True, blank=True)
    packageWidth = models.IntegerField(null=True, blank=True)
    packageWeight = models.IntegerField(null=True, blank=True)
    packageQuantity = models.IntegerField(null=True, blank=True)
    itemHeight = models.IntegerField(null=True, blank=True)
    itemLength = models.IntegerField(null=True, blank=True)
    itemWidth = models.IntegerField(null=True, blank=True)
    itemWeight = models.IntegerField(null=True, blank=True)
    availabilityAmazon = models.IntegerField(null=True, blank=True)
    availabilityAmazonDelay = models.JSONField(blank=True, null=True)
    ebayListingIds = models.JSONField(null=True, blank=True)
    isAdultProduct = models.BooleanField(default=False)
    launchpad = models.BooleanField(default=False)
    isB2B = models.BooleanField(default=False)
    audienceRating = models.CharField(max_length=255, blank=True, null=True)
    newPriceIsMAP = models.BooleanField(default=False)
    isEligibleForTradeIn = models.BooleanField(default=False)
    isEligibleForSuperSaverShipping = models.BooleanField(default=False)
    fbaFees = models.JSONField(null=True, blank=True)
    referralFeePercent = models.IntegerField(null=True, blank=True)
    coupon = models.JSONField(blank=True, null=True)
    promotions = models.JSONField(blank=True, null=True)
    salesRankReference = models.BigIntegerField(null=True, blank=True)
    salesRankReferenceHistory = models.JSONField(null=True, blank=True)
    salesRanks = models.JSONField(null=True, blank=True)
    rentalDetails = models.TextField(blank=True, null=True)
    rentalSellerId = models.CharField(max_length=255, null=True, blank=True)
    rentalPrices = models.JSONField(null=True, blank=True)
    liveOffersOrder = models.JSONField(null=True, blank=True)
    buyBoxSellerIdHistory = models.JSONField(null=True, blank=True)
    buyBoxUsedHistory = models.JSONField(null=True, blank=True)
    isRedirectASIN = models.BooleanField(default=False)
    isSNS = models.BooleanField(default=False)
    author = models.CharField(max_length=255, null=True, blank=True)
    offersSuccessful = models.BooleanField(default=False)
    g = models.IntegerField(null=True, blank=True)
    csv = models.JSONField(null=True, blank=True)

    class Meta:
        app_label = 'amazon'

class CategoryTree(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='category_tree', null=True)
    catId = models.BigIntegerField(null=True, blank=True)
    name = models.CharField(max_length=255, null=True)

    class Meta:
        app_label = 'amazon'

class Stats(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='stats', null=True)
    current = models.JSONField(null=True, blank=True)
    avg = models.JSONField(null=True, blank=True)
    avg30 = models.JSONField(null=True, blank=True)
    avg90 = models.JSONField(null=True, blank=True)
    avg180 = models.JSONField(null=True, blank=True)
    avg365= models.JSONField(null=True, blank=True)
    atIntervalStart = models.JSONField(null=True, blank=True)
    min = models.JSONField(null=True, blank=True)
    max = models.JSONField(null=True, blank=True)
    minInInterval = models.JSONField(null=True, blank=True)
    maxInInterval = models.JSONField(null=True, blank=True)
    outOfStockPercentageInInterval = models.JSONField(null=True, blank=True)
    outOfStockPercentage30 = models.JSONField(null=True, blank=True)
    outOfStockPercentage90 = models.JSONField(null=True, blank=True)
    lastOffersUpdate = models.BigIntegerField(null=True, blank=True)
    salesRankDrops30 = models.IntegerField(null=True, blank=True)
    salesRankDrops90 = models.IntegerField(null=True, blank=True)
    salesRankDrops180 = models.IntegerField(null=True, blank=True)
    salesRankDrops365 = models.IntegerField(null=True, blank=True)
    totalOfferCount = models.IntegerField(null=True, blank=True)
    tradeInPrice = models.IntegerField(null=True, blank=True)
    lightningDealInfo = models.JSONField(null=True, blank=True)
    #following fields are only set if the offers or buybox parameter was used
    buyBoxSellerId = models.CharField(max_length=255, null=True, blank=True)
    buyBoxPrice = models.IntegerField(null=True, blank=True)
    buyBoxShipping = models.IntegerField(null=True, blank=True)
    buyBoxIsUnqualified = models.BooleanField(default=False, null=True, blank=True)
    buyBoxIsShippable = models.BooleanField(default=False, null=True, blank=True)
    buyBoxIsPreorder = models.BooleanField(default=False, null=True, blank=True)
    buyBoxIsBackorder = models.BooleanField(default=False, null=True, blank=True)
    buyBoxIsFBA = models.BooleanField(default=False, null=True, blank=True)
    buyBoxIsAmazon = models.BooleanField(default=False, null=True, blank=True)
    buyBoxIsMAP = models.BooleanField(default=False, null=True, blank=True)
    buyBoxIsUsed = models.BooleanField(default=False, null=True, blank=True)
    buyBoxMinOrderQuantity = models.IntegerField(null=True, blank=True)
    buyBoxMaxOrderQuantity = models.IntegerField(null=True, blank=True)
    buyBoxCondition = models.IntegerField(null=True, blank=True)
    buyBoxAvailabilityMessage = models.CharField(max_length=255, null=True, blank=True)
    buyBoxShippingCountry = models.CharField(max_length=255, null=True, blank=True)
    buyBoxIsPrimeExclusive = models.BooleanField(default=False, null=True, blank=True)
    buyBoxIsPrimeEligible = models.BooleanField(default=False, null=True, blank=True)
    buyBoxIsPrimePantry = models.BooleanField(default=False, null=True, blank=True)
    buyBoxIsFreeShippingEligible = models.BooleanField(default=False, null=True, blank=True)
    buyBoxStats = models.JSONField(null=True, blank=True)
    buyBoxUsedStats = models.JSONField(null=True, blank=True)
    buyBoxUsedPrice = models.IntegerField(null=True, blank=True)
    buyBoxUsedShipping = models.IntegerField(null=True, blank=True)
    buyBoxUsedSellerId = models.CharField(max_length=255, null=True, blank=True)
    buyBoxIsWarehouseDeal = models.BooleanField(default=False, null=True, blank=True)
    buyBoxUsedIsFBA = models.BooleanField(default=False, null=True, blank=True)
    buyBoxUsedCondition = models.IntegerField(null=True, blank=True)
    #the following fields are only set if the offers parameter was used
    retrievedOfferCount = models.IntegerField(null=True, blank=True)
    isAddonItem = models.BooleanField(default=False, null=True, blank=True)
    sellerIdsLowestFBA = models.JSONField(null=True, blank=True)
    sellerIdsLowestFBM = models.JSONField(null=True, blank=True)
    offerCountFBA = models.IntegerField(null=True, blank=True)
    offerCountFBM = models.IntegerField(null=True, blank=True)

    class Meta:
        app_label = 'amazon'
    

class Variations(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='variations', null=True)
    asin = models.CharField(max_length=10, null=True)
    attributes = models.JSONField(null=True)

    class Meta:
        app_label = 'amazon'

class Offers(models.Model):
    CONDITION_CHOICES = [
        (0, "Unknown"),
        (1, "New"),
        (2, "Used - Like New"),
        (3, "Used - Very Good"),
        (4, "Used - Good"),
        (5, "Used - Acceptable"),
        (6, "Refurbished"),
        (7, "Collectible - Like New"),
        (8, "Collectible - Very Good"),
        (9, "Collectible - Good"),
        (10, "Collectible - Acceptable"),
        (11, "Rental"),
    ]

    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='offers', null=True)
    offerId = models.IntegerField(null=True, blank=True)
    lastSeen = models.BigIntegerField(null=True, blank=True)
    sellerId = models.CharField(max_length=255, null=True, blank=True)
    isPrime = models.BooleanField(default=False)
    isFBA = models.BooleanField(default=False)
    isMAP = models.BooleanField(default=False)
    isShippable = models.BooleanField(default=False)
    isAddonItem = models.BooleanField(default=False)
    isPreorder = models.BooleanField(default=False)
    isWarehouseDeal = models.BooleanField(default=False)
    isScam = models.BooleanField(default=False)
    shipsFromChina = models.BooleanField(default=False)
    isAmazon = models.BooleanField(default=False)
    isPrimeExcl = models.BooleanField(default=False)
    coupon = models.IntegerField(null=True, blank=True)
    condition = models.PositiveSmallIntegerField(choices=CONDITION_CHOICES)
    conditionComment = models.TextField(null=True, blank=True)
    offersCSV = models.JSONField(null=True, blank=True)
    primeExclCSV = models.JSONField(null=True, blank=True)

    class Meta:
        app_label = 'amazon'
    
class WalmartProduct(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='walmart_product', null=True)
    updated = models.BooleanField(default=True)
    walmartCode = models.CharField(max_length=24, null=True)
    pos = models.IntegerField(default=1)
    trackingSince = models.BigIntegerField(null=True, blank=True)
    lastUpdate = models.BigIntegerField(null=True, blank=True)
    lastRatingUpdate = models.BigIntegerField(null=True, blank=True)
    lastPriceChange = models.BigIntegerField(null=True, blank=True)
    source = models.CharField(default='walmart', max_length=255, blank=True, null=True)
    title = models.CharField(max_length=255, blank=True)
    priceCsv = ArrayField(models.CharField(max_length=24), blank=True, null=True)
    priceCurrent = models.CharField(max_length=24, blank=True, null=True)
    priceWas = models.CharField(max_length=24, blank=True, null=True)
    priceCurrency = models.CharField(default='USD', max_length=24, blank=True, null=True)
    imageUrl = models.CharField(max_length=500, blank=True, null=True)
    subscribePrice = models.CharField(max_length=24, blank=True, null=True)
    opportunity = models.BooleanField(default=False, blank=True, null=True)
    sellerStatus = models.CharField(max_length=255 ,blank=True, null=True)
    ratingCsv = ArrayField(models.CharField(max_length=24), blank=True, null=True)
    ratingsStart = models.IntegerField(blank=True, null=True)
    ratingsCount = models.IntegerField(blank=True, null=True)
    tags = ArrayField(models.CharField(max_length=100, blank=True), blank=True, null=True)

    class Meta:
        app_label = 'amazon'


class ProductService:
    @classmethod
    def validate_json(cls, json_object, valid_keys):
        invalid_keys = [key for key in json_object if key not in valid_keys]
        for key in invalid_keys:
            # print(key)
            json_object.pop(key, None)
        return json_object
    
    @classmethod
    def sync_bulk_create_or_update(cls, products):
        print('KEEPA: sync_bulk_create_or_update')
        if products:
            print('KEEPA: products data is available')
            for product_data in products:
                category_tree_data = product_data.get('categoryTree')
                stats_data = product_data.get('stats')

                product_data.pop('categoryTree', None)
                product_data.pop('stats', None)

                product_data = cls.validate_json(product_data, ValidKeys.product_keys)

                try:
                    product = Product.objects.get(asin=product_data.get('asin'), domainId=product_data.get('domainId'))
                    for field, value in product_data.items():
                        setattr(product, field, value)
                    product.save()
                    
                    if category_tree_data:
                        for cat_tree in category_tree_data:
                            cat_tree = cls.validate_json(cat_tree, ValidKeys.category_tree_keys)
                            CategoryTree.objects.update_or_create(product=product, catId=cat_tree.get('catId'), defaults=cat_tree)
                    
                    if stats_data:
                        stats_data = cls.validate_json(stats_data, ValidKeys.stats_keys)
                        Stats.objects.update_or_create(product=product, defaults=stats_data)
                        
                except ObjectDoesNotExist:
                    product = Product.objects.create(**product_data)
                    product.save()

                    if category_tree_data:
                        for cat_tree in category_tree_data:
                            cat_tree = cls.validate_json(cat_tree, ValidKeys.category_tree_keys)
                            CategoryTree.objects.update_or_create(product=product, catId=cat_tree.get('catId'), defaults=cat_tree)
                    
                    if stats_data:
                        stats_data = cls.validate_json(stats_data, ValidKeys.stats_keys)
                        Stats.objects.update_or_create(product=product, defaults=stats_data)

            print('KEEPA: products data stored')
        else:
            print('KEEAP: products data is not available!')

    @classmethod
    def get_all_data_for_discord(cls):
        asin_counts = Product.objects.values('asin').annotate(
            total_count=Count('domainId'),
            updated_count=Count('domainId', filter=Q(updated=True))
        ).filter(total_count=F('updated_count'))

        updated_asins = [item['asin'] for item in asin_counts]

        products = Product.objects.filter(asin__in=updated_asins).annotate(
            buyBoxPrice=Coalesce(F('stats__buyBoxPrice'), Value(0, IntegerField())),
            buyBoxShipping=Coalesce(F('stats__buyBoxShipping'), Value(0, IntegerField())),
            buyBoxIsFBA=Coalesce(F('stats__buyBoxIsFBA'), Value(False, BooleanField())),
            buyBoxIsAmazon=Coalesce(F('stats__buyBoxIsAmazon'), Value(False, BooleanField())),
            buyBoxAvailabilityMessage=Coalesce(F('stats__buyBoxAvailabilityMessage'), Value('N/A', CharField())),
        )

        product_list = []

        for product_model in products:
            product = model_to_dict(product_model, fields=[
                'asin', 'domainId', 'title', 'manufacturer', 'brand', 'packageHeight', 
                'packageLength', 'packageWidth', 'packageWeight', 'packageQuantity', 
                'itemHeight', 'itemLength', 'itemWidth', 'itemWeight', 'fbaFees', 
                'buyBoxPrice', 'buyBoxShipping', 'buyBoxIsFBA', 'buyBoxIsAmazon', 
                'buyBoxAvailabilityMessage', 'imagesCSV', 'rootCategory', 'salesRanks'
            ])

            product['buyBoxPrice'] = product_model.buyBoxPrice
            product['buyBoxShipping'] = product_model.buyBoxShipping
            product['buyBoxIsFBA'] = product_model.buyBoxIsFBA
            product['buyBoxIsAmazon'] = product_model.buyBoxIsAmazon
            product['buyBoxAvailabilityMessage'] = product_model.buyBoxAvailabilityMessage

            product['categoryTree'] = list(CategoryTree.objects.filter(product__asin=product['asin'], catId=product['rootCategory']).values())
                    
            try:
                domain_exchange_rate = DomainExchangeRate.objects.get(domain_code=product['domainId'])
                product['exchangeRate'] = str(domain_exchange_rate.exchange_rate)
                product['domainExchangeText'] = domain_exchange_rate.get_domain_code_display()
                product['domainExchangeSymbol'] = DomainExchangeRate.CURRENCY_SYMBOLS[domain_exchange_rate.domain_name]
                product_list.append(product)
            except DomainExchangeRate.DoesNotExist:
                pass

        if product_list:
            # print('all_product_list:', product_list)
            product_asin_domain_pairs = [(product['asin'], product['domainId']) for product in product_list]
            
            q_objects = Q()
            for asin, domainId in product_asin_domain_pairs:
                q_objects |= Q(asin=asin, domainId=domainId)

            Product.objects.filter(q_objects).update(updated=False)

        return product_list


    @classmethod
    def get_walmart_data_for_discord(cls):
        products = Product.objects.filter(domainId=1, walmart_product__updated=True).annotate(
            buyBoxPrice=Coalesce(F('stats__buyBoxPrice'), Value(0, IntegerField())),
            buyBoxShipping=Coalesce(F('stats__buyBoxShipping'), Value(0, IntegerField())),
            buyBoxIsFBA=Coalesce(F('stats__buyBoxIsFBA'), Value(False, BooleanField())),
            buyBoxIsAmazon=Coalesce(F('stats__buyBoxIsAmazon'), Value(False, BooleanField())),
            buyBoxAvailabilityMessage=Coalesce(F('stats__buyBoxAvailabilityMessage'), Value('N/A', CharField())),
        ).prefetch_related('walmart_product')

        product_list = []

        for product_model in products:
            product = model_to_dict(product_model, fields=[
                'asin', 'domainId', 'title', 'manufacturer', 'brand', 'packageHeight', 
                'packageLength', 'packageWidth', 'packageWeight', 'packageQuantity', 
                'itemHeight', 'itemLength', 'itemWidth', 'itemWeight', 'fbaFees', 
                'buyBoxPrice', 'buyBoxShipping', 'buyBoxIsFBA', 'buyBoxIsAmazon', 
                'buyBoxAvailabilityMessage',
                'imagesCSV', 'rootCategory', 'salesRanks'
            ])
            
            product['buyBoxPrice'] = product_model.buyBoxPrice
            product['buyBoxShipping'] = product_model.buyBoxShipping
            product['buyBoxIsFBA'] = product_model.buyBoxIsFBA
            product['buyBoxIsAmazon'] = product_model.buyBoxIsAmazon
            product['buyBoxAvailabilityMessage'] = product_model.buyBoxAvailabilityMessage

            product['categoryTree'] = list(CategoryTree.objects.filter(product__asin=product['asin'], catId=product['rootCategory']).values())

            related_walmart_products = product_model.walmart_product.filter(updated=True)
            product['walmartProduct'] = [model_to_dict(related_walmart_product, fields=['walmartCode', 'source', 'title', 'priceCurrent', 'imageUrl']) for related_walmart_product in related_walmart_products]

            try:
                domain_exchange_rate = DomainExchangeRate.objects.get(domain_code=product['domainId'])
                product['exchangeRate'] = str(domain_exchange_rate.exchange_rate)
                product['domainExchangeText'] = domain_exchange_rate.get_domain_code_display()
                product['domainExchangeSymbol'] = DomainExchangeRate.CURRENCY_SYMBOLS[domain_exchange_rate.domain_name]
                product_list.append(product)
            except DomainExchangeRate.DoesNotExist:
                pass

        if product_list:
            # print('walmart_product_list:', product_list)
            WalmartProduct.objects.filter(product__in=products).update(updated=False)

        return product_list
    
    @classmethod
    def sync_bulk_update_ecommerce(cls, products):
        if products:
            for product_data in products:
                try:
                    if product_data:
                        for walmartProduct in product_data:
                            product, created = Product.objects.get_or_create(asin=walmartProduct['asin'], domainId=1)
                            walmartProduct.pop('asin', None)
                            walmartProduct['product'] = product
                            WalmartProduct.objects.update_or_create(defaults=walmartProduct, walmartCode=walmartProduct['walmartCode'])
                except ObjectDoesNotExist:
                    pass
                except Exception as e:
                    print(f'Error: {str(e)}')

    @classmethod
    def get_search_data_for_ecommerce(cls):
        products = Product.objects.filter(domainId=1).values('asin', 'upcList', 'title')
        return list(products)