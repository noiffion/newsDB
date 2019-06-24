
## Three questions
   The program 'news.py' will answer three questions posed about the contents in the Postgresql 'news' database:
  1. What are the most popular three articles of all time?
  2. Who are the most popular article authors of all time?
  3. On which days did more than 1% of requests lead to errors?
 
The program runs on Linux and has been tested only on Linux.

#### Usage and required programs
   Running the program 'news.py' interactively displays the answers to the three questions above. 
 After connecting to the database creating the four SQL views necessary for obtaining the answers
 the three questions will be printed to the screen and the user has the possibility to choose
 between the questions prompting the program to display the answer to the screen in the standard
 psql table format.

 The necessary queries can be found in the 'Queries' directory as stand-alone txt files:
 * The four views necessary to obtain the answer
 * And the queries producing the answers
 The 'news.py' program will need these files as they are where they are to run correctly.

 Additional information about the queries and their output can be found in the threeq.txt
 file in the Queries directory.

 The sql statements for the four views are the following:

View_1:
 ```
CREATE OR REPLACE VIEW hit_per_page AS
SELECT COUNT(id) AS pageview,
CASE
WHEN path LIKE '/article/bad-things-gon%' THEN 'bad-things-gone'
WHEN path LIKE '/article/balloon-goons-doome%' THEN 'balloon-goons-doomed'
WHEN path LIKE '/article/bears-love-berrie%' THEN 'bears-love-berries'
WHEN path LIKE '/article/candidate-is-jer%' THEN 'candidate-is-jerk'
WHEN path LIKE '/article/goats-eat-google%' THEN 'goats-eat-googles'
WHEN path LIKE '/article/media-obsessed-with-bear%' THEN 'media-obsessed-with-bears'
WHEN path LIKE '/article/trouble-for-trouble%' THEN 'trouble-for-troubled'
WHEN path LIKE '/article/so-many-bear%' THEN 'so-many-bears'
ELSE 'Not article'
END AS slug
FROM log
GROUP BY slug
ORDER BY pageview DESC;
```

View_2:
```
CREATE OR REPLACE VIEW authors_articles AS
SELECT articles.title, articles.slug, authors.name, authors.id as author_id FROM
authors JOIN articles ON
authors.id = articles.author;
```

View_3:
```
CREATE OR REPLACE VIEW ok_200 AS
SELECT COUNT(id) AS sum, status, date_trunc('day', time) AS day
FROM log
WHERE status LIKE '%200%'
GROUP BY day, status
ORDER BY day;
```

View_4:
```
CREATE OR REPLACE VIEW error_404 AS
SELECT COUNT(id) AS sum, status, date_trunc('day', time) AS day
FROM log
WHERE status LIKE '%404%'
GROUP BY day, status
ORDER BY day;
```


 The database can be downloaded [from here](https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f748_newsdata/newsdata.zip)
 
 And attached here as newsdata.sql.gz.
 
 Because the database and the program runs only on Linux the installation of 'VirtualBox' and 
 'Vagrant' is also needed apart from Postgresql and the third version of Python:
 ```
 $ sudo apt install python3
 $ sudo apt install python3-pip
 $ sudo apt install postgresql
 $ sudo apt install python3-psycopg2
 $ sudo apt install vagrant
 $ sudo apt install virtualbox
 ```
 Vagrant and Virtual Box are creating a virtual Linux (Ubuntu) operating system where the
 programs can be run.

 Then creating the 'vagrant' directory the:
 ```
 $ psql -d news -f newsdata.sql
 ```
 command will create the database from the downloaded 'newsdata.sql' file. 
 (If not then we have to create a database named 'news' for the user in psql with the 
  CREATE DATABASE news WITH OWNER vagrant; 
  - and then run the command above).

 And with the 'vagrant up' and 'vagrant ssh' commands one can connect to the virtual machine
 where the program can be run. 
 Finally to start the program type the following in the (virtual) Linux shell:
 ```
 $ python3 news.py
 ```
 After starting the program every information the user needs to move forward will be
 displayed on the screen.
 
#### Contributors
  The database is created by Karl Krueger and can be accessed [here](https://github.com/udacity/fullstack-nanodegree-vm).

#### License
 MIT License
