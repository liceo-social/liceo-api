## Configuration

### Environment variables

All configuration setings can be set via environmen variables. All these variables must start with `LICEO_API_` prefix

### Crypto

Crypto configuration has to do with security settings, for example, how jwt tokens are generated. These are the available settings:

- `LICEO_API_CRYPTO_SECRET_KEY`: Secret key to generate JWT tokens
- `LICEO_API_CRYPTO_ALGORITHM`: Algorithm used to generate JWT tokens
- `LICEO_API_CRYPTO_SALT`: Salt used to generate JWT tokens
- `LICEO_API_CRYPTO_TOKEN_EXPIRES_MINUTES`: How long JWT tokens live until they expire (default `30` minutes)

### Database 

The database variables are:

- `LICEO_API_DB_TYPE`: Type of the database (default `postgresql`)
- `LICEO_API_DB_NAME`: Name of the database (default `liceo`)
- `LICEO_API_DB_USERNAME`: Username to access database (default `username`)
- `LICEO_API_DB_PASSWORD`: Password to access database (default `password`)
- `LICEO_API_DB_DRIVER`: Driver to access database (default `pg8000`)
- `LICEO_API_DB_HOST`: Host name where the database can be located (default `postgres-svc`) 
- `LICEO_API_DB_PORT`: Port where the database is listening (default `5432`)


### Observability

TODO

### File

Liceo file storage configuration

- `LICEO_API_FILE_ROOT_PATH`: The root path where all files' hierarchy could be found (default `/tmp/liceo`)

### Mail

- `LICEO_API_MAIL_HOST`: Host of the mail server (default `mailpit-svc`)
- `LICEO_API_MAIL_PORT`: Port through the mail will be sent (default `1025`)
- `LICEO_API_MAIL_DEFAULT_SENDER`: Default mail sender (default `system@liceo.com`)