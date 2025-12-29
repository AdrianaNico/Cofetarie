--
-- PostgreSQL database dump
--

\restrict ujrdvKUfmroH5NQFOzwgvvPz9qCNtPqg9fen8x03F1nDXYFEepbMTOEM3lT6XFf

-- Dumped from database version 18.1
-- Dumped by pg_dump version 18.1

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Data for Name: Cofetarie_ingrediente; Type: TABLE DATA; Schema: django; Owner: adriana
--

INSERT INTO django."Cofetarie_ingrediente" (id, nume_ingredient, este_alergen, detalii_alergen) VALUES (1, 'Făină', true, 'gluten');
INSERT INTO django."Cofetarie_ingrediente" (id, nume_ingredient, este_alergen, detalii_alergen) VALUES (2, 'Lapte', true, 'lactate');
INSERT INTO django."Cofetarie_ingrediente" (id, nume_ingredient, este_alergen, detalii_alergen) VALUES (3, 'Cacao', false, '');
INSERT INTO django."Cofetarie_ingrediente" (id, nume_ingredient, este_alergen, detalii_alergen) VALUES (4, 'Unt', true, 'lactate');
INSERT INTO django."Cofetarie_ingrediente" (id, nume_ingredient, este_alergen, detalii_alergen) VALUES (5, 'Praf de copt', false, '');
INSERT INTO django."Cofetarie_ingrediente" (id, nume_ingredient, este_alergen, detalii_alergen) VALUES (6, 'Zahăr', false, '');
INSERT INTO django."Cofetarie_ingrediente" (id, nume_ingredient, este_alergen, detalii_alergen) VALUES (7, 'Ouă', false, '');
INSERT INTO django."Cofetarie_ingrediente" (id, nume_ingredient, este_alergen, detalii_alergen) VALUES (8, 'Vanilie', false, '');
INSERT INTO django."Cofetarie_ingrediente" (id, nume_ingredient, este_alergen, detalii_alergen) VALUES (9, 'Căpșuni', false, '');
INSERT INTO django."Cofetarie_ingrediente" (id, nume_ingredient, este_alergen, detalii_alergen) VALUES (10, 'Fistic', true, '');


--
-- Name: Cofetarie_ingrediente_id_seq; Type: SEQUENCE SET; Schema: django; Owner: adriana
--

SELECT pg_catalog.setval('django."Cofetarie_ingrediente_id_seq"', 10, true);


--
-- PostgreSQL database dump complete
--

\unrestrict ujrdvKUfmroH5NQFOzwgvvPz9qCNtPqg9fen8x03F1nDXYFEepbMTOEM3lT6XFf

--
-- PostgreSQL database dump
--

\restrict NC3VESUF5unuCIOB3ddVyKDPoD7qdzAIkhWWfqmyO6AS8zD9pGEeRUf1DngPd6a

-- Dumped from database version 18.1
-- Dumped by pg_dump version 18.1

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Data for Name: Cofetarie_locatie; Type: TABLE DATA; Schema: django; Owner: adriana
--



--
-- Name: Cofetarie_locatie_id_seq; Type: SEQUENCE SET; Schema: django; Owner: adriana
--

SELECT pg_catalog.setval('django."Cofetarie_locatie_id_seq"', 1, false);


--
-- PostgreSQL database dump complete
--

\unrestrict NC3VESUF5unuCIOB3ddVyKDPoD7qdzAIkhWWfqmyO6AS8zD9pGEeRUf1DngPd6a

--
-- PostgreSQL database dump
--

\restrict LKsPecYgT8WembdlEneObiDHadXxVB3BejrPsLShY6GluCNDIh4J12bOiihdbCb

-- Dumped from database version 18.1
-- Dumped by pg_dump version 18.1

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Data for Name: Cofetarie_optiuni_decoratiune; Type: TABLE DATA; Schema: django; Owner: adriana
--



--
-- Name: Cofetarie_optinuni_decoratiune_id_seq; Type: SEQUENCE SET; Schema: django; Owner: adriana
--

