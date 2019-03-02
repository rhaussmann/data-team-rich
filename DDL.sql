DROP TABLE IF EXISTS public.dtr;

CREATE TABLE public.dtr
(
    index bigint,
    "Day" timestamp without time zone,
    "Customer ID" integer,
    "Campaign ID" integer,
    "Campaign" text COLLATE pg_catalog."default",
    "Campaign state" boolean,
    "Campaign serving status" text COLLATE pg_catalog."default",
    "Clicks" integer,
    "Start date" timestamp without time zone,
    "End date" timestamp without time zone,
    "Budget" money,
    "Budget ID" integer,
    "Budget explicitly shared" boolean,
    "Label IDs" text COLLATE pg_catalog."default",
    "Labels" text COLLATE pg_catalog."default",
    "Invalid clicks" integer,
    "Conversions" integer,
    "Conv. rate" double precision,
    "CTR" double precision,
    "Cost" money,
    "Impressions" integer,
    "Avg. position" double precision,
    "Interaction Rate" double precision,
    "Interactions" integer,
    "Search Lost IS rank" double precision
)

TABLESPACE pg_default;
