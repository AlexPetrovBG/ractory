--
-- PostgreSQL database dump
--

-- Dumped from database version 15.12
-- Dumped by pg_dump version 16.9 (Ubuntu 16.9-0ubuntu0.24.04.1)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: workflowactiontype; Type: TYPE; Schema: public; Owner: rafactory_rw
--

CREATE TYPE public.workflowactiontype AS ENUM (
    'BarcodeScan',
    'PieceCut',
    'AssemblyWeld',
    'QualityCheck',
    'Packaging',
    'Shipping',
    'MaterialRequest',
    'MaterialReceived',
    'WorkstationLogin',
    'WorkstationLogout',
    'ErrorReport',
    'MaintenanceRequest',
    'SystemEvent'
);


ALTER TYPE public.workflowactiontype OWNER TO rafactory_rw;

--
-- Name: update_updated_at_column(); Type: FUNCTION; Schema: public; Owner: rafactory_rw
--

CREATE FUNCTION public.update_updated_at_column() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
        BEGIN
            NEW.updated_at = CURRENT_TIMESTAMP;
            RETURN NEW;
        END;
        $$;


ALTER FUNCTION public.update_updated_at_column() OWNER TO rafactory_rw;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: alembic_version; Type: TABLE; Schema: public; Owner: rafactory_rw
--

CREATE TABLE public.alembic_version (
    version_num character varying(32) NOT NULL
);


ALTER TABLE public.alembic_version OWNER TO rafactory_rw;

--
-- Name: api_keys; Type: TABLE; Schema: public; Owner: rafactory_rw
--

CREATE TABLE public.api_keys (
    guid uuid NOT NULL,
    company_guid uuid NOT NULL,
    key_hash character varying NOT NULL,
    description character varying,
    scopes character varying,
    is_active boolean NOT NULL,
    created_at timestamp with time zone DEFAULT now() NOT NULL,
    last_used_at timestamp with time zone,
    updated_at timestamp with time zone
);


ALTER TABLE public.api_keys OWNER TO rafactory_rw;

--
-- Name: articles; Type: TABLE; Schema: public; Owner: rafactory_rw
--

CREATE TABLE public.articles (
    code character varying NOT NULL,
    designation character varying,
    consume_group_designation character varying,
    consume_group_priority integer,
    quantity double precision,
    unit character varying,
    category_designation character varying,
    "position" character varying,
    short_position character varying,
    code_no_color character varying,
    component_code character varying,
    is_extra boolean,
    length double precision,
    width double precision,
    height double precision,
    surface double precision,
    angle1 double precision,
    angle2 double precision,
    unit_weight double precision,
    bar_length double precision,
    company_guid uuid NOT NULL,
    created_at timestamp with time zone DEFAULT now() NOT NULL,
    updated_at timestamp with time zone,
    guid uuid NOT NULL,
    project_guid uuid NOT NULL,
    component_guid uuid NOT NULL,
    is_active boolean DEFAULT true NOT NULL,
    deleted_at timestamp with time zone
);


ALTER TABLE public.articles OWNER TO rafactory_rw;

--
-- Name: assemblies; Type: TABLE; Schema: public; Owner: rafactory_rw
--

CREATE TABLE public.assemblies (
    trolley_cell character varying,
    trolley character varying,
    cell_number integer,
    picture bytea,
    company_guid uuid NOT NULL,
    created_at timestamp with time zone DEFAULT now() NOT NULL,
    updated_at timestamp with time zone,
    guid uuid NOT NULL,
    project_guid uuid NOT NULL,
    component_guid uuid NOT NULL,
    is_active boolean DEFAULT true NOT NULL,
    deleted_at timestamp with time zone
);


ALTER TABLE public.assemblies OWNER TO rafactory_rw;

--
-- Name: companies; Type: TABLE; Schema: public; Owner: rafactory_rw
--

CREATE TABLE public.companies (
    guid uuid NOT NULL,
    name character varying NOT NULL,
    short_name character varying,
    logo_path character varying,
    is_active boolean NOT NULL,
    created_at timestamp with time zone DEFAULT now() NOT NULL,
    updated_at timestamp with time zone,
    company_index integer,
    CONSTRAINT company_index_range CHECK (((company_index >= 0) AND (company_index <= 99)))
);


ALTER TABLE public.companies OWNER TO rafactory_rw;

--
-- Name: components; Type: TABLE; Schema: public; Owner: rafactory_rw
--

CREATE TABLE public.components (
    code character varying NOT NULL,
    designation character varying,
    quantity integer NOT NULL,
    picture bytea,
    company_guid uuid NOT NULL,
    created_at timestamp with time zone DEFAULT now() NOT NULL,
    updated_at timestamp with time zone,
    guid uuid NOT NULL,
    project_guid uuid NOT NULL,
    is_active boolean DEFAULT true NOT NULL,
    deleted_at timestamp with time zone
);


ALTER TABLE public.components OWNER TO rafactory_rw;

--
-- Name: pieces; Type: TABLE; Schema: public; Owner: rafactory_rw
--

CREATE TABLE public.pieces (
    piece_id character varying NOT NULL,
    outer_length integer,
    angle_left integer,
    angle_right integer,
    orientation character varying,
    barcode character varying,
    assembly_width integer,
    assembly_height integer,
    trolley character varying,
    cell character varying,
    trolley_cell character varying,
    operations character varying,
    component_code character varying,
    component_description character varying,
    info2 character varying,
    info3 character varying,
    client character varying,
    dealer character varying,
    project_description character varying,
    inner_length integer,
    reinforcement_code character varying,
    reinforcement_length integer,
    hardware_info character varying,
    glass_info character varying,
    other_length integer,
    project_number character varying,
    component_number character varying,
    water_handle character varying,
    segment_order character varying,
    cutting_pattern character varying,
    fixing_mode character varying,
    material_type character varying,
    project_code_parent character varying,
    bar_id character varying,
    bar_rest integer,
    bar_length integer,
    bar_cutting_tolerance integer,
    profile_code character varying,
    profile_name character varying,
    lamination character varying,
    gasket character varying,
    profile_width integer,
    profile_height integer,
    welding_tolerance integer,
    profile_color character varying,
    profile_type_ra character varying,
    profile_type character varying,
    trolley_size character varying,
    profile_code_with_color character varying,
    parent_assembly_trolley_cell character varying,
    mullion_trolley_cell character varying,
    glazing_bead_trolley_cell character varying,
    picture bytea,
    project_phase character varying,
    company_guid uuid NOT NULL,
    created_at timestamp with time zone DEFAULT now() NOT NULL,
    updated_at timestamp with time zone,
    guid uuid NOT NULL,
    project_guid uuid NOT NULL,
    component_guid uuid NOT NULL,
    assembly_guid uuid,
    is_active boolean DEFAULT true NOT NULL,
    deleted_at timestamp with time zone
);


ALTER TABLE public.pieces OWNER TO rafactory_rw;

--
-- Name: projects; Type: TABLE; Schema: public; Owner: rafactory_rw
--

CREATE TABLE public.projects (
    code character varying NOT NULL,
    updated_at timestamp with time zone,
    due_date timestamp with time zone,
    in_production boolean,
    company_name character varying,
    company_guid uuid NOT NULL,
    created_at timestamp with time zone DEFAULT now() NOT NULL,
    guid uuid NOT NULL,
    is_active boolean DEFAULT true NOT NULL,
    deleted_at timestamp with time zone
);


ALTER TABLE public.projects OWNER TO rafactory_rw;

--
-- Name: ui_templates; Type: TABLE; Schema: public; Owner: rafactory_rw
--

CREATE TABLE public.ui_templates (
    id integer NOT NULL,
    company_guid uuid NOT NULL,
    workstation_guid uuid,
    name character varying NOT NULL,
    json_data json NOT NULL,
    created_at timestamp with time zone DEFAULT now() NOT NULL,
    updated_at timestamp with time zone
);


ALTER TABLE public.ui_templates OWNER TO rafactory_rw;

--
-- Name: ui_templates_id_seq; Type: SEQUENCE; Schema: public; Owner: rafactory_rw
--

CREATE SEQUENCE public.ui_templates_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.ui_templates_id_seq OWNER TO rafactory_rw;

--
-- Name: ui_templates_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: rafactory_rw
--

ALTER SEQUENCE public.ui_templates_id_seq OWNED BY public.ui_templates.id;


--
-- Name: users; Type: TABLE; Schema: public; Owner: rafactory_rw
--

CREATE TABLE public.users (
    guid uuid NOT NULL,
    company_guid uuid NOT NULL,
    email character varying NOT NULL,
    pwd_hash character varying NOT NULL,
    role character varying NOT NULL,
    pin character varying(6),
    is_active boolean NOT NULL,
    created_at timestamp with time zone DEFAULT now() NOT NULL,
    updated_at timestamp with time zone,
    name character varying,
    surname character varying,
    picture_path character varying
);


