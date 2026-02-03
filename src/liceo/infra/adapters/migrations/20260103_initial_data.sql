-- PERMISSIONS_USERS
INSERT INTO liceo_permissions (id, name, description) VALUES ('kKCRCZrgu6f7LmQeKeBpn4', 'USERS_LIST', 'allows listing users');
INSERT INTO liceo_permissions (id, name, description) VALUES ('BFtJeZG2AprxV4EQThYjzD', 'USERS_CREATE', 'allows creating a new user');

-- PERMISSIONS_ROLES
INSERT INTO liceo_permissions (id, name, description) VALUES ('J9fYxw932HbnRs5RzaYbbs', 'ROLES_LIST', 'allows listing roles');
INSERT INTO liceo_permissions (id, name, description) VALUES ('JLEBxFv8WmocNkmmZyeyxT', 'ROLES_CREATE', 'allows creating a new role');


-- ROLES
INSERT INTO liceo_roles (id, name, description) VALUES ('RZ2JLgj89aFmyjv6yngmJ7', 'ROLE_USER', 'default permission for regular users');
INSERT INTO liceo_roles (id, name, description) VALUES ('rDCJKyPVeGLfmboVS7PkXC', 'ROLE_ADMIN', 'allows any action in the system');


-- ROLE_ADMIN_USERS_LIST
INSERT INTO liceo_roles_permissions (role_id, permission_id) VALUES ('rDCJKyPVeGLfmboVS7PkXC', 'kKCRCZrgu6f7LmQeKeBpn4')
-- ROLE_ADMIN_USERS_CREATE
INSERT INTO liceo_roles_permissions (role_id, permission_id) VALUES ('rDCJKyPVeGLfmboVS7PkXC', 'BFtJeZG2AprxV4EQThYjzD')
-- ROLE_ADMIN_ROLE_LIST
INSERT INTO liceo_roles_permissions (role_id, permission_id) VALUES ('rDCJKyPVeGLfmboVS7PkXC', 'J9fYxw932HbnRs5RzaYbbs')
-- ROLE_ADMIN_ROLE_CREATE
INSERT INTO liceo_roles_permissions (role_id, permission_id) VALUES ('rDCJKyPVeGLfmboVS7PkXC', 'JLEBxFv8WmocNkmmZyeyxT')