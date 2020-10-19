# luftdaten-archive-to-sql

## Download csv files
wget -r --no-parent https://archive.sensor.community/2020-07-04/

## Install python modules
pip3 install -r requirements.txt

## Create config.ini
Setup the database (currently only postgresql) and the folder with the csv files.

	[db]
	host=
	user=
	passwd=
	db=
	port=5432
	
	[data]
	folder=*.csv