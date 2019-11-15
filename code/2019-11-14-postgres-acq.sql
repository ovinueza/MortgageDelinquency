-- Table: public.acq

-- DROP TABLE public.acq;

CREATE TABLE public.acq
(
    "LoanIdentifier" bigint NOT NULL,
    "SellerName" character varying(75) COLLATE pg_catalog."default",
    "OriginalInterestRate" numeric(5,3),
    "OriginalUPB" bigint,
    "OriginalLoanTerm" smallint,
    "OriginationDate" character varying(25) COLLATE pg_catalog."default",
    "FirstPaymentDate" character varying(25) COLLATE pg_catalog."default",
    "OriginalLoanToValueLTV" smallint,
    "PrimaryMortgageInsurancePercent" numeric(15,2),
    "OriginalDebtToIncomeRatio" character varying(25) COLLATE pg_catalog."default",
    "NumberofBorrowers" smallint,
    "FirstTimeHomeBuyerIndicator" smallint,
    "BorrowerCreditScoreAtOrigination" character varying(25) COLLATE pg_catalog."default",
    "PropertyState" character varying(2) COLLATE pg_catalog."default",
    "ZipCodeShort" smallint,
    "CoBorrowerCreditScoreAtOrigination" character varying(25) COLLATE pg_catalog."default",
    CONSTRAINT acq_pkey PRIMARY KEY ("LoanIdentifier")
)
WITH (
    OIDS = FALSE
)
TABLESPACE pg_default;

ALTER TABLE public.acq
    OWNER to postgres;