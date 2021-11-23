/*CREATE TABLE Sales (salesperson text, amt currency, year integer, model text, new boolean) 

INSERT INTO Sales (salesperson, amt, year, model, new) VALUES  ('Tim', 16000, 2010, 'Honda Fit', 'true');
INSERT INTO Sales (salesperson, amt, year, model, new) VALUES ('Tim', 9000, 2006, 'Ford Focus', 'false');
INSERT INTO Sales (salesperson, amt, year, model, new) VALUES ('Gayle', 8000, 2004, 'Dodge Neon', 'false');
INSERT INTO Sales (salesperson, amt, year, model, new) VALUES ('Gayle', 28000, 2009, 'Ford Mustang', 'true');
INSERT INTO Sales (salesperson, amt, year, model, new) VALUES ('Gayle', 50000, 2010, 'Lincoln Navigator', 'true');
INSERT INTO Sales (salesperson, amt, year, model, new) VALUES ('Don', 20000, 2008, 'Toyota Prius', 'false');

*/

Select * FROM Sales WHERE new="true" AND year >= 2004
