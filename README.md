run docker-compose with some additional features

```yml
version: "3"

x-host-services:
  nextjs:
    command: cd frontend && yarn dev

services:
  mocker:
    labels:
      - watch
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

