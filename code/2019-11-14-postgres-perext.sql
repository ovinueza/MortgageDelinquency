-- Table: public.perext

-- DROP TABLE public.perext;

CREATE TABLE public.perext
(
    "UniqueID" bigint NOT NULL,
    "LoanIdentifier" bigint,
    "MonthlyReportingPeriod" date,
    "LoanAge" smallint,
    "RemainingMonthstoMaturity" smallint,
    "AdjustedMonthstoMaturity" character varying(25) COLLATE pg_catalog."default",
    "MaturityDate" character varying(25) COLLATE pg_catalog."default",
    "MetropolitanStatisticalAreaMSA" bigint,
    "CurrentLoanDelinquencyStatus" character varying(15) COLLATE pg_catalog."default",
    "ForeclosureDate" character varying(25) COLLATE pg_catalog."default",
    CONSTRAINT perext_pkey PRIMARY KEY ("UniqueID"),
    CONSTRAINT "LoanIdentifier" FOREIGN KEY ("LoanIdentifier")
        REFERENCES public.acq ("LoanIdentifier") MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
)
WITH (
    OIDS = FALSE
)
TABLESPACE pg_default;

ALTER TABLE public.perext
    OWNER to postgres;