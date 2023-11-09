--
-- PostgreSQL database dump
--

-- Dumped from database version 16.0 (Debian 16.0-1.pgdg120+1)
-- Dumped by pg_dump version 16.0

-- Started on 2023-11-09 13:05:53 CET

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
-- TOC entry 216 (class 1259 OID 16415)
-- Name: fahrzeuge; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.fahrzeuge (
    issi integer NOT NULL,
    funkrufname character varying NOT NULL
);


ALTER TABLE public.fahrzeuge OWNER TO postgres;

-- Completed on 2023-11-09 13:05:56 CET

--
-- PostgreSQL database dump complete
--

