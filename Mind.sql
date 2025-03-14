PGDMP  '    3                }            Mind    17.4    17.4     +           0    0    ENCODING    ENCODING        SET client_encoding = 'UTF8';
                           false            ,           0    0 
   STDSTRINGS 
   STDSTRINGS     (   SET standard_conforming_strings = 'on';
                           false            -           0    0 
   SEARCHPATH 
   SEARCHPATH     8   SELECT pg_catalog.set_config('search_path', '', false);
                           false            .           1262    16388    Mind    DATABASE     l   CREATE DATABASE "Mind" WITH TEMPLATE = template0 ENCODING = 'UTF8' LOCALE_PROVIDER = libc LOCALE = 'es-ES';
    DROP DATABASE "Mind";
                     postgres    false            �            1259    16428 
   resultados    TABLE     �   CREATE TABLE public.resultados (
    idresult integer NOT NULL,
    iduser integer,
    porcentaje_fatiga1 double precision,
    porcentaje_fatiga2 double precision,
    capacidad_perceptiva double precision,
    resultado_final double precision
);
    DROP TABLE public.resultados;
       public         heap r       postgres    false            �            1259    16427    resultados_idresult_seq    SEQUENCE     �   CREATE SEQUENCE public.resultados_idresult_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 .   DROP SEQUENCE public.resultados_idresult_seq;
       public               postgres    false    220            /           0    0    resultados_idresult_seq    SEQUENCE OWNED BY     S   ALTER SEQUENCE public.resultados_idresult_seq OWNED BY public.resultados.idresult;
          public               postgres    false    219            �            1259    16390    users    TABLE     �   CREATE TABLE public.users (
    iduser integer NOT NULL,
    usuario character varying(255) NOT NULL,
    "contraseña" character varying(255) NOT NULL
);
    DROP TABLE public.users;
       public         heap r       postgres    false            �            1259    16389    users_id_seq    SEQUENCE     �   CREATE SEQUENCE public.users_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 #   DROP SEQUENCE public.users_id_seq;
       public               postgres    false    218            0           0    0    users_id_seq    SEQUENCE OWNED BY     A   ALTER SEQUENCE public.users_id_seq OWNED BY public.users.iduser;
          public               postgres    false    217            �           2604    16431    resultados idresult    DEFAULT     z   ALTER TABLE ONLY public.resultados ALTER COLUMN idresult SET DEFAULT nextval('public.resultados_idresult_seq'::regclass);
 B   ALTER TABLE public.resultados ALTER COLUMN idresult DROP DEFAULT;
       public               postgres    false    219    220    220            �           2604    16393    users iduser    DEFAULT     h   ALTER TABLE ONLY public.users ALTER COLUMN iduser SET DEFAULT nextval('public.users_id_seq'::regclass);
 ;   ALTER TABLE public.users ALTER COLUMN iduser DROP DEFAULT;
       public               postgres    false    217    218    218            (          0    16428 
   resultados 
   TABLE DATA           �   COPY public.resultados (idresult, iduser, porcentaje_fatiga1, porcentaje_fatiga2, capacidad_perceptiva, resultado_final) FROM stdin;
    public               postgres    false    220   �       &          0    16390    users 
   TABLE DATA           ?   COPY public.users (iduser, usuario, "contraseña") FROM stdin;
    public               postgres    false    218   .       1           0    0    resultados_idresult_seq    SEQUENCE SET     E   SELECT pg_catalog.setval('public.resultados_idresult_seq', 2, true);
          public               postgres    false    219            2           0    0    users_id_seq    SEQUENCE SET     :   SELECT pg_catalog.setval('public.users_id_seq', 2, true);
          public               postgres    false    217            �           2606    16433    resultados resultados_pkey 
   CONSTRAINT     ^   ALTER TABLE ONLY public.resultados
    ADD CONSTRAINT resultados_pkey PRIMARY KEY (idresult);
 D   ALTER TABLE ONLY public.resultados DROP CONSTRAINT resultados_pkey;
       public                 postgres    false    220            �           2606    16397    users users_pkey 
   CONSTRAINT     R   ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (iduser);
 :   ALTER TABLE ONLY public.users DROP CONSTRAINT users_pkey;
       public                 postgres    false    218            �           2606    16399    users users_usuario_key 
   CONSTRAINT     U   ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_usuario_key UNIQUE (usuario);
 A   ALTER TABLE ONLY public.users DROP CONSTRAINT users_usuario_key;
       public                 postgres    false    218            �           2606    16434 !   resultados resultados_iduser_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.resultados
    ADD CONSTRAINT resultados_iduser_fkey FOREIGN KEY (iduser) REFERENCES public.users(iduser);
 K   ALTER TABLE ONLY public.resultados DROP CONSTRAINT resultados_iduser_fkey;
       public               postgres    false    4750    220    218            (   !   x�3�4��! �e�i���d�b���� �q�      &   r   x���C! ����^r�#��?�dX��<�Z�@Qu�)a��������wc��е��K9�t���c7\SF;h��Ђ��w�Iү�[}ҝh[Ic)��=߯9��'0     