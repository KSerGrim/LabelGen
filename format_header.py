searchingHeaders = {
    "order-id": "notes",
    "recipient-name":  "to_name",
    "ship-address-1": "to_address1",
    "ship-address-2": "to_address2",
    "ship-address-3": "to_address3",
    "ship-city": "to_city",
    "ship-state": "to_state",
    "ship-postal-code": "to_postcode",
    "ship-country": "to_country"
}

default_headers = {
    "provider": "upsv2",
    "class": "ups_ground",
    "weight": 48,
    "from_name": "FULFILLMENT",
    "from_company": "FULFILLMENT",
    "from_phone": "9257508950",
    "from_address1": "2470 AIRPORT BLVD",
    "from_address2": "",
    "from_city": "AURORA",
    "from_state": "CO",
    "from_postcode": "80011",
    "from_country": "US",
    "to_company": "",  # Assuming to keep empty if not a business order
    "length": 18,
    "width": 14,
    "height": 8,
}

formatted_headers = {
    "provider": "upsv2",
    "class": "ups_ground",
    "weight": 48,
    "order-id": "notes", #
    "from_name": "FULFILLMENT",
    "from_company": "FULFILLMENT",
    "from_phone": "9257508950",
    "from_address1": "2470 AIRPORT BLVD",
    "from_address2": "",
    "from_city": "AURORA",
    "from_state": "CO",
    "from_postcode": "80011",
    "from_country": "US",
    "recipient-name": "to_name", #
    "to_company": "",
    "buyer-phone-number": "to_phone",
    "ship-address-1": "to_address1", #
    "ship-address-2": "to_address2", #
    "ship-address-3": "to_address3", #
    "ship-city": "to_city", #
    "ship-state": "to_state", #
    "ship-postal-code": "to_postcode",#
    "ship-country": "to_country", #
    "length": 18,
    "width": 14,
    "height": 8,
}

shipd_headers = {
    "AmazonOrderId": "order-id",
}