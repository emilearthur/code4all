"""
A template example:
We creat a car sales reporter. we can store records of sales in an SQLite db table. 

We have two common task:
* Select all sales of new vechiles and output them to a the screen in a comma-delimited format 
* Output a comma-delimited list of all salespeople with their gross sales and save it to a  file that can be 
imported to a spreadsheet 

Steps:
* Connect to the db. 
* Construct a query for new vechile or gross sales. 
* Issue the query  
* Format the results into a comma-delimited string 
* Output the data to a file or email

** the query constuction and the output steps are different for the two task. 
"""

# Creating a db  and putting some sample data 
import sqlite3
import datetime

conn = sqlite3.connect("sales.db") 

#conn.execute("CREATE TABLE Sales (salesperson text, amt currency, year integer, model text, new boolean)")

conn.execute("INSERT INTO Sales (salesperson, amt, year, model, new) VALUES  ('Jane', 16000, 2010, 'Honda Fit', 'true')") 
conn.execute("INSERT INTO Sales (salesperson, amt, year, model, new) VALUES ('Crek', 9000, 2006, 'Ford Focus', 'false')")
conn.execute("INSERT INTO Sales (salesperson, amt, year, model, new) VALUES ('Mulan', 8000, 2004, 'Dodge Neon', 'false')") 
conn.execute("INSERT INTO Sales (salesperson, amt, year, model, new) VALUES ('Mulan', 28000, 2009, 'Ford Mustang', 'true')") 
conn.execute("INSERT INTO Sales (salesperson, amt, year, model, new) VALUES ('Gayle', 50000, 2010, 'Lincoln Navigator', 'true')") 
conn.execute("INSERT INTO Sales (salesperson, amt, year, model, new) VALUES ('John', 20000, 2008, 'Toyota Prius', 'false')") 
conn.commit()
conn.close()


class QueryTemplate:
    def connect(self):
        self.conn = sqlite3.connect("sales.db") 
    
    def construct_query(self):
        raise NotImplementedError()
    
    def do_query(self):
        results = self.conn.execute(self.query) 
        self.results = results.fetchall() 

    def format_results(self):
        output = [] 
        for row in self.results:
            row = [str(i) for i in row]
            output.append(", ".join(row))
        self.formatted_results = "\n".join(output)
    def output_results(self):
        raise NotImplementedError()

    def process_format(self):
        """ Ensures that each step is executed in order. 
        """
        self.connect() 
        self.construct_query() 
        self.do_query() 
        self.format_results() 
        self.output_results() 


class NewVehiclesQuery(QueryTemplate):
    def construct_query(self):
        self.query = "select * from Sales where new='true' " 
    
    def output_results(self):
        print(self.format_results) 


class UserGrossQuery(QueryTemplate):
    def construct_query(self):
        self.query = ("select salesperson, sum(amt) from Sales group by salesperson") 
    
    def output_results(self):
        filename = "gross_sales_{0}".format(datetime.date.today().strftime("%Y%m%d"))
        with open(filename, "w") as outfile:
            outfile.write(self.format_results) 


"""
To help with implementing subclasses, the two methods that are not specified raise
NotImplementedError. This is a common way to specify abstract interfaces in Python
when abstract base classes seem too heavyweight. The methods could have empty
implementations (with pass), or could be fully unspecified. Raising
NotImplementedError, however, helps the programmer understand that the class is
meant to be subclassed and these methods overridden. Empty methods or methods that do
not exist are harder to identify as needing to be implemented and to debug if we forget to
implement them.
"""