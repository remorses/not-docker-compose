run docker-compose with some additional features

features like
- run commands on the host, via `x-host-services` field
- restart a service when a volume changes (enable adding the label `watch`) 
- deploy the services to [Google Cloud Run]() with `not-docker-compose deploy` (enable adding the label `deploy`) 

```yml
version: "3"

x-host-services:
  nextjs:
    command: cd frontend && yarn dev

services:
  mocker:
    labels:
      - watch
      - deploy
    image: mongoke/graphql-mocker
    ports:
      - 7090:80
    depends_on:
      - mongoke
      - api
    environment:
      - PORT=80
      - URL=http://gateway
      - MOCKS_PATH=/mocks.js
      - PRESERVE_MUTATIONS=1
    volumes:
      - ./frontend/src/mocks.js:/mocks.js
```

