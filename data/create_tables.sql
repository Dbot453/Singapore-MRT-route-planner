CREATE TABLE "station" (
"station_code" TEXT,
"station_name" TEXT,
"line_name" TEXT,
"line_colour" TEXT,
"latitude" NUMERIC,
"longitude" NUMERIC,
PRIMARY KEY("station_code")
)


CREATE TABLE "distance" (
"id" INTEGER,
"station1" TEXT,
"station2" TEXT,
"line" TEXT,
"distance" NUMERIC,
PRIMARY KEY("id" AUTOINCREMENT)
)

CREATE TABLE "adjacent_stations" (
"id" INTEGER,
"station_code" TEXT NOT NULL,
"neighbour" TEXT NOT NULL,
PRIMARY KEY("id" AUTOINCREMENT)
)

CREATE TABLE route (
	id INTEGER NOT NULL, 
	start VARCHAR(150), 
	dest VARCHAR(150), 
	distance FLOAT, 
	travel_time FLOAT, 
	path_codes VARCHAR(10000), 
	path_names VARCHAR(10000), 
	save_datetime DATETIME, 
	user_id INTEGER, 
	PRIMARY KEY (id), 
	FOREIGN KEY(user_id) REFERENCES user (id)
)

create TABLE transfer_time (
	station_name VARCHAR(150),
	start_line VARCHAR(150),
	start_code VARCHAR(20),
	end_line VARCHAR(150),
	end_code VARCHAR(20),
	transfer_time_seconds NUMERIC);


