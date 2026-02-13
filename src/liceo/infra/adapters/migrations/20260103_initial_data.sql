-- #######################
-- ###   PERMISSIONS   ###
-- #######################

-- USERS
INSERT INTO liceo_permissions (id, name, description) VALUES ('kKCRCZrgu6f7LmQeKeBpn4', 'USERS_LIST', 'allows listing users');
INSERT INTO liceo_permissions (id, name, description) VALUES ('wZwcsF4frKkXEDQNiT2vyi', 'USERS_SHOW', 'shows a specific user');
INSERT INTO liceo_permissions (id, name, description) VALUES ('BFtJeZG2AprxV4EQThYjzD', 'USERS_CREATE', 'allows creating a new user');
INSERT INTO liceo_permissions (id, name, description) VALUES ('NPFxsWHzDUdsYqsJReC9k8', 'USERS_UPDATE_DETAILS', 'allows updating user details');
INSERT INTO liceo_permissions (id, name, description) VALUES ('tKEqg6EMhAFb6og8VJuz7B', 'USERS_UPDATE_PASSWORD', 'allows updating user password');
INSERT INTO liceo_permissions (id, name, description) VALUES ('zrijiR9osDidEX6dQFp5hV', 'USERS_UPDATE_SECURITY', 'allows updating user security properties');

-- ROLES
INSERT INTO liceo_permissions (id, name, description) VALUES ('J9fYxw932HbnRs5RzaYbbs', 'ROLES_LIST', 'allows listing roles');
INSERT INTO liceo_permissions (id, name, description) VALUES ('JLEBxFv8WmocNkmmZyeyxT', 'ROLES_CREATE', 'allows creating a new role');

-- STORAGE
INSERT INTO liceo_permissions (id, name, description) VALUES ('8abQNKu4jXMrQPyrteBXcD', 'STORAGE_UPLOAD', 'allows to upload files');
INSERT INTO liceo_permissions (id, name, description) VALUES ('Fi9rbWdjGrcpLttbkLRHpL', 'STORAGE_DOWNLOAD', 'allows to download files');

-- #######################
-- ###      ROLES      ###
-- #######################

-- USERS
INSERT INTO liceo_roles (id, name, description) VALUES ('RZ2JLgj89aFmyjv6yngmJ7', 'ROLE_USER', 'default permission for regular users');

-- ADMINS
INSERT INTO liceo_roles (id, name, description) VALUES ('rDCJKyPVeGLfmboVS7PkXC', 'ROLE_ADMIN', 'allows any action in the system');

-- #######################
-- #  ROLES_PERMISSIONS  #
-- #######################

-- ADMIN/USERS_LIST
INSERT INTO liceo_roles_permissions (role_id, permission_id) VALUES ('rDCJKyPVeGLfmboVS7PkXC', 'kKCRCZrgu6f7LmQeKeBpn4');
-- ADMIN/USERS_SHOW
INSERT INTO liceo_roles_permissions (role_id, permission_id) VALUES ('rDCJKyPVeGLfmboVS7PkXC', 'wZwcsF4frKkXEDQNiT2vyi');
-- ADMIN/USERS_CREATE
INSERT INTO liceo_roles_permissions (role_id, permission_id) VALUES ('rDCJKyPVeGLfmboVS7PkXC', 'BFtJeZG2AprxV4EQThYjzD');
-- ADMIN/USERS_UPDATE_DETAILS
INSERT INTO liceo_roles_permissions (role_id, permission_id) VALUES ('rDCJKyPVeGLfmboVS7PkXC', 'NPFxsWHzDUdsYqsJReC9k8');
-- ADMIN/USERS_UPDATE_PASSWORD
INSERT INTO liceo_roles_permissions (role_id, permission_id) VALUES ('rDCJKyPVeGLfmboVS7PkXC', 'tKEqg6EMhAFb6og8VJuz7B');
-- ADMIN/USERS_UPDATE_SECURITY
INSERT INTO liceo_roles_permissions (role_id, permission_id) VALUES ('rDCJKyPVeGLfmboVS7PkXC', 'zrijiR9osDidEX6dQFp5hV');

-- ADMIN/ROLE_LIST
INSERT INTO liceo_roles_permissions (role_id, permission_id) VALUES ('rDCJKyPVeGLfmboVS7PkXC', 'J9fYxw932HbnRs5RzaYbbs');
-- ADMIN/ROLE_CREATE
INSERT INTO liceo_roles_permissions (role_id, permission_id) VALUES ('rDCJKyPVeGLfmboVS7PkXC', 'JLEBxFv8WmocNkmmZyeyxT');
-- ADMIN/STORAGE_UPLOAD
INSERT INTO liceo_roles_permissions (role_id, permission_id) VALUES ('rDCJKyPVeGLfmboVS7PkXC', '8abQNKu4jXMrQPyrteBXcD');
-- ADMIN/STORAGE_DOWNLOAD
INSERT INTO liceo_roles_permissions (role_id, permission_id) VALUES ('rDCJKyPVeGLfmboVS7PkXC', 'Fi9rbWdjGrcpLttbkLRHpL');

-- #######################
-- ###      USERS      ###
-- #######################

-- DEFAULT ADMIN USER (john.doe@liceo.social/superpassword)
INSERT INTO liceo_users (
    id,
    name,
    surname,
    username,
    password,
    password_expired,
    account_active,
    account_blocked,
    account_expired,
    created_at,
    created_by
)
VALUES 
(
    'ZLP35KRt4jm8EkaebeWjJP', 
    'John', 
    'Doe', 
    'john.doe@liceo.social', 
    '$2b$10$Yxoh.mrE75jD1U.U7dBYV.pPLkgh1pwpUKPXavugoFLuujp98Radu', 
    FALSE,
    TRUE,
    FALSE,
    FALSE,
    '2026-02-06T16:59:35.444164', 
    'ZLP35KRt4jm8EkaebeWjJP'
);

INSERT INTO liceo_users 
(
    id,
    name,
    surname,
    username,
    password,
    password_expired,
    account_active,
    account_blocked,
    account_expired,
    created_at,
    created_by
)
VALUES 
(
    'UAF65EbeDYf7X8CfjZfoqM', 
    'Pedro', 
    'Gutierrez', 
    'pedro.gutierrez@liceo.social', 
    '$2b$10$Yxoh.mrE75jD1U.U7dBYV.pPLkgh1pwpUKPXavugoFLuujp98Radu', 
    FALSE,
    TRUE,
    FALSE,
    FALSE,
    '2026-02-06T16:59:35.444164', 
    'ZLP35KRt4jm8EkaebeWjJP'
);

-- #######################
-- ###   ROLES_USERS   ###
-- #######################

-- ROLE_ADMIN (john.doe@liceo.social)
INSERT INTO liceo_roles_users (role_id, user_id) VALUES ('rDCJKyPVeGLfmboVS7PkXC', 'ZLP35KRt4jm8EkaebeWjJP');
-- ROLE_USER (pedro.gutierrez@liceo.social)
INSERT INTO liceo_roles_users (role_id, user_id) VALUES ('RZ2JLgj89aFmyjv6yngmJ7', 'UAF65EbeDYf7X8CfjZfoqM');