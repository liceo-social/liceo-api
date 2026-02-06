INSERT INTO liceo_users 
(id, name, surname, username, password, created_by, created_at) 
VALUES 
(:id, :name, :surname, :username, :password, :created_by, :created_at) RETURNING id;