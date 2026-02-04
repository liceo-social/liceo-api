INSERT INTO liceo_users 
(id, name, surname, username, password) 
VALUES 
(:id, :name, :surname, :username, :password) RETURNING id;