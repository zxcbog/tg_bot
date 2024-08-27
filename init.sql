ALTER USER postgres WITH PASSWORD '1';

-- Переключаемся на базу данных postgres
\c postgres;

-- Table: public.users

-- DROP TABLE IF EXISTS public.users;

CREATE TABLE IF NOT EXISTS public.users
(
    phone_number text COLLATE pg_catalog."default" NOT NULL,
    first_name text COLLATE pg_catalog."default" NOT NULL,
    telegram_user_id bigint NOT NULL,
    last_name text COLLATE pg_catalog."default" NOT NULL,
    CONSTRAINT users_pkey PRIMARY KEY (telegram_user_id)
)
TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.users
    OWNER to postgres;

-- Table: public.orders

-- DROP TABLE IF EXISTS public.orders;

CREATE TABLE IF NOT EXISTS public.orders
(
    order_id bigint NOT NULL GENERATED ALWAYS AS IDENTITY ( INCREMENT 1 START 1 MINVALUE 1 MAXVALUE 9223372036854775807 CACHE 1 ),
    sending_city text COLLATE pg_catalog."default" NOT NULL,
    delivery_city text COLLATE pg_catalog."default" NOT NULL,
    org_name text COLLATE pg_catalog."default" NOT NULL,
    loading_address text COLLATE pg_catalog."default" NOT NULL,
    orientier text COLLATE pg_catalog."default" NOT NULL,
    delivery_packaging text COLLATE pg_catalog."default" NOT NULL,
    total_weight text COLLATE pg_catalog."default" NOT NULL,
    delivery_type text COLLATE pg_catalog."default" NOT NULL,
    payment_type text COLLATE pg_catalog."default" NOT NULL,
    telegram_user_id bigint NOT NULL,
    loading_datetime text COLLATE pg_catalog."default" NOT NULL,
    loader_worker_contact text COLLATE pg_catalog."default" NOT NULL,
    delivery_count bigint NOT NULL,
    delivery_datetime text COLLATE pg_catalog."default" NOT NULL,
    accepted boolean NOT NULL DEFAULT false,
    CONSTRAINT orders_pkey PRIMARY KEY (order_id),
    CONSTRAINT user_id FOREIGN KEY (telegram_user_id)
        REFERENCES public.users (telegram_user_id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
        NOT VALID
)
TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.orders
    OWNER to postgres;
