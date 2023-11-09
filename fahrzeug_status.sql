--
-- PostgreSQL database dump
--

-- Dumped from database version 16.0 (Debian 16.0-1.pgdg120+1)
-- Dumped by pg_dump version 16.0

-- Started on 2023-11-08 16:24:26 CET

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

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- TOC entry 215 (class 1259 OID 16389)
-- Name: fahrzeug_status; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.fahrzeug_status (
    issi integer,
    status character varying,
    "timestamp" timestamp without time zone,
    id integer NOT NULL
);


ALTER TABLE public.fahrzeug_status OWNER TO postgres;

--
-- TOC entry 3206 (class 2606 OID 16402)
-- Name: fahrzeug_status fahrzeug_status_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.fahrzeug_status
    ADD CONSTRAINT fahrzeug_status_pkey PRIMARY KEY (id);


--
-- TOC entry 3207 (class 2620 OID 24583)
-- Name: fahrzeug_status status_notify_trigger; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE OR REPLACE FUNCTION new_status() RETURNS trigger AS $new_status$
BEGIN 
PERFORM pg_notify('status_notification', NEW::text);
RETURN NEW;
END;                                                                                             
$new_status$ LANGUAGE plpgsql;

CREATE TRIGGER status_notify_trigger AFTER INSERT ON public.fahrzeug_status FOR EACH ROW EXECUTE FUNCTION public.new_status();


-- Completed on 2023-11-08 16:24:29 CET

--
-- PostgreSQL database dump complete
--

