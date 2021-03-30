# Harvest API

Backend REST API to get statistics about CGI projects. Harvest mixes data from
tractor and shotgun and display these statistics through the Harvest GUI web application.

## Get started

To install :

```bash
repository/location/ pip install .
```

To start the server :

```bash
python -m harvest_api
```

OR

To start the server without install :

```bash
repository/location/harvest_api python app.py
```

### Options

- -e or --environment \<environmentpreset\> :
Set the default values of the specifyed environment
for development environment : dev or development
for production environment : prod or production

- -h or --host \<hostname\> :
Set the host adress of the tractor's database
(dev default : localhost:5432, prod default : localhost:9876)

- -u or --user \<username\> :
Set the postgresql username of the tractor's database
(dev default : postgres, prod default : root)

- -p or --port \<portnumber\> :
Set the port of the flask server
(dev default : 8080, prod default : 5000)

### Dependencies

- flask
- flask_cors
- waitress
- psycopg2
- sqlalchemy
- apscheduler

To install all the dependencies at once :

```bash
repository/location pip install -r requirements.txt
```

## Usage

### Routes

- /infos/projects :

Return a list of JSON containing the name, the color and the id for each project
in the database

```url
/stats/farm-usage
```

Return a JSON with the quantity of blades currently free, busy, nimby and off

```url
/stats/projects-usage
```

Return a JSON with the quantity of blades working for each project

```url
/stats/blades-usage
```

Return a JSON with the quantity of blades working for each types of blades
(MK4, MK8, MK10, ...)

```url
/stats/farm-history/hours
```

URL Parameters :

- start (int) timestamp (javascript precision) : date from wich we compute the average
- end (int) timestamp (javascript precision) : date until wich we compute the average
- ignore-we (bool) : specify if we ignore data from saturday and sunday when we
compute the average

Return a list of JSON with the average amount of blades free, busy, nimby and off
along each hours of a day

```url
/stats/farm-history/days
```

URL Parameters :

- start (int) timestamp (javascript precision) : date from wich we compute the average
- end (int) timestamp (javascript precision) : date until wich we compute the average

Return a list of JSON with the average amount of blades free, busy, nimby and off
along each days of a week

```url
/stats/farm-history/days
```

URL Parameters :

- start (int) timestamp (javascript precision) : date from wich we compute the average
- end (int) timestamp (javascript precision) : date until wich we compute the average

Return a list of JSON with the average amount of blades free, busy, nimby and off
along each days of a week
