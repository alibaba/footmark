from footmark.market.productobject import TaggedPRODUCTObject


class Product(TaggedPRODUCTObject):
    def __init__(self, connection=None):
        super(Product, self).__init__(connection)

    def __repr__(self):
        return 'Product:%s' % self.id

    def __getattr__(self, name):
        if name == 'price':
            return self.suggested_price

    def __setattr__(self, name, value):
        super(TaggedPRODUCTObject, self).__setattr__(name, value)

    def get(self):
        return self.connection.describe_product(code=self.code)

    def read(self):
        product = {}
        for name, value in list(self.__dict__.items()):
            if name in ["connection", "region_id", "region", "request_id", "description", "product_extras","shop_info", "pic_url"]:
                continue
            if name == 'product_skus':
                for m in value['product_sku'][0]['modules']['module']:
                    if m['code'] == 'img_id':
                        res = m['properties']['property'][0]['property_values']['property_value']
                product['image_ids'] = res
                continue
            product[name] = value
        return product