ALTER TABLE public.users OWNER TO rafactory_rw;

--
-- Name: workflow; Type: TABLE; Schema: public; Owner: rafactory_rw
--

CREATE TABLE public.workflow (
    guid uuid NOT NULL,
    company_guid uuid NOT NULL,
    company_name character varying,
    workstation_guid uuid,
    workstation_name character varying,
    api_key_guid uuid,
    user_guid uuid,
    user_name character varying,
    action_type public.workflowactiontype NOT NULL,
    action_value character varying,
    created_at timestamp with time zone DEFAULT now() NOT NULL,
    updated_at timestamp with time zone
);


ALTER TABLE public.workflow OWNER TO rafactory_rw;

--
-- Name: workstations; Type: TABLE; Schema: public; Owner: rafactory_rw
--

CREATE TABLE public.workstations (
    guid uuid NOT NULL,
    company_guid uuid NOT NULL,
    location character varying NOT NULL,
    type character varying NOT NULL,
    is_active boolean NOT NULL,
    created_at timestamp with time zone DEFAULT now() NOT NULL,
    updated_at timestamp with time zone
);


ALTER TABLE public.workstations OWNER TO rafactory_rw;

--
-- Name: ui_templates id; Type: DEFAULT; Schema: public; Owner: rafactory_rw
--

ALTER TABLE ONLY public.ui_templates ALTER COLUMN id SET DEFAULT nextval('public.ui_templates_id_seq'::regclass);


--
-- Data for Name: alembic_version; Type: TABLE DATA; Schema: public; Owner: rafactory_rw
--

COPY public.alembic_version (version_num) FROM stdin;
c6c952dd3308
\.


--
-- Data for Name: api_keys; Type: TABLE DATA; Schema: public; Owner: rafactory_rw
--

COPY public.api_keys (guid, company_guid, key_hash, description, scopes, is_active, created_at, last_used_at, updated_at) FROM stdin;
d4828f42-d472-41e8-b660-75c16944a94b	8cf127b5-e93d-4d62-a922-cb1bab0f424e	$2b$12$m6nNOrHf5r3sDjQkf53PleQ.nKWkBkDHwmcjShle07zp1BvtZTzEu	Test API Key	sync:read,sync:write	t	2025-05-22 08:44:31.222193+00	2025-05-22 08:48:47.471234+00	2025-05-22 08:48:47.136959+00
32350a4d-ea36-4c08-ae3f-ba06f4cdf44d	8cf127b5-e93d-4d62-a922-cb1bab0f424e	$2b$12$6I8Br/6vcoBdrII6BWg9BO7b2UxoAsFek/lfs5B8/0MyHaD/MFLn.	Test Integration	sync:read,sync:write	t	2025-05-22 07:47:41.305873+00	2025-05-22 07:49:38.181621+00	2025-05-22 07:49:37.602584+00
16ca0edf-341a-4fea-9190-0a7dcf284a8c	c23d70ac-6fb9-4815-b56e-74de4fc2650b	$2b$12$p3KuEv6vU6o6EQAbmvl62uuXT.sGSZGjuKbnaCEKizdrrgkVi5vDK	Test Isolation Key	sync:read,sync:write	t	2025-05-22 08:09:04.320821+00	\N	\N
17253a3a-1d47-484c-a334-b0bd62493fe8	8cf127b5-e93d-4d62-a922-cb1bab0f424e	$2b$12$QwHZ92krx3N3XrDgJG./2.hoDUyAEQ4uqyZCk5r.4zmTqp3EjTfOm	Isolation Test Key	sync:read,sync:write	t	2025-05-22 08:09:38.739587+00	\N	\N
469ae60c-f162-4e0b-b98d-53d10dbc33c2	c23d70ac-6fb9-4815-b56e-74de4fc2650b	$2b$12$WaiY.YWaNVnGDh1owHVJNuP8fJqLV5Ci2j/S4O3c5RtWEse0.Ma.a	Test API Key	sync:read,sync:write	t	2025-05-22 08:44:17.523057+00	2025-05-22 08:50:13.482014+00	2025-05-22 08:50:11.876755+00
43af60cc-fff3-44a7-9de7-9290c1cd7832	c23d70ac-6fb9-4815-b56e-74de4fc2650b	$2b$12$.wnmg0eCudamaQnTqSHkFO7OUTFtZ2gUECu2MEIvQ41IH16YpJyXG	Isolation Test Key 2	sync:read,sync:write	t	2025-05-22 08:09:11.012176+00	2025-05-22 08:10:22.372748+00	2025-05-22 08:10:21.040663+00
15d90f68-5fb3-4fd7-bb7a-ab236e27f2c3	8cf127b5-e93d-4d62-a922-cb1bab0f424e	$2b$12$rQSs0B5bzW2BPwxqiNKFDOYPjWQHfsPB2.Lj9//KCwqBb4IZ.jydS	Isolation Test	sync:read,sync:write	t	2025-05-22 08:10:37.469249+00	\N	\N
4c101e59-4310-4ff9-b03f-9fd255617506	8cf127b5-e93d-4d62-a922-cb1bab0f424e	$2b$12$7X6pUqrzPfKz/X2h9cD1AOw3oHW6S.mLJ1QQQmtt49QGdPlFA5TnK	Test Integration for Company B	sync:read,sync:write	t	2025-05-22 08:21:18.626864+00	2025-05-22 08:29:55.54419+00	2025-05-22 08:29:53.90316+00
0490ab0d-9c9d-47af-9055-a920c8161bf7	c23d70ac-6fb9-4815-b56e-74de4fc2650b	$2b$12$w5Ep6BkrWhgHcsjwpduMR.QeMhgZN3u8IKP5IExINcnXfBs06zmcK	Isolation Test	sync:read,sync:write	t	2025-05-22 08:10:37.107987+00	2025-05-22 08:10:42.167493+00	2025-05-22 08:10:40.628621+00
79f76edf-76f9-4874-aa6f-2a1c4563575e	8cf127b5-e93d-4d62-a922-cb1bab0f424e	$2b$12$1Dc4qWpNAe/gozYwBEZEcea8pyGTWpK7ud562/o9OZRGWSNK5KtPG	Isolation Test	sync:read,sync:write	t	2025-05-22 08:50:39.245511+00	\N	\N
2f373c5d-df2c-4e57-9e3d-50635b1f9992	c23d70ac-6fb9-4815-b56e-74de4fc2650b	$2b$12$Rfjw7SvwsPF7YQ9dQZ0MAeqSvIZNseJ2G5wi4DZkACVjCYjN9pVKK	Isolation Test	sync:read,sync:write	t	2025-05-22 08:50:38.95334+00	2025-05-22 08:50:46.997118+00	2025-05-22 08:50:44.384265+00
2e00aafc-6070-4f65-a603-84b989be8520	c23d70ac-6fb9-4815-b56e-74de4fc2650b	$2b$12$CqoYOd4r6Izh5tS5WcFQau6SvZk48GLi.Fq/rkS3zBLfdJGatEbSa	Test Integration for Company A	sync:read,sync:write	t	2025-05-22 08:21:10.784596+00	2025-05-22 08:39:00.808227+00	2025-05-22 08:38:58.84997+00
32a46f5e-774b-47ea-80f9-1b30b73111e7	c23d70ac-6fb9-4815-b56e-74de4fc2650b	$2b$12$leAU4GjhpeJ6XIMk70wSkOfWsXT8nKgObbpq/FUhY9Nk5TCwIafWW	Test API Key	sync:read,sync:write	t	2025-05-22 08:14:21.19438+00	2025-05-22 08:15:01.116559+00	2025-05-22 08:14:59.400093+00
e553597c-8c26-47cf-b3f7-da1b8ea0d3cd	c23d70ac-6fb9-4815-b56e-74de4fc2650b	$2b$12$IsEFNgw4tk8KrNTH.eZpiO4ToFPcWaEo7f1h2P14fUUmCQ.W1SA8m	Test API Key	sync:read,sync:write	t	2025-05-22 08:13:35.009038+00	2025-05-22 08:14:12.303092+00	2025-05-22 08:14:10.56874+00
f5e31932-14cb-494c-bc6f-bcbdd6a52ee1	8cf127b5-e93d-4d62-a922-cb1bab0f424e	$2b$12$TM2sTlPP00RCebw7OWN9B.7f5DxDJL0f7DNDSVDy5jluMqoQ4i.sa	Test API Key	sync:read,sync:write	t	2025-05-22 08:13:35.402289+00	2025-05-22 08:14:14.085813+00	2025-05-22 08:14:12.352611+00
4d4f55b9-5705-43d8-b12b-c7e391f40221	8cf127b5-e93d-4d62-a922-cb1bab0f424e	$2b$12$F74.yRq6IL0eXi2LPHO8CuyA9.RdvdwfYX7bGeclOcthCl3K1AS5S	Test API Key	sync:read,sync:write	t	2025-05-22 08:10:49.823932+00	2025-05-22 08:11:13.58996+00	2025-05-22 08:11:11.837943+00
2798b1d3-35eb-4a56-9987-94b7e162aa77	c23d70ac-6fb9-4815-b56e-74de4fc2650b	$2b$12$JKG6zPrD7wItqjhHlyFIjerlwI2lMYgCX0OTF4fgBc2lkZKYbrpAO	Test API Key	sync:read,sync:write	t	2025-05-22 08:10:49.525682+00	2025-05-22 08:11:15.383816+00	2025-05-22 08:11:13.639748+00
fadf5197-d4d0-429e-851d-cb9858c9a3c4	c23d70ac-6fb9-4815-b56e-74de4fc2650b	$2b$12$LHRfttFU4X8.mKPS7VhCROVf54Xg/Jo8bc5Hb0rdUcnh63YzdRWNO	Test API Key	sync:read,sync:write	t	2025-05-22 08:11:19.864226+00	2025-05-22 08:11:51.216328+00	2025-05-22 08:11:49.471749+00
d1c17421-fb86-4b67-8b7e-2294d84e278f	8cf127b5-e93d-4d62-a922-cb1bab0f424e	$2b$12$RWGj.YqAqzhZvBadYYcHweZtA.ClWk1pFG4RmjqspkBuU7me.V8lO	Test API Key	sync:read,sync:write	t	2025-05-22 08:11:20.136785+00	2025-05-22 08:11:53.035985+00	2025-05-22 08:11:51.265725+00
b2f43502-780a-4d78-b5ee-53f9622ddbe8	8cf127b5-e93d-4d62-a922-cb1bab0f424e	$2b$12$NwrGHKixqExBpELxJDlzgOHf0GqjdSRjXVSxn8u228GNN3thzZcPC	Test API Key	sync:read,sync:write	t	2025-05-22 08:14:21.486783+00	2025-05-22 08:15:02.904896+00	2025-05-22 08:15:01.16534+00
7da9f79b-8e2a-423c-9016-1288aa75fb49	c23d70ac-6fb9-4815-b56e-74de4fc2650b	$2b$12$eH8hEWSX/oTMgeeDDmWxbOhERNz8VmESvcVR29uDeGwAC7wnWEK8a	Test API Key	sync:read,sync:write	t	2025-05-22 08:50:54.776684+00	2025-05-22 08:51:36.7271+00	2025-05-22 08:51:34.108233+00
e034c613-3487-47f7-9b3a-4d6611fe2413	8cf127b5-e93d-4d62-a922-cb1bab0f424e	$2b$12$JkJFUGjAr/g2yAP8IQtFN.tCbWXjO2s4Mcgr2XN47fRK5wKVLoTGS	Test API Key	sync:read,sync:write	t	2025-05-22 08:50:55.049777+00	2025-05-22 08:51:41.532843+00	2025-05-22 08:51:36.775388+00
0dee28c4-23ad-4f95-a7b9-dd1418e68c02	c23d70ac-6fb9-4815-b56e-74de4fc2650b	$2b$12$R0DAtkn7GZBarL/E0.4U3Of5KC0qI1lKnFGXh0JT4kTE3cT.pqTX2	Read-Only Key	sync:read	t	2025-05-22 08:51:56.863934+00	2025-05-22 08:52:16.710899+00	2025-05-22 08:52:11.229071+00
0426553e-8cdc-4372-991c-714e582d86cc	c23d70ac-6fb9-4815-b56e-74de4fc2650b	$2b$12$ukmT0Ixi0g04P70UP76cX.mqOMoZnpj478l/7bAyj0jJh2k8PjAqe	Updated Test Integration	sync:read,sync:write	t	2025-05-22 07:46:50.673425+00	2025-05-22 07:50:05.391022+00	2025-05-22 11:23:53.253156+00
\.


