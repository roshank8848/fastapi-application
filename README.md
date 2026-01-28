### Fastapi application

Create `.env` and `.dev.env` file in the top level directory as the `docker-compose.yaml`. Populate the following contents on the `.env` file.

```
DATABASE_URL="mysql+pymysql://<user>:<password>@<host>:3306/<database>"
```

Create a `.dev.env` file with following content. This file will be used to build container in `docker-compose.yaml`

```
MYSQL_DATABASE=<database>
MYSQL_ROOT_PASSWORD=<root_password>
MYSQL_USER=<user>
MYSQL_PASSWORD=<password> 
```
Create image with `docker build -t <image>:<tag> .`. Use `docker-compose build` to build the image.


### Contributing Guidelines
