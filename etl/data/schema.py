database_schema = {
    "raw_layer": {
        "products": {
            "columns": ["product_id", "name", "category", "base_price", "load_date"],
            "primary_keys": []
        },
        "orders": {
            "columns": ["order_id", "order_date", "customer_id", "load_date"],
            "primary_keys": []
        },
        "order_items": {
            "columns": ["order_id", "product_id", "quantity", "price", "load_date"],
            "primary_keys": []
        },
        "customers": {
            "columns": ["customer_id", "name", "city", "load_date"],
            "primary_keys": []
        }
    },
    "data_vault_layer": {
        "hubs": {
            "customers_hub": {
                "columns": ["customer_id", "load_date"],
                "primary_keys": ["customer_id"]
            },
            "products_hub": {
                "columns": ["product_id", "load_date"],
                "primary_keys": ["product_id"]
            },
            "orders_hub": {
                "columns": ["order_id", "load_date"],
                "primary_keys": ["order_id"]
            }
        },
        "links": {
            "order_customers_link": {
                "columns": [
                    {"name": "nk_order_customer", "fk": None},
                    {"name": "order_id", "fk": {"references": "orders_hub", "column": "order_id"}},
                    {"name": "customer_id", "fk": {"references": "customers_hub", "column": "customer_id"}},
                    "load_date"
                ],
                "primary_keys": ["nk_order_customer"]
            },
            "order_products_link": {
                "columns": [
                    {"name": "nk_order_products", "fk": None},
                    {"name": "order_id", "fk": {"references": "orders_hub", "column": "order_id"}},
                    {"name": "product_id", "fk": {"references": "products_hub", "column": "product_id"}},
                    "load_date"
                ],
                "primary_keys": ["nk_order_products"]
            }
        },
        "satellites": {
            "order_sat": {
                "columns": [
                    {"name": "nk_order_id", "fk": {"references": "orders_hub", "column": "order_id"}},
                    "order_date",
                    "load_date",
                    "end_date",
                    "hash_diff"
                ],
                "primary_keys": []
            },
            "customers_details_sat": {
                "columns": [
                    {"name": "customer_id", "fk": {"references": "customers_hub", "column": "customer_id"}},
                    "name",
                    "city",
                    "load_date",
                    "end_date",
                    "hash_diff"
                ],
                "primary_keys": []
            },
            "products_details_sat": {
                "columns": [
                    {"name": "product_id", "fk": {"references": "products_hub", "column": "product_id"}},
                    "name",
                    "category",
                    "quantity",
                    "base_price",
                    "load_date",
                    "end_date",
                    "hash_diff"
                ],
                "primary_keys": []
            }
        }
    }
}