--
-- Data for Name: articles; Type: TABLE DATA; Schema: public; Owner: rafactory_rw
--

COPY public.articles (code, designation, consume_group_designation, consume_group_priority, quantity, unit, category_designation, "position", short_position, code_no_color, component_code, is_extra, length, width, height, surface, angle1, angle2, unit_weight, bar_length, company_guid, created_at, updated_at, guid, project_guid, component_guid, is_active, deleted_at) FROM stdin;
ART002	Test Article 2	\N	\N	2	pcs	\N	\N	\N	\N	\N	f	\N	\N	\N	\N	\N	\N	\N	\N	c23d70ac-6fb9-4815-b56e-74de4fc2650b	2025-05-22 08:29:37.55319+00	\N	550e8400-e29b-41d4-a716-446655440008	6155fec7-a74e-4e05-a76f-077526c017fd	943ab57d-fa40-4202-8562-5b49fc072399	t	\N
ART_B2	Test Article B2	\N	\N	2	pcs	\N	\N	\N	\N	\N	f	\N	\N	\N	\N	\N	\N	\N	\N	8cf127b5-e93d-4d62-a922-cb1bab0f424e	2025-05-22 08:29:55.546777+00	\N	550e8400-e29b-41d4-a716-446655440009	a610de55-bf7d-4afe-b9de-068ef7b64394	ad6c97cf-ef85-415f-b1a4-0ad2cdc52c9a	t	\N
BULK_A1	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	f	\N	\N	\N	\N	\N	\N	\N	\N	c23d70ac-6fb9-4815-b56e-74de4fc2650b	2025-05-22 08:30:36.580335+00	\N	f2f69a0f-4330-4b76-8c4c-c625b25ac2b3	6155fec7-a74e-4e05-a76f-077526c017fd	943ab57d-fa40-4202-8562-5b49fc072399	t	\N
BULK_A2	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	f	\N	\N	\N	\N	\N	\N	\N	\N	c23d70ac-6fb9-4815-b56e-74de4fc2650b	2025-05-22 08:30:36.580335+00	\N	b12110ae-fc48-409d-938b-c96f53219e16	6155fec7-a74e-4e05-a76f-077526c017fd	943ab57d-fa40-4202-8562-5b49fc072399	t	\N
ART001_UPDATED	Updated Test Article	\N	\N	5	pcs	\N	\N	\N	\N	\N	f	\N	\N	\N	\N	\N	\N	\N	\N	c23d70ac-6fb9-4815-b56e-74de4fc2650b	2025-05-22 08:29:28.158354+00	2025-05-23 04:42:57.101425+00	3bf50954-c8c1-4b0a-b358-d94299d47e8c	6155fec7-a74e-4e05-a76f-077526c017fd	943ab57d-fa40-4202-8562-5b49fc072399	t	\N
ART_B1_UPDATED	Updated Test Article B	\N	\N	5	pcs	\N	\N	\N	\N	\N	f	\N	\N	\N	\N	\N	\N	\N	\N	8cf127b5-e93d-4d62-a922-cb1bab0f424e	2025-05-22 08:29:46.329943+00	2025-05-23 06:09:31.986153+00	f397ef6b-cdaa-4255-86c3-5afaac834064	a610de55-bf7d-4afe-b9de-068ef7b64394	ad6c97cf-ef85-415f-b1a4-0ad2cdc52c9a	t	\N
\.


--
-- Data for Name: assemblies; Type: TABLE DATA; Schema: public; Owner: rafactory_rw
--

