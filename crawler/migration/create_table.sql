CREATE TABLE IF NOT EXISTS crawler.product (
            platform text NULL,
            category text NOT NULL,
            product_id text NOT NULL,
            product_name text NULL,
            price float8 NULL,
            original_price float8 NULL,
            discount_rate float8 NULL,
            seller_id text NOT NULL,
            seller_name text NULL,
            brand_id text NULL,
            brand_name text NULL,
            rating_average float8 NULL,
            review_count int4 NULL,
            url_path text NULL,
            CONSTRAINT product_pkey PRIMARY KEY (category, product_id, url_path, seller_id)
            );