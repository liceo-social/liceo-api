SELECT id 
FROM liceo_users lu
WHERE lu.username = :username
AND lu.password = :password;