SELECT pg_catalog.setval('django."Cofetarie_optinuni_decoratiune_id_seq"', 1, false);


--
-- PostgreSQL database dump complete
--

\unrestrict LKsPecYgT8WembdlEneObiDHadXxVB3BejrPsLShY6GluCNDIh4J12bOiihdbCb

--
-- PostgreSQL database dump
--

\restrict ZCxHPiAhC8WTS4JT6AX9ATYjs8c4dkUPNsyDBoLG7xYSu96T5k4zQejuk3tBTq2

-- Dumped from database version 18.1
-- Dumped by pg_dump version 18.1

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Data for Name: Cofetarie_optiuni_blat; Type: TABLE DATA; Schema: django; Owner: adriana
--



--
-- Name: Cofetarie_optiuni_blat_id_seq; Type: SEQUENCE SET; Schema: django; Owner: adriana
--

SELECT pg_catalog.setval('django."Cofetarie_optiuni_blat_id_seq"', 1, false);


--
-- PostgreSQL database dump complete
--

\unrestrict ZCxHPiAhC8WTS4JT6AX9ATYjs8c4dkUPNsyDBoLG7xYSu96T5k4zQejuk3tBTq2

--
-- PostgreSQL database dump
--

\restrict cikRLlh5FY3magw3NqZdxKenwLIQblYmVZeycUFCO78vCtRP9W6oogfpseeo6eY

-- Dumped from database version 18.1
-- Dumped by pg_dump version 18.1

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Data for Name: Cofetarie_optiuni_crema; Type: TABLE DATA; Schema: django; Owner: adriana
--



--
-- Name: Cofetarie_optiuni_crema_id_seq; Type: SEQUENCE SET; Schema: django; Owner: adriana
--

SELECT pg_catalog.setval('django."Cofetarie_optiuni_crema_id_seq"', 1, false);


--
-- PostgreSQL database dump complete
--

\unrestrict cikRLlh5FY3magw3NqZdxKenwLIQblYmVZeycUFCO78vCtRP9W6oogfpseeo6eY

--
-- PostgreSQL database dump
--

\restrict 31BQsPMm3D2HlKLg2Zg8DF8PhvQStojQOomOSM8CdmsNHCClKlhMaTEbxsjiUwu

-- Dumped from database version 18.1
-- Dumped by pg_dump version 18.1

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Data for Name: Cofetarie_organizator; Type: TABLE DATA; Schema: django; Owner: adriana
--



--
-- Name: Cofetarie_organizator_id_seq; Type: SEQUENCE SET; Schema: django; Owner: adriana
--

SELECT pg_catalog.setval('django."Cofetarie_organizator_id_seq"', 1, false);


--
-- PostgreSQL database dump complete
--

\unrestrict 31BQsPMm3D2HlKLg2Zg8DF8PhvQStojQOomOSM8CdmsNHCClKlhMaTEbxsjiUwu

--
-- PostgreSQL database dump
--

\restrict 8GXz2wChgbQDx0xkOyq2FGOUJt3bpvapxSYlDxD3KO0AD3ZM2b4qRzLviMxSvM9

-- Dumped from database version 18.1
-- Dumped by pg_dump version 18.1

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Data for Name: Cofetarie_prajitura; Type: TABLE DATA; Schema: django; Owner: adriana
--

INSERT INTO django."Cofetarie_prajitura" (id, nume_prajitura, descriere_prajitura, gramaj, pret, categorie, imagine) VALUES (1, 'Cinnamon Roll Ciocolata', 'Rulouri pufoase din aluat fraged, dospit lent, umplute cu unt fin, zahăr aromat și scorțișoară, îmbogățite cu bucăți generoase de ciocolată. Coapte până devin aurii și glazurate delicat, aceste cinnamon rolls îmbină perfect aroma caldă a scorțișoarei cu gustul intens al ciocolatei, oferind un desert irezistibil, ideal pentru orice moment al zilei.', 150, 20.00, 'CR', 'media/prajituri/Cinnamonrolls_ciocolata_nGLmhfV.png');


