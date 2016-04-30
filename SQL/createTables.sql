CREATE TABLE availability
(
   block_id        int(11),
   available       int(11),
   datetimestamp   timestamp DEFAULT 'CURRENT_TIMESTAMP'
);


------------------------------------------------------------------
--  TABLE edges
------------------------------------------------------------------

CREATE TABLE edges
(
   block_id      int(11),
   block_name    varchar(128),
   latitude_1    char(20),
   longitude_1   char(20),
   latitude_2    char(20),
   longitude_2   char(20),
   node_id_1     int(11),
   node_id_2     int(11),
   no_blocks     int(11),
   operational   int(11),
   latitude      char(20),
   longitude     char(20)
);


------------------------------------------------------------------
--  TABLE nodes
------------------------------------------------------------------

CREATE TABLE nodes
(
   node_id      int(11),
   latitude     char(20),
   longitude    char(20),
   node_name    varchar(128),
   coordinate   point
);


------------------------------------------------------------------
--  TABLE probabilistic_data
------------------------------------------------------------------

CREATE TABLE probabilistic_data
(
   block_id      int(11),
   available     decimal(20, 18),
   operational   int(11),
   probability   decimal(20, 18),
   hour_of_day   char(2)
);