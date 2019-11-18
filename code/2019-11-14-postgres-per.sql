-- Table: public.per

-- DROP TABLE public.per;

CREATE TABLE public.per
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
    CONSTRAINT "UniqueID" PRIMARY KEY ("UniqueID"),
    CONSTRAINT "LoanIdentifier" FOREIGN KEY ("LoanIdentifier")
        REFERENCES public.acq ("LoanIdentifier") MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
)
WITH (
    OIDS = FALSE
)
TABLESPACE pg_default;

ALTER TABLE public.per
    OWNER to postgres;