--
-- Name: Cofetarie_prajitura_id_seq; Type: SEQUENCE SET; Schema: django; Owner: adriana
--

SELECT pg_catalog.setval('django."Cofetarie_prajitura_id_seq"', 1, true);


--
-- PostgreSQL database dump complete
--

\unrestrict 8GXz2wChgbQDx0xkOyq2FGOUJt3bpvapxSYlDxD3KO0AD3ZM2b4qRzLviMxSvM9

--
-- PostgreSQL database dump
--

\restrict kkI5ZqtKcBK0coQaffikfDVeuXECL3GQlcCriwNv276ybRdrvDYQBAKwfBhdbnN

-- Dumped from database version 18.1
-- Dumped by pg_dump version 18.1

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Data for Name: Cofetarie_prajitura_ingrediente; Type: TABLE DATA; Schema: django; Owner: adriana
--

INSERT INTO django."Cofetarie_prajitura_ingrediente" (id, prajitura_id, ingrediente_id) VALUES (1, 1, 1);
INSERT INTO django."Cofetarie_prajitura_ingrediente" (id, prajitura_id, ingrediente_id) VALUES (2, 1, 2);
INSERT INTO django."Cofetarie_prajitura_ingrediente" (id, prajitura_id, ingrediente_id) VALUES (3, 1, 3);
INSERT INTO django."Cofetarie_prajitura_ingrediente" (id, prajitura_id, ingrediente_id) VALUES (4, 1, 4);
INSERT INTO django."Cofetarie_prajitura_ingrediente" (id, prajitura_id, ingrediente_id) VALUES (5, 1, 5);
INSERT INTO django."Cofetarie_prajitura_ingrediente" (id, prajitura_id, ingrediente_id) VALUES (6, 1, 6);
INSERT INTO django."Cofetarie_prajitura_ingrediente" (id, prajitura_id, ingrediente_id) VALUES (7, 1, 7);


--
-- Name: Cofetarie_prajitura_ingrediente_id_seq; Type: SEQUENCE SET; Schema: django; Owner: adriana
--

SELECT pg_catalog.setval('django."Cofetarie_prajitura_ingrediente_id_seq"', 7, true);


--
-- PostgreSQL database dump complete
--

\unrestrict kkI5ZqtKcBK0coQaffikfDVeuXECL3GQlcCriwNv276ybRdrvDYQBAKwfBhdbnN

--
-- PostgreSQL database dump
--

\restrict dLpRygNGiS0fTcACMZjcuSOOQve84wfSjcn46rqF2pNyj29zKce0JWJXbdeTFcE

-- Dumped from database version 18.1
-- Dumped by pg_dump version 18.1

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Data for Name: Cofetarie_tort; Type: TABLE DATA; Schema: django; Owner: adriana
--



--
-- Name: Cofetarie_tort_id_seq; Type: SEQUENCE SET; Schema: django; Owner: adriana
--

SELECT pg_catalog.setval('django."Cofetarie_tort_id_seq"', 1, false);


--
-- PostgreSQL database dump complete
--

\unrestrict dLpRygNGiS0fTcACMZjcuSOOQve84wfSjcn46rqF2pNyj29zKce0JWJXbdeTFcE

--
-- PostgreSQL database dump
--

\restrict 0d3qybarB3GL9Ef8irZeobpoodHJuBKON4M0fSeYWKFpKdQV12inFsiqMv8xtLZ

-- Dumped from database version 18.1
-- Dumped by pg_dump version 18.1

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Data for Name: Cofetarie_tort_ingrediente; Type: TABLE DATA; Schema: django; Owner: adriana
--



--
-- Name: Cofetarie_tort_ingrediente_id_seq; Type: SEQUENCE SET; Schema: django; Owner: adriana
--

SELECT pg_catalog.setval('django."Cofetarie_tort_ingrediente_id_seq"', 1, false);


--
-- PostgreSQL database dump complete
--

\unrestrict 0d3qybarB3GL9Ef8irZeobpoodHJuBKON4M0fSeYWKFpKdQV12inFsiqMv8xtLZ