COPY public.assemblies (trolley_cell, trolley, cell_number, picture, company_guid, created_at, updated_at, guid, project_guid, component_guid, is_active, deleted_at) FROM stdin;
\N	T2	2	\N	c23d70ac-6fb9-4815-b56e-74de4fc2650b	2025-05-22 07:58:43.015339+00	\N	9fb4a075-1bdc-4dc0-b517-dc98943d6720	550e8400-e29b-41d4-a716-446655440000	550e8400-e29b-41d4-a716-446655440002	t	\N
\N	T3	3	\N	c23d70ac-6fb9-4815-b56e-74de4fc2650b	2025-05-22 07:58:51.473853+00	\N	550e8400-e29b-41d4-a716-446655440004	6155fec7-a74e-4e05-a76f-077526c017fd	943ab57d-fa40-4202-8562-5b49fc072399	t	\N
\N	T2	2	\N	8cf127b5-e93d-4d62-a922-cb1bab0f424e	2025-05-22 07:59:20.718196+00	\N	7828e554-072f-4692-9b75-dac0d2cf6021	550e8400-e29b-41d4-a716-446655440001	550e8400-e29b-41d4-a716-446655440003	t	\N
\N	T3	3	\N	8cf127b5-e93d-4d62-a922-cb1bab0f424e	2025-05-22 07:59:28.810272+00	\N	550e8400-e29b-41d4-a716-446655440005	a610de55-bf7d-4afe-b9de-068ef7b64394	ad6c97cf-ef85-415f-b1a4-0ad2cdc52c9a	t	\N
\N	T1_UPDATED	10	\N	c23d70ac-6fb9-4815-b56e-74de4fc2650b	2025-05-22 07:58:20.37407+00	2025-05-23 04:41:37.080051+00	ed225d42-ccd8-4ed7-9bae-fb318d1d9c06	6155fec7-a74e-4e05-a76f-077526c017fd	943ab57d-fa40-4202-8562-5b49fc072399	t	\N
\N	T1_UPDATED	10	\N	8cf127b5-e93d-4d62-a922-cb1bab0f424e	2025-05-22 07:58:58.671417+00	2025-05-23 06:07:55.93101+00	53faab84-c851-4527-b10d-0adfebcfa630	a610de55-bf7d-4afe-b9de-068ef7b64394	ad6c97cf-ef85-415f-b1a4-0ad2cdc52c9a	t	\N
\.


--
-- Data for Name: companies; Type: TABLE DATA; Schema: public; Owner: rafactory_rw
--

COPY public.companies (guid, name, short_name, logo_path, is_active, created_at, updated_at, company_index) FROM stdin;
28fbeed6-5e09-4b75-ad74-ab1cdc4dec71	Delice Automatics Ltd.	\N	\N	t	2025-04-26 07:21:08.997363+00	2025-05-05 13:54:26.465339+00	1
8cf127b5-e93d-4d62-a922-cb1bab0f424e	Company B	\N	\N	t	2025-05-22 07:15:14.992166+00	2025-05-22 07:16:11.008686+00	3
c23d70ac-6fb9-4815-b56e-74de4fc2650b	Company A	\N	\N	t	2025-05-22 07:15:08.782428+00	2025-05-22 07:16:38.66568+00	4
b23040b3-405e-4bd9-ba4f-86c1e19efab1	Test Company 1	\N	\N	t	2025-05-22 11:25:28.513679+00	\N	5
8771f506-8a85-4f95-bf3c-4c8234d79517	Test Company 2	\N	\N	t	2025-05-22 11:25:42.528895+00	\N	10
\.


--
-- Data for Name: components; Type: TABLE DATA; Schema: public; Owner: rafactory_rw
--

COPY public.components (code, designation, quantity, picture, company_guid, created_at, updated_at, guid, project_guid, is_active, deleted_at) FROM stdin;
COMP_A1_2	Second Component	2	\N	c23d70ac-6fb9-4815-b56e-74de4fc2650b	2025-05-22 07:54:34.408044+00	\N	4bf54f9d-32ae-4b1b-aeb3-e4bf3b6c04df	6155fec7-a74e-4e05-a76f-077526c017fd	t	\N
COMP_A2_1	Component with Specific GUID	1	\N	c23d70ac-6fb9-4815-b56e-74de4fc2650b	2025-05-22 07:55:00.989638+00	\N	550e8400-e29b-41d4-a716-446655440002	550e8400-e29b-41d4-a716-446655440000	t	\N
COMP_A2_2	Another Component	3	\N	c23d70ac-6fb9-4815-b56e-74de4fc2650b	2025-05-22 07:55:08.268483+00	\N	78caa7e7-a228-42d6-94e2-99e8936f3807	550e8400-e29b-41d4-a716-446655440000	t	\N
COMP_A3_1	Project A3 Component 1	2	\N	c23d70ac-6fb9-4815-b56e-74de4fc2650b	2025-05-22 07:55:17.907203+00	\N	7aa1299f-8b3b-43e3-9845-a8bb05124cba	0a7bd61e-e780-4e03-ad42-b4b50a46515a	t	\N
COMP_A3_2	Project A3 Component 2	4	\N	c23d70ac-6fb9-4815-b56e-74de4fc2650b	2025-05-22 07:55:25.195684+00	\N	954e1d99-c8b0-4e98-a4e9-2430918850ba	0a7bd61e-e780-4e03-ad42-b4b50a46515a	t	\N
COMP_B1_2	Project B1 Component 2	2	\N	8cf127b5-e93d-4d62-a922-cb1bab0f424e	2025-05-22 07:55:41.581659+00	\N	51f8ca31-2172-4c67-a38c-61ac295bb451	a610de55-bf7d-4afe-b9de-068ef7b64394	t	\N
COMP_B2_1	Component with Specific GUID	1	\N	8cf127b5-e93d-4d62-a922-cb1bab0f424e	2025-05-22 07:55:56.728843+00	\N	550e8400-e29b-41d4-a716-446655440003	550e8400-e29b-41d4-a716-446655440001	t	\N
COMP_B2_2	Project B2 Component 2	3	\N	8cf127b5-e93d-4d62-a922-cb1bab0f424e	2025-05-22 07:56:04.950071+00	\N	14238589-cf29-40da-a898-2471a0cb96a5	550e8400-e29b-41d4-a716-446655440001	t	\N
COMP_B3_1	Project B3 Component 1	1	\N	8cf127b5-e93d-4d62-a922-cb1bab0f424e	2025-05-22 07:56:34.004328+00	\N	ea6f1536-3b67-4a92-82b9-1c05dab3c0a9	fd723b43-798d-4469-9174-5e3f83da410a	t	\N
COMP_B3_2	Project B3 Component 2	2	\N	8cf127b5-e93d-4d62-a922-cb1bab0f424e	2025-05-22 07:56:41.401786+00	\N	a087e2ce-9407-4dbc-a46f-3d8c60507e45	fd723b43-798d-4469-9174-5e3f83da410a	t	\N
COMP_A1_1_UPDATED	Updated First Component	5	\N	c23d70ac-6fb9-4815-b56e-74de4fc2650b	2025-05-22 07:54:26.859371+00	2025-05-23 04:40:50.967449+00	943ab57d-fa40-4202-8562-5b49fc072399	6155fec7-a74e-4e05-a76f-077526c017fd	t	\N
COMP_B1_1_UPDATED	Updated Component B1_1	10	\N	8cf127b5-e93d-4d62-a922-cb1bab0f424e	2025-05-22 07:55:32.55337+00	2025-05-23 06:07:21.066748+00	ad6c97cf-ef85-415f-b1a4-0ad2cdc52c9a	a610de55-bf7d-4afe-b9de-068ef7b64394	t	\N
\.


--
-- Data for Name: pieces; Type: TABLE DATA; Schema: public; Owner: rafactory_rw
--

COPY public.pieces (piece_id, outer_length, angle_left, angle_right, orientation, barcode, assembly_width, assembly_height, trolley, cell, trolley_cell, operations, component_code, component_description, info2, info3, client, dealer, project_description, inner_length, reinforcement_code, reinforcement_length, hardware_info, glass_info, other_length, project_number, component_number, water_handle, segment_order, cutting_pattern, fixing_mode, material_type, project_code_parent, bar_id, bar_rest, bar_length, bar_cutting_tolerance, profile_code, profile_name, lamination, gasket, profile_width, profile_height, welding_tolerance, profile_color, profile_type_ra, profile_type, trolley_size, profile_code_with_color, parent_assembly_trolley_cell, mullion_trolley_cell, glazing_bead_trolley_cell, picture, project_phase, company_guid, created_at, updated_at, guid, project_guid, component_guid, assembly_guid, is_active, deleted_at) FROM stdin;
PIECE002	200	90	90	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	c23d70ac-6fb9-4815-b56e-74de4fc2650b	2025-05-22 08:28:42.977528+00	\N	809dd56e-8553-4ffa-a409-80e397a534bc	6155fec7-a74e-4e05-a76f-077526c017fd	943ab57d-fa40-4202-8562-5b49fc072399	\N	t	\N
PIECE003	150	30	60	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	c23d70ac-6fb9-4815-b56e-74de4fc2650b	2025-05-22 08:28:51.816257+00	\N	550e8400-e29b-41d4-a716-446655440006	6155fec7-a74e-4e05-a76f-077526c017fd	943ab57d-fa40-4202-8562-5b49fc072399	ed225d42-ccd8-4ed7-9bae-fb318d1d9c06	t	\N
PIECE004	250	45	45	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	c23d70ac-6fb9-4815-b56e-74de4fc2650b	2025-05-22 08:28:59.692224+00	\N	550e8400-e29b-41d4-a716-446655440007	6155fec7-a74e-4e05-a76f-077526c017fd	943ab57d-fa40-4202-8562-5b49fc072399	\N	t	\N
PIECE_B2	200	90	90	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	8cf127b5-e93d-4d62-a922-cb1bab0f424e	2025-05-22 08:29:19.47512+00	\N	55fbe07e-7144-4826-82fc-a66245de6b40	a610de55-bf7d-4afe-b9de-068ef7b64394	ad6c97cf-ef85-415f-b1a4-0ad2cdc52c9a	\N	t	\N
BULK1	100	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	c23d70ac-6fb9-4815-b56e-74de4fc2650b	2025-05-22 08:30:27.272432+00	\N	8393a844-f995-4e05-b330-371bc8448055	6155fec7-a74e-4e05-a76f-077526c017fd	943ab57d-fa40-4202-8562-5b49fc072399	\N	t	\N
BULK2	200	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	c23d70ac-6fb9-4815-b56e-74de4fc2650b	2025-05-22 08:30:27.272432+00	\N	1290a271-21a1-4e90-80fb-85bd89d81a2d	6155fec7-a74e-4e05-a76f-077526c017fd	943ab57d-fa40-4202-8562-5b49fc072399	\N	t	\N
PIECE001_UPDATED	120	60	30	\N	BAR123	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	c23d70ac-6fb9-4815-b56e-74de4fc2650b	2025-05-22 08:28:34.413643+00	2025-05-23 04:42:17.771017+00	3397158b-e00e-4b18-9d7e-d5f180445b65	6155fec7-a74e-4e05-a76f-077526c017fd	943ab57d-fa40-4202-8562-5b49fc072399	ed225d42-ccd8-4ed7-9bae-fb318d1d9c06	t	\N
PIECE_B1_UPDATED	200	60	30	\N	BAR_B1	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	8cf127b5-e93d-4d62-a922-cb1bab0f424e	2025-05-22 08:29:11.785577+00	2025-05-23 06:08:45.796661+00	8ca8efcd-3dc2-42a0-bc1e-7aaf95fd53e8	a610de55-bf7d-4afe-b9de-068ef7b64394	ad6c97cf-ef85-415f-b1a4-0ad2cdc52c9a	53faab84-c851-4527-b10d-0adfebcfa630	t	\N
\.


--
-- Data for Name: projects; Type: TABLE DATA; Schema: public; Owner: rafactory_rw
--

COPY public.projects (code, updated_at, due_date, in_production, company_name, company_guid, created_at, guid, is_active, deleted_at) FROM stdin;
Project_A1	\N	2024-12-31 23:59:59+00	f	\N	c23d70ac-6fb9-4815-b56e-74de4fc2650b	2025-05-22 07:48:56.720416+00	6155fec7-a74e-4e05-a76f-077526c017fd	t	\N
Project_A2	\N	2024-12-31 23:59:59+00	f	\N	c23d70ac-6fb9-4815-b56e-74de4fc2650b	2025-05-22 07:49:05.469677+00	550e8400-e29b-41d4-a716-446655440000	t	\N
Project_A3	\N	2024-12-31 23:59:59+00	f	\N	c23d70ac-6fb9-4815-b56e-74de4fc2650b	2025-05-22 07:49:13.070706+00	0a7bd61e-e780-4e03-ad42-b4b50a46515a	t	\N
Project_B2	\N	2024-12-31 23:59:59+00	f	\N	8cf127b5-e93d-4d62-a922-cb1bab0f424e	2025-05-22 07:49:30.051084+00	550e8400-e29b-41d4-a716-446655440001	t	\N
Project_B3	\N	2024-12-31 23:59:59+00	f	\N	8cf127b5-e93d-4d62-a922-cb1bab0f424e	2025-05-22 07:49:38.184301+00	fd723b43-798d-4469-9174-5e3f83da410a	t	\N
Mixed_1	\N	2024-12-31 23:59:59+00	f	\N	c23d70ac-6fb9-4815-b56e-74de4fc2650b	2025-05-22 07:50:05.394425+00	5164459c-898c-4dd3-acc7-40392364e966	t	\N
Mixed_2	\N	2024-12-31 23:59:59+00	f	\N	c23d70ac-6fb9-4815-b56e-74de4fc2650b	2025-05-22 07:50:05.394425+00	550e8400-e29b-41d4-a716-446655440002	t	\N
PROJ_A1_UPDATED	2025-05-22 11:26:43.345803+00	\N	f	\N	28fbeed6-5e09-4b75-ad74-ab1cdc4dec71	2025-05-22 07:47:24.708317+00	a0900c75-0f8c-4f45-9f98-e725b5246416	t	\N
PROJ_TEST_UPDATED	2025-05-23 04:40:12.611731+00	\N	t	\N	c23d70ac-6fb9-4815-b56e-74de4fc2650b	2025-05-22 08:45:49.624548+00	a9de1611-75b1-41dd-a543-34cb62490a81	t	\N
Project_B1_UPDATED	2025-05-23 05:06:59.757474+00	\N	t	\N	8cf127b5-e93d-4d62-a922-cb1bab0f424e	2025-05-22 07:49:21.646062+00	a610de55-bf7d-4afe-b9de-068ef7b64394	t	\N
\.


--
-- Data for Name: ui_templates; Type: TABLE DATA; Schema: public; Owner: rafactory_rw
--

COPY public.ui_templates (id, company_guid, workstation_guid, name, json_data, created_at, updated_at) FROM stdin;
\.


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: rafactory_rw
--

COPY public.users (guid, company_guid, email, pwd_hash, role, pin, is_active, created_at, updated_at, name, surname, picture_path) FROM stdin;
820c0611-2d55-4094-8851-8891a67247c4	c23d70ac-6fb9-4815-b56e-74de4fc2650b	admin2.a@example.com	$2b$12$KgGj67G222RTahMizVkj0eXa69phLH.CmXC.LopRsFy6fovl3u6iS	CompanyAdmin	\N	t	2025-05-22 07:17:14.894416+00	\N	Admin	Two	\N
ee5048f3-7202-4f44-a38c-fc7b3d65f760	c23d70ac-6fb9-4815-b56e-74de4fc2650b	pm1.a@example.com	$2b$12$zNhP2rmqEIZIBxnuRx3m2.jWrTCAcn3sB0xmFukPHf0tRcqvgHLgi	ProjectManager	\N	t	2025-05-22 07:17:22.137931+00	\N	Project	Manager One	\N
01ef5ee6-4390-47dc-9d2e-d146ffe97159	8cf127b5-e93d-4d62-a922-cb1bab0f424e	admin1.b@example.com	$2b$12$q.DVq1IEIkEP8J3.zb1W8.DF/cS6TVONuy1Qlsa63eY.7xuWXvttG	CompanyAdmin	\N	t	2025-05-22 07:17:29.727806+00	\N	Admin B	One	\N
797cdcd8-e6d1-40d6-b9db-1c8e1b4c167f	c23d70ac-6fb9-4815-b56e-74de4fc2650b	pm2.a@example.com	$2b$12$NDx9G4MmWhpWViDlTUSYi.W9QEKBfvGp0PYFZwAJGxtSW1t4wNl62	ProjectManager	\N	t	2025-05-22 07:18:53.656228+00	\N	\N	\N	\N
2350b23b-6c1b-43be-a12c-93b40cd6f6f6	c23d70ac-6fb9-4815-b56e-74de4fc2650b	op1.a@example.com	$2b$12$ePE5drWU/tsByJ0luIMHZOUs/T9WWxEeqtgh2I72KJ.5JF2aqsAaS	Operator	123456	t	2025-05-22 07:19:01.524273+00	\N	\N	\N	\N
bd950513-c9c5-4e2e-8728-0e6de17509be	8cf127b5-e93d-4d62-a922-cb1bab0f424e	admin2.b@example.com	$2b$12$LzfxKOicN3WgkHd3k4MzEuMXpI6UKGsLIjozjtNzckf1VB3xc081y	CompanyAdmin	\N	t	2025-05-22 07:23:25.931466+00	\N	Admin B	Two	\N
24ee4a5e-f81b-4521-a83d-447619a304db	c23d70ac-6fb9-4815-b56e-74de4fc2650b	extended.user@example.com	$2b$12$wnlaBUCiJENZUH9EWIZcGuir0AH5Tsn8knVFGGjh0OR15Bi7XteMK	ProjectManager	\N	t	2025-05-22 07:41:44.742705+00	2025-05-22 07:42:08.255188+00	Johnny	Smith	/images/profile/johnsmith.jpg
5e9ad11e-51f5-4356-aa23-3639d377c731	c23d70ac-6fb9-4815-b56e-74de4fc2650b	null.fields@example.com	$2b$12$KVPPTA5fVdvMsFaqezTtPO7pePh4cNDnsgWxRPiW/QohfxBr0yDiW	ProjectManager	\N	f	2025-05-22 07:42:46.50362+00	2025-05-22 07:43:58.268153+00	\N	\N	\N
caf68769-697a-4593-a99f-63f98a3eb7ab	c23d70ac-6fb9-4815-b56e-74de4fc2650b	admin1.a@example.com	$2b$12$aWbCz/rTCR/40pOY75Q9TO0Veu5UWIbH8IyEiWRb7CRJjT8.gG.Ii	CompanyAdmin	\N	t	2025-05-22 07:16:56.858846+00	2025-05-22 11:22:46.652546+00	AdminUpdated	OneUpdated	\N
856d4637-cb16-4cf0-a535-efc02364096a	28fbeed6-5e09-4b75-ad74-ab1cdc4dec71	a.petrov@delice.bg	$2b$12$gOE4AUzzCGEI30WT.BYslODPPnF6WHni3GKxDFV7DRCpM72Ot0p5u	SystemAdmin	\N	t	2025-04-26 07:21:08.997363+00	2025-05-02 08:42:30.256138+00	\N	\N	\N
\.


--
-- Data for Name: workflow; Type: TABLE DATA; Schema: public; Owner: rafactory_rw
--

COPY public.workflow (guid, company_guid, company_name, workstation_guid, workstation_name, api_key_guid, user_guid, user_name, action_type, action_value, created_at, updated_at) FROM stdin;
78663e5e-8545-4b59-b0e0-f00e056007a3	28fbeed6-5e09-4b75-ad74-ab1cdc4dec71	Delice Automatics Ltd.	\N	\N	\N	856d4637-cb16-4cf0-a535-efc02364096a	a.petrov@delice.bg	SystemEvent	Test workflow entry	2025-05-22 11:27:26.429296+00	\N
\.


--
-- Data for Name: workstations; Type: TABLE DATA; Schema: public; Owner: rafactory_rw
--

COPY public.workstations (guid, company_guid, location, type, is_active, created_at, updated_at) FROM stdin;
e1e6ee80-dff2-4cc0-8699-f1842fcb4be8	c23d70ac-6fb9-4815-b56e-74de4fc2650b	Warehouse	Logistics	t	2025-05-22 07:44:43.231071+00	\N
23e4697b-09a9-4043-9b40-8ddad1b50d96	8cf127b5-e93d-4d62-a922-cb1bab0f424e	Assembly Line 1	Assembly	t	2025-05-22 09:07:57.595327+00	\N
d07ebe30-e5fb-4fc8-a49f-a84522347544	c23d70ac-6fb9-4815-b56e-74de4fc2650b	Updated Assembly Line 1	Assembly	t	2025-05-22 07:44:35.719562+00	2025-05-22 11:23:13.197461+00
\.


--
-- Name: ui_templates_id_seq; Type: SEQUENCE SET; Schema: public; Owner: rafactory_rw
--

SELECT pg_catalog.setval('public.ui_templates_id_seq', 1, false);


--
-- Name: alembic_version alembic_version_pkc; Type: CONSTRAINT; Schema: public; Owner: rafactory_rw
--

ALTER TABLE ONLY public.alembic_version
    ADD CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num);


--
-- Name: api_keys api_keys_key_hash_key; Type: CONSTRAINT; Schema: public; Owner: rafactory_rw
--

ALTER TABLE ONLY public.api_keys
    ADD CONSTRAINT api_keys_key_hash_key UNIQUE (key_hash);


--
-- Name: api_keys api_keys_pkey; Type: CONSTRAINT; Schema: public; Owner: rafactory_rw
--

ALTER TABLE ONLY public.api_keys
    ADD CONSTRAINT api_keys_pkey PRIMARY KEY (guid);


--
-- Name: companies companies_pkey; Type: CONSTRAINT; Schema: public; Owner: rafactory_rw
--

ALTER TABLE ONLY public.companies
    ADD CONSTRAINT companies_pkey PRIMARY KEY (guid);


--
-- Name: articles pk_articles; Type: CONSTRAINT; Schema: public; Owner: rafactory_rw
--

ALTER TABLE ONLY public.articles
    ADD CONSTRAINT pk_articles PRIMARY KEY (guid);


--
-- Name: assemblies pk_assemblies; Type: CONSTRAINT; Schema: public; Owner: rafactory_rw
--

ALTER TABLE ONLY public.assemblies
    ADD CONSTRAINT pk_assemblies PRIMARY KEY (guid);


--
-- Name: components pk_components; Type: CONSTRAINT; Schema: public; Owner: rafactory_rw
--

ALTER TABLE ONLY public.components
    ADD CONSTRAINT pk_components PRIMARY KEY (guid);


--
-- Name: pieces pk_pieces; Type: CONSTRAINT; Schema: public; Owner: rafactory_rw
--

ALTER TABLE ONLY public.pieces
    ADD CONSTRAINT pk_pieces PRIMARY KEY (guid);


--
-- Name: projects pk_projects; Type: CONSTRAINT; Schema: public; Owner: rafactory_rw
--

ALTER TABLE ONLY public.projects
    ADD CONSTRAINT pk_projects PRIMARY KEY (guid);


--
-- Name: ui_templates ui_templates_pkey; Type: CONSTRAINT; Schema: public; Owner: rafactory_rw
--

ALTER TABLE ONLY public.ui_templates
    ADD CONSTRAINT ui_templates_pkey PRIMARY KEY (id);


--
-- Name: articles uq_articles_guid; Type: CONSTRAINT; Schema: public; Owner: rafactory_rw
--

ALTER TABLE ONLY public.articles
    ADD CONSTRAINT uq_articles_guid UNIQUE (guid);


--
-- Name: assemblies uq_assemblies_guid; Type: CONSTRAINT; Schema: public; Owner: rafactory_rw
--

ALTER TABLE ONLY public.assemblies
    ADD CONSTRAINT uq_assemblies_guid UNIQUE (guid);


--
-- Name: companies uq_company_index; Type: CONSTRAINT; Schema: public; Owner: rafactory_rw
--

ALTER TABLE ONLY public.companies
    ADD CONSTRAINT uq_company_index UNIQUE (company_index);


--
-- Name: components uq_components_guid; Type: CONSTRAINT; Schema: public; Owner: rafactory_rw
--

ALTER TABLE ONLY public.components
    ADD CONSTRAINT uq_components_guid UNIQUE (guid);


--
-- Name: pieces uq_pieces_guid; Type: CONSTRAINT; Schema: public; Owner: rafactory_rw
--

ALTER TABLE ONLY public.pieces
    ADD CONSTRAINT uq_pieces_guid UNIQUE (guid);


--
-- Name: projects uq_projects_guid; Type: CONSTRAINT; Schema: public; Owner: rafactory_rw
--

ALTER TABLE ONLY public.projects
    ADD CONSTRAINT uq_projects_guid UNIQUE (guid);


--
-- Name: users users_email_key; Type: CONSTRAINT; Schema: public; Owner: rafactory_rw
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_email_key UNIQUE (email);


--
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: rafactory_rw
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (guid);


--
-- Name: workflow workflow_pkey; Type: CONSTRAINT; Schema: public; Owner: rafactory_rw
--

ALTER TABLE ONLY public.workflow
    ADD CONSTRAINT workflow_pkey PRIMARY KEY (guid);


--
-- Name: workstations workstations_pkey; Type: CONSTRAINT; Schema: public; Owner: rafactory_rw
--

ALTER TABLE ONLY public.workstations
    ADD CONSTRAINT workstations_pkey PRIMARY KEY (guid);


--
-- Name: ix_companies_name; Type: INDEX; Schema: public; Owner: rafactory_rw
--

CREATE INDEX ix_companies_name ON public.companies USING btree (name);


--
-- Name: ix_workflow_action_type; Type: INDEX; Schema: public; Owner: rafactory_rw
--

CREATE INDEX ix_workflow_action_type ON public.workflow USING btree (action_type);


--
-- Name: ix_workflow_company_guid; Type: INDEX; Schema: public; Owner: rafactory_rw
--

CREATE INDEX ix_workflow_company_guid ON public.workflow USING btree (company_guid);


--
-- Name: ix_workflow_created_at; Type: INDEX; Schema: public; Owner: rafactory_rw
--

CREATE INDEX ix_workflow_created_at ON public.workflow USING btree (created_at);


--
-- Name: ix_workflow_user_guid; Type: INDEX; Schema: public; Owner: rafactory_rw
--

CREATE INDEX ix_workflow_user_guid ON public.workflow USING btree (user_guid);


--
-- Name: ix_workflow_workstation_guid; Type: INDEX; Schema: public; Owner: rafactory_rw
--

CREATE INDEX ix_workflow_workstation_guid ON public.workflow USING btree (workstation_guid);


--
-- Name: api_keys api_keys_updated_at_trigger; Type: TRIGGER; Schema: public; Owner: rafactory_rw
--

CREATE TRIGGER api_keys_updated_at_trigger BEFORE UPDATE ON public.api_keys FOR EACH ROW EXECUTE FUNCTION public.update_updated_at_column();


--
-- Name: articles update_articles_updated_at; Type: TRIGGER; Schema: public; Owner: rafactory_rw
--

CREATE TRIGGER update_articles_updated_at BEFORE UPDATE ON public.articles FOR EACH ROW EXECUTE FUNCTION public.update_updated_at_column();


--
-- Name: assemblies update_assemblies_updated_at; Type: TRIGGER; Schema: public; Owner: rafactory_rw
--

CREATE TRIGGER update_assemblies_updated_at BEFORE UPDATE ON public.assemblies FOR EACH ROW EXECUTE FUNCTION public.update_updated_at_column();


--
-- Name: companies update_companies_updated_at; Type: TRIGGER; Schema: public; Owner: rafactory_rw
--

CREATE TRIGGER update_companies_updated_at BEFORE UPDATE ON public.companies FOR EACH ROW EXECUTE FUNCTION public.update_updated_at_column();


--
-- Name: components update_components_updated_at; Type: TRIGGER; Schema: public; Owner: rafactory_rw
--

CREATE TRIGGER update_components_updated_at BEFORE UPDATE ON public.components FOR EACH ROW EXECUTE FUNCTION public.update_updated_at_column();


--
-- Name: pieces update_pieces_updated_at; Type: TRIGGER; Schema: public; Owner: rafactory_rw
--

CREATE TRIGGER update_pieces_updated_at BEFORE UPDATE ON public.pieces FOR EACH ROW EXECUTE FUNCTION public.update_updated_at_column();


--
-- Name: projects update_projects_updated_at; Type: TRIGGER; Schema: public; Owner: rafactory_rw
--

CREATE TRIGGER update_projects_updated_at BEFORE UPDATE ON public.projects FOR EACH ROW EXECUTE FUNCTION public.update_updated_at_column();


--
-- Name: ui_templates update_ui_templates_updated_at; Type: TRIGGER; Schema: public; Owner: rafactory_rw
--

CREATE TRIGGER update_ui_templates_updated_at BEFORE UPDATE ON public.ui_templates FOR EACH ROW EXECUTE FUNCTION public.update_updated_at_column();


--
-- Name: api_keys update_updated_at_timestamp; Type: TRIGGER; Schema: public; Owner: rafactory_rw
--

CREATE TRIGGER update_updated_at_timestamp BEFORE UPDATE ON public.api_keys FOR EACH ROW EXECUTE FUNCTION public.update_updated_at_column();


--
-- Name: articles update_updated_at_timestamp; Type: TRIGGER; Schema: public; Owner: rafactory_rw
--

CREATE TRIGGER update_updated_at_timestamp BEFORE UPDATE ON public.articles FOR EACH ROW EXECUTE FUNCTION public.update_updated_at_column();


--
-- Name: assemblies update_updated_at_timestamp; Type: TRIGGER; Schema: public; Owner: rafactory_rw
--

CREATE TRIGGER update_updated_at_timestamp BEFORE UPDATE ON public.assemblies FOR EACH ROW EXECUTE FUNCTION public.update_updated_at_column();


--
-- Name: companies update_updated_at_timestamp; Type: TRIGGER; Schema: public; Owner: rafactory_rw
--

CREATE TRIGGER update_updated_at_timestamp BEFORE UPDATE ON public.companies FOR EACH ROW EXECUTE FUNCTION public.update_updated_at_column();


--
-- Name: components update_updated_at_timestamp; Type: TRIGGER; Schema: public; Owner: rafactory_rw
--

CREATE TRIGGER update_updated_at_timestamp BEFORE UPDATE ON public.components FOR EACH ROW EXECUTE FUNCTION public.update_updated_at_column();


--
-- Name: pieces update_updated_at_timestamp; Type: TRIGGER; Schema: public; Owner: rafactory_rw
--

CREATE TRIGGER update_updated_at_timestamp BEFORE UPDATE ON public.pieces FOR EACH ROW EXECUTE FUNCTION public.update_updated_at_column();


--
-- Name: projects update_updated_at_timestamp; Type: TRIGGER; Schema: public; Owner: rafactory_rw
--

CREATE TRIGGER update_updated_at_timestamp BEFORE UPDATE ON public.projects FOR EACH ROW EXECUTE FUNCTION public.update_updated_at_column();


--
-- Name: ui_templates update_updated_at_timestamp; Type: TRIGGER; Schema: public; Owner: rafactory_rw
--

CREATE TRIGGER update_updated_at_timestamp BEFORE UPDATE ON public.ui_templates FOR EACH ROW EXECUTE FUNCTION public.update_updated_at_column();


--
-- Name: users update_updated_at_timestamp; Type: TRIGGER; Schema: public; Owner: rafactory_rw
--

CREATE TRIGGER update_updated_at_timestamp BEFORE UPDATE ON public.users FOR EACH ROW EXECUTE FUNCTION public.update_updated_at_column();


--
-- Name: workstations update_updated_at_timestamp; Type: TRIGGER; Schema: public; Owner: rafactory_rw
--

CREATE TRIGGER update_updated_at_timestamp BEFORE UPDATE ON public.workstations FOR EACH ROW EXECUTE FUNCTION public.update_updated_at_column();


--
-- Name: users update_users_updated_at; Type: TRIGGER; Schema: public; Owner: rafactory_rw
--

CREATE TRIGGER update_users_updated_at BEFORE UPDATE ON public.users FOR EACH ROW EXECUTE FUNCTION public.update_updated_at_column();


--
-- Name: workstations update_workstations_updated_at; Type: TRIGGER; Schema: public; Owner: rafactory_rw
--

CREATE TRIGGER update_workstations_updated_at BEFORE UPDATE ON public.workstations FOR EACH ROW EXECUTE FUNCTION public.update_updated_at_column();


--
-- Name: api_keys api_keys_company_guid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: rafactory_rw
--

ALTER TABLE ONLY public.api_keys
    ADD CONSTRAINT api_keys_company_guid_fkey FOREIGN KEY (company_guid) REFERENCES public.companies(guid);


--
-- Name: articles articles_company_guid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: rafactory_rw
--

ALTER TABLE ONLY public.articles
    ADD CONSTRAINT articles_company_guid_fkey FOREIGN KEY (company_guid) REFERENCES public.companies(guid);


--
-- Name: assemblies assemblies_company_guid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: rafactory_rw
--

ALTER TABLE ONLY public.assemblies
    ADD CONSTRAINT assemblies_company_guid_fkey FOREIGN KEY (company_guid) REFERENCES public.companies(guid);


--
-- Name: components components_company_guid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: rafactory_rw
--

ALTER TABLE ONLY public.components
    ADD CONSTRAINT components_company_guid_fkey FOREIGN KEY (company_guid) REFERENCES public.companies(guid);


--
-- Name: articles fk_articles_component_guid; Type: FK CONSTRAINT; Schema: public; Owner: rafactory_rw
--

ALTER TABLE ONLY public.articles
    ADD CONSTRAINT fk_articles_component_guid FOREIGN KEY (component_guid) REFERENCES public.components(guid);


--
-- Name: articles fk_articles_project_guid; Type: FK CONSTRAINT; Schema: public; Owner: rafactory_rw
--

ALTER TABLE ONLY public.articles
    ADD CONSTRAINT fk_articles_project_guid FOREIGN KEY (project_guid) REFERENCES public.projects(guid);


--
-- Name: assemblies fk_assemblies_component_guid; Type: FK CONSTRAINT; Schema: public; Owner: rafactory_rw
--

ALTER TABLE ONLY public.assemblies
    ADD CONSTRAINT fk_assemblies_component_guid FOREIGN KEY (component_guid) REFERENCES public.components(guid);


--
-- Name: assemblies fk_assemblies_project_guid; Type: FK CONSTRAINT; Schema: public; Owner: rafactory_rw
--

ALTER TABLE ONLY public.assemblies
    ADD CONSTRAINT fk_assemblies_project_guid FOREIGN KEY (project_guid) REFERENCES public.projects(guid);


--
-- Name: components fk_components_project_guid; Type: FK CONSTRAINT; Schema: public; Owner: rafactory_rw
--

ALTER TABLE ONLY public.components
    ADD CONSTRAINT fk_components_project_guid FOREIGN KEY (project_guid) REFERENCES public.projects(guid);


--
-- Name: pieces fk_pieces_assembly_guid; Type: FK CONSTRAINT; Schema: public; Owner: rafactory_rw
--

ALTER TABLE ONLY public.pieces
    ADD CONSTRAINT fk_pieces_assembly_guid FOREIGN KEY (assembly_guid) REFERENCES public.assemblies(guid);


--
-- Name: pieces fk_pieces_component_guid; Type: FK CONSTRAINT; Schema: public; Owner: rafactory_rw
--

ALTER TABLE ONLY public.pieces
    ADD CONSTRAINT fk_pieces_component_guid FOREIGN KEY (component_guid) REFERENCES public.components(guid);


--
-- Name: pieces fk_pieces_project_guid; Type: FK CONSTRAINT; Schema: public; Owner: rafactory_rw
--

ALTER TABLE ONLY public.pieces
    ADD CONSTRAINT fk_pieces_project_guid FOREIGN KEY (project_guid) REFERENCES public.projects(guid);


--
-- Name: pieces pieces_company_guid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: rafactory_rw
--

ALTER TABLE ONLY public.pieces
    ADD CONSTRAINT pieces_company_guid_fkey FOREIGN KEY (company_guid) REFERENCES public.companies(guid);


--
-- Name: projects projects_company_guid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: rafactory_rw
--

ALTER TABLE ONLY public.projects
    ADD CONSTRAINT projects_company_guid_fkey FOREIGN KEY (company_guid) REFERENCES public.companies(guid);


--
-- Name: ui_templates ui_templates_company_guid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: rafactory_rw
--

ALTER TABLE ONLY public.ui_templates
    ADD CONSTRAINT ui_templates_company_guid_fkey FOREIGN KEY (company_guid) REFERENCES public.companies(guid);


--
-- Name: ui_templates ui_templates_workstation_guid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: rafactory_rw
--

ALTER TABLE ONLY public.ui_templates
    ADD CONSTRAINT ui_templates_workstation_guid_fkey FOREIGN KEY (workstation_guid) REFERENCES public.workstations(guid);


--
-- Name: users users_company_guid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: rafactory_rw
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_company_guid_fkey FOREIGN KEY (company_guid) REFERENCES public.companies(guid);


--
-- Name: workflow workflow_company_guid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: rafactory_rw
--

ALTER TABLE ONLY public.workflow
    ADD CONSTRAINT workflow_company_guid_fkey FOREIGN KEY (company_guid) REFERENCES public.companies(guid);


--
-- Name: workflow workflow_user_guid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: rafactory_rw
--

ALTER TABLE ONLY public.workflow
    ADD CONSTRAINT workflow_user_guid_fkey FOREIGN KEY (user_guid) REFERENCES public.users(guid);


--
-- Name: workflow workflow_workstation_guid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: rafactory_rw
--

ALTER TABLE ONLY public.workflow
    ADD CONSTRAINT workflow_workstation_guid_fkey FOREIGN KEY (workstation_guid) REFERENCES public.workstations(guid);


--
-- Name: workstations workstations_company_guid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: rafactory_rw
--

ALTER TABLE ONLY public.workstations
    ADD CONSTRAINT workstations_company_guid_fkey FOREIGN KEY (company_guid) REFERENCES public.companies(guid);


--
-- Name: alembic_version; Type: ROW SECURITY; Schema: public; Owner: rafactory_rw
--

ALTER TABLE public.alembic_version ENABLE ROW LEVEL SECURITY;

--
-- Name: api_keys; Type: ROW SECURITY; Schema: public; Owner: rafactory_rw
--

ALTER TABLE public.api_keys ENABLE ROW LEVEL SECURITY;

--
-- Name: articles; Type: ROW SECURITY; Schema: public; Owner: rafactory_rw
--

ALTER TABLE public.articles ENABLE ROW LEVEL SECURITY;

--
-- Name: assemblies; Type: ROW SECURITY; Schema: public; Owner: rafactory_rw
--

ALTER TABLE public.assemblies ENABLE ROW LEVEL SECURITY;

--
-- Name: companies; Type: ROW SECURITY; Schema: public; Owner: rafactory_rw
--

ALTER TABLE public.companies ENABLE ROW LEVEL SECURITY;

--
-- Name: components; Type: ROW SECURITY; Schema: public; Owner: rafactory_rw
--

ALTER TABLE public.components ENABLE ROW LEVEL SECURITY;

--
-- Name: pieces; Type: ROW SECURITY; Schema: public; Owner: rafactory_rw
--

ALTER TABLE public.pieces ENABLE ROW LEVEL SECURITY;

--
-- Name: projects; Type: ROW SECURITY; Schema: public; Owner: rafactory_rw
--

ALTER TABLE public.projects ENABLE ROW LEVEL SECURITY;

--
-- Name: api_keys tenant_isolation; Type: POLICY; Schema: public; Owner: rafactory_rw
--

CREATE POLICY tenant_isolation ON public.api_keys USING (((company_guid = (current_setting('app.tenant'::text))::uuid) OR (current_setting('app.bypass_rls'::text, true) = 'true'::text)));


--
-- Name: articles tenant_isolation; Type: POLICY; Schema: public; Owner: rafactory_rw
--

CREATE POLICY tenant_isolation ON public.articles USING ((((company_guid = (current_setting('app.tenant'::text))::uuid) AND (is_active = true)) OR (current_setting('app.bypass_rls'::text, true) = 'true'::text)));


--
-- Name: assemblies tenant_isolation; Type: POLICY; Schema: public; Owner: rafactory_rw
--

CREATE POLICY tenant_isolation ON public.assemblies USING ((((company_guid = (current_setting('app.tenant'::text))::uuid) AND (is_active = true)) OR (current_setting('app.bypass_rls'::text, true) = 'true'::text)));


--
-- Name: companies tenant_isolation; Type: POLICY; Schema: public; Owner: rafactory_rw
--

CREATE POLICY tenant_isolation ON public.companies USING (((guid = (current_setting('app.tenant'::text))::uuid) OR (current_setting('app.bypass_rls'::text, true) = 'true'::text)));


--
-- Name: components tenant_isolation; Type: POLICY; Schema: public; Owner: rafactory_rw
--

CREATE POLICY tenant_isolation ON public.components USING ((((company_guid = (current_setting('app.tenant'::text))::uuid) AND (is_active = true)) OR (current_setting('app.bypass_rls'::text, true) = 'true'::text)));


--
-- Name: pieces tenant_isolation; Type: POLICY; Schema: public; Owner: rafactory_rw
--

CREATE POLICY tenant_isolation ON public.pieces USING ((((company_guid = (current_setting('app.tenant'::text))::uuid) AND (is_active = true)) OR (current_setting('app.bypass_rls'::text, true) = 'true'::text)));


--
-- Name: projects tenant_isolation; Type: POLICY; Schema: public; Owner: rafactory_rw
--

CREATE POLICY tenant_isolation ON public.projects USING ((((company_guid = (current_setting('app.tenant'::text))::uuid) AND (is_active = true)) OR (current_setting('app.bypass_rls'::text, true) = 'true'::text)));


--
-- Name: ui_templates tenant_isolation; Type: POLICY; Schema: public; Owner: rafactory_rw
--

CREATE POLICY tenant_isolation ON public.ui_templates USING (((company_guid = (current_setting('app.tenant'::text))::uuid) OR (current_setting('app.bypass_rls'::text, true) = 'true'::text)));


--
-- Name: users tenant_isolation; Type: POLICY; Schema: public; Owner: rafactory_rw
--

CREATE POLICY tenant_isolation ON public.users USING (((company_guid = (current_setting('app.tenant'::text))::uuid) OR (current_setting('app.bypass_rls'::text, true) = 'true'::text)));


--
-- Name: workstations tenant_isolation; Type: POLICY; Schema: public; Owner: rafactory_rw
--

CREATE POLICY tenant_isolation ON public.workstations USING (((company_guid = (current_setting('app.tenant'::text))::uuid) OR (current_setting('app.bypass_rls'::text, true) = 'true'::text)));


--
-- Name: ui_templates; Type: ROW SECURITY; Schema: public; Owner: rafactory_rw
--

ALTER TABLE public.ui_templates ENABLE ROW LEVEL SECURITY;

--
-- Name: users; Type: ROW SECURITY; Schema: public; Owner: rafactory_rw
--

ALTER TABLE public.users ENABLE ROW LEVEL SECURITY;

--
-- Name: workflow; Type: ROW SECURITY; Schema: public; Owner: rafactory_rw
--

ALTER TABLE public.workflow ENABLE ROW LEVEL SECURITY;

--
-- Name: workstations; Type: ROW SECURITY; Schema: public; Owner: rafactory_rw
--

ALTER TABLE public.workstations ENABLE ROW LEVEL SECURITY;

--
-- PostgreSQL database dump complete
--

