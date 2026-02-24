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

- `LICEO_API_POOL_SIZE`: number of persistent connections (default `5`)
- `LICEO_API_MAX_OVERFLOW`: extra temporary connections beyond pool_size (default `10`)
- `LICEO_API_POOL_TIMEOUT`: seconds to wait before giving up getting a conn (default `30`)
- `LICEO_API_POOL_RECYCLE`: recycle connections after N seconds (default `1800` -> 30 min)
- `LICEO_API_POOL_PRE_PING`: test connections before using (default `True`)


### Observability

TODO

### File

Liceo file storage configuration

- `LICEO_API_FILE_ROOT_PATH`: The root path where all files' hierarchy could be found (default `/tmp/liceo`)

### Mail

- `LICEO_API_MAIL_HOST`: Host of the mail server (default `mailpit-svc`)
- `LICEO_API_MAIL_PORT`: Port through the mail will be sent (default `1025`)
- `LICEO_API_MAIL_DEFAULT_SENDER`: Default mail sender (default `system@liceo.com`)

### Sherlock Queries

The Sherlock utilities can cache SQL files in production setting to True the following variable:

- `SHERLOCK_CACHE_SQL`: caches sql file resolution

Actually just with the variable present it will cache sql resolution. Remember to unset the variable if you'd like to work with queries in development and do changes on the fly.

```shell
unset SHERLOCK_CACHE_SQL
```