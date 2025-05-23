--
-- PostgreSQL database dump
--

-- Dumped from database version 15.12
-- Dumped by pg_dump version 16.8 (Ubuntu 16.8-0ubuntu0.24.04.1)

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
-- Name: update_updated_at_column(); Type: FUNCTION; Schema: public; Owner: rafactory_rw
--

CREATE FUNCTION public.update_updated_at_column() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
    BEGIN
       NEW.updated_at = NOW();
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
    created_at timestamp with time zone DEFAULT now(),
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
    created_at timestamp with time zone DEFAULT now(),
    updated_at timestamp with time zone,
    guid uuid NOT NULL,
    project_guid uuid NOT NULL,
    component_guid uuid NOT NULL
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
    created_at timestamp with time zone DEFAULT now(),
    updated_at timestamp with time zone,
    guid uuid NOT NULL,
    project_guid uuid NOT NULL,
    component_guid uuid NOT NULL
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
    updated_at timestamp with time zone NOT NULL,
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
    created_at timestamp with time zone DEFAULT now(),
    updated_at timestamp with time zone,
    guid uuid NOT NULL,
    project_guid uuid NOT NULL
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
    created_at timestamp with time zone DEFAULT now(),
    updated_at timestamp with time zone,
    guid uuid NOT NULL,
    project_guid uuid NOT NULL,
    component_guid uuid NOT NULL,
    assembly_guid uuid
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
    created_at timestamp with time zone DEFAULT now(),
    guid uuid NOT NULL
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
    created_at timestamp without time zone DEFAULT now() NOT NULL,
    updated_at timestamp without time zone
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
    created_at timestamp with time zone DEFAULT now(),
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
    action_type character varying NOT NULL,
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
    created_at timestamp without time zone DEFAULT now() NOT NULL,
    updated_at timestamp with time zone
);


ALTER TABLE public.workstations OWNER TO rafactory_rw;

--
-- Name: ui_templates id; Type: DEFAULT; Schema: public; Owner: rafactory_rw
--

ALTER TABLE ONLY public.ui_templates ALTER COLUMN id SET DEFAULT nextval('public.ui_templates_id_seq'::regclass);


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

CREATE POLICY tenant_isolation ON public.articles USING (((company_guid = (current_setting('app.tenant'::text))::uuid) OR (current_setting('app.bypass_rls'::text, true) = 'true'::text)));


--
-- Name: assemblies tenant_isolation; Type: POLICY; Schema: public; Owner: rafactory_rw
--

CREATE POLICY tenant_isolation ON public.assemblies USING (((company_guid = (current_setting('app.tenant'::text))::uuid) OR (current_setting('app.bypass_rls'::text, true) = 'true'::text)));


--
-- Name: companies tenant_isolation; Type: POLICY; Schema: public; Owner: rafactory_rw
--

CREATE POLICY tenant_isolation ON public.companies USING (((guid = (current_setting('app.tenant'::text))::uuid) OR (current_setting('app.bypass_rls'::text, true) = 'true'::text)));


--
-- Name: components tenant_isolation; Type: POLICY; Schema: public; Owner: rafactory_rw
--

CREATE POLICY tenant_isolation ON public.components USING (((company_guid = (current_setting('app.tenant'::text))::uuid) OR (current_setting('app.bypass_rls'::text, true) = 'true'::text)));


--
-- Name: pieces tenant_isolation; Type: POLICY; Schema: public; Owner: rafactory_rw
--

CREATE POLICY tenant_isolation ON public.pieces USING (((company_guid = (current_setting('app.tenant'::text))::uuid) OR (current_setting('app.bypass_rls'::text, true) = 'true'::text)));


--
-- Name: projects tenant_isolation; Type: POLICY; Schema: public; Owner: rafactory_rw
--

CREATE POLICY tenant_isolation ON public.projects USING (((company_guid = (current_setting('app.tenant'::text))::uuid) OR (current_setting('app.bypass_rls'::text, true) = 'true'::text)));


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

