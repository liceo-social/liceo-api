INSERT INTO liceo_roles_users 
(user_id, role_id) 
VALUES 
(:user_id, :role_id) RETURNING user_id;