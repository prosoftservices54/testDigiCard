CREATE TABLE Customer
(
    number VARCHAR(15) PRIMARY KEY NOT NULL,
    email VARCHAR(255),
    password VARCHAR(255),
    gender VARCHAR(10),
    role VARCHAR(40) default 'customer',
    games_to_use INT default 0,
    level INT default 1,
    total_points INT default 0,
    creation_date DATE,
    birth_date DATE,
    visit_rate FLOAT,
    visit_rate_noon FLOAT,
    visit_rate_evening FLOAT,
    notification_success_rate FLOAT,
    average_amount FLOAT
);

CREATE TABLE Orders
(
    id VARCHAR(20) PRIMARY KEY NOT NULL,
    customer_number VARCHAR(15) NOT NULL,
    date DATE,
    part_of_day INT,
    amount INT,
    starter INT,
    appetizer INT,
    FOREIGN KEY (customer_number) REFERENCES Customer(number)
);

CREATE TABLE Reward
(
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    label VARCHAR(500) NOT NULL,
    level_required INT,
    value INT DEFAULT 0
);

CREATE TABLE Customer_Reward
(
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    customer_number VARCHAR(15) NOT NULL,
    reward_id INTEGER NOT NULL,
    date DATE NOT NULL,
    date_used DATE,
    worked BOOLEAN DEFAULT FALSE,
    FOREIGN KEY (customer_number) REFERENCES Customer(number),
    FOREIGN KEY (reward_id) REFERENCES Reward(id)
);


CREATE TABLE Notification
(
    id VARCHAR(20) PRIMARY KEY NOT NULL,
    customer_number VARCHAR(15) NOT NULL ,
    date Date,
    FOREIGN KEY (customer_number) references Customer(number)
);


CREATE TABLE Links
(
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    name VARCHAR(500),
    url VARCHAR(5000)
);

CREATE TABLE Customer_Links
(
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    customer_number VARCHAR(15),
    link_id INTEGER,
    FOREIGN KEY (customer_number) REFERENCES Customer(number),
    FOREIGN KEY (link_id) REFERENCES Links(id)
);