INSERT INTO Customer (number, email, password, gender, creation_date, birth_date, visit_rate, visit_rate_noon, visit_rate_evening, notification_success_rate, average_amount)
VALUES
('+33 6 12 34 56 78', 'alice@example.com', 'admin', 'Female', '2023-01-15', '1990-05-20', 75, 80, 70, 95, 50.0),
('+44 7911 123456', 'bob@example.com', 'admin','Male', '2022-06-20', '1985-08-10', 60, 55, 65, 85, 30.0),
('+1 202-555-0123', 'charlie@example.com', 'admin','Male', '2024-03-10', '1992-11-25', 90, 85, 95, 98, 70.0),
('+49 170 1234567', 'diana@example.com', 'admin','Female', '2023-09-01', '1989-12-15', 45, 50, 40, 80, 40.0),
('+34 612 345 678', 'eva@example.com', 'admin','Female', '2021-11-11', '1995-03-30', 65, 70, 60, 90, 60.0),
('+33 7 89 01 23 45', 'frank@example.com', 'admin','Male', '2020-04-05', '1988-02-28', 80, 75, 85, 92, 55.0),
('+61 412 345 678', 'hank@example.com', 'admin','Male', '2024-01-25', '1994-01-14', 50, 55, 45, 80, 35.0),
('+39 331 2345678', 'irene@example.com', 'admin','Female', '2021-03-22', '1996-06-30', 55, 58, 52, 85, 65.0),
('+1 646-555-9876', 'jack@example.com', 'admin','Male', '2023-02-17', '1991-09-22', 78, 80, 75, 90, 75.0);


INSERT INTO Orders (id, customer_number, date, part_of_day, amount, starter, appetizer)
VALUES
('O001', '+33 6 12 34 56 78', '2024-11-01', 1, 50, 1, 0),
('O002', '+33 6 12 34 56 78', '2024-11-06', 1, 30, 1, 1),
('O003', '+1 202-555-0123', '2024-11-08', 1, 70, 0, 1),
('O004', '+33 6 12 34 56 78', '2024-10-20', 2, 40, 1, 0),
('O005', '+34 612 345 678', '2024-09-30', 2, 60, 0, 1),
('O006', '+33 7 89 01 23 45', '2024-10-25', 2, 55, 1, 0),
('O007', '+1 415-555-0198', '2024-11-10', 2, 45, 0, 1),
('O008', '+61 412 345 678', '2024-10-15', 2, 35, 1, 0),
('O009', '+39 331 2345678', '2024-10-12', 1, 65, 1, 1),
('O010', '+1 646-555-9876', '2024-11-18', 1, 75, 0, 1);


INSERT INTO Reward (id, label, level_required, value)
VALUES
(1, '10p Discount', 1, 10),
(2, 'Free Dessert', 5,15),
(3, '50p Off Next Order', 3, 50),
(4, 'Free Beverage', 4, 10),
(5, 'Free meal', 10, 20);


INSERT INTO Customer_Reward (customer_number, reward_id, date)
VALUES
('+33 6 12 34 56 78', 1, '2024-11-15'),
('+33 6 12 34 56 78', 2, '2024-10-05'),
('+1 202-555-0123', 3, '2024-11-08'),
('+49 170 1234567', 4, '2024-10-20'),
('+34 612 345 678', 5, '2024-09-30'),
('+33 6 12 34 56 78', 1, '2024-10-25'),
('+1 415-555-0198', 2, '2024-11-10'),
('+39 331 2345678', 4, '2024-10-12'),
('+1 646-555-9876', 5, '2024-11-18');



INSERT INTO Notification (id, customer_number, date)
VALUES
('N001', '+33 6 12 34 56 78', '2024-11-01'),
('N012', '+33 6 12 34 56 78', '2024-11-05'),
('N002', '+44 7911 123456', '2024-11-05'),
('N003', '+1 202-555-0123', '2024-11-08'),
('N004', '+49 170 1234567', '2024-10-20'),
('N005', '+34 612 345 678', '2024-09-30'),
('N006', '+33 7 89 01 23 45', '2024-10-25'),
('N007', '+1 415-555-0198', '2024-11-10'),
('N008', '+61 412 345 678', '2024-10-15'),
('N009', '+39 331 2345678', '2024-10-12'),
('N010', '+1 646-555-9876', '2024-11-18');


INSERT INTO Links (id, name, url)
VALUES
(1, 'Google', 'https://www.google.com'),
(2, 'Facebook', 'https://www.facebook.com'),
(3, 'Twitter', 'https://www.twitter.com'),
(4, 'Instagram', 'https://www.instagram.com'),
(5, 'LinkedIn', 'https://www.linkedin.com');


INSERT INTO Customer_Links (customer_number, link_id)
VALUES
('+33 6 12 34 56 78', 1),
('+33 6 12 34 56 78', 2);


UPDATE Customer SET total_points = 6 WHERE number = '+33 6 12 34 56 78';
UPDATE Customer SET games_to_use = 2 WHERE number = '+33 6 12 34 56 78';

UPDATE Customer_Reward SET worked = TRUE WHERE customer_number = '+33 6 12 34 56 78' AND reward_id = 'R001';
UPDATE Customer_Reward SET worked = TRUE WHERE customer_number = '+1 646-555-9876' AND reward_id = 'R005';
