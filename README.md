# Zoas Store Backend

<div align="center">

[![Build Status](https://travis-ci.com/jeovazero/zoas-store-backend.svg?branch=master)](https://travis-ci.com/jeovazero/zoas-store-backend)
[![Coverage Status](https://coveralls.io/repos/github/jeovazero/zoas-store-backend/badge.svg?branch=master)](https://coveralls.io/github/jeovazero/zoas-store-backend?branch=master)
[![black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)

</div>

A project of api graphql for a fictitious ecommerce (Zoas Store)

For learning of some libs and best practices of python ecosystem

It utilized in the project:

- Lang: **Python3.7**
- Framework: **Flask**
- Graphql: **Graphene Python**
- ORM: **SqlAlchemy**
- Database: **PostgreSQL 11**
- StyleGuide: **Black** + **Flask8**
- Type check: **Mypy**
- Git hook: **pre-commit**
- Test: **pytest**
- CI: **Travis**
- Coverage: **Coveralls**


**This version is only for tests**

**In the next release will support Relay**


## Scripts

#### `make init`
> Create a virtual env and install the dependencies of project

#### `make start`
> Run app in development mode (api running on: localhost:5000/graphql)

#### `make install`
> Install dependencies of requirements file

#### `make upgradeInstall`
> Upgrade dependencies and install them

#### `make test`
> Run tests

#### `make testCoverage`
> Run tests with coverage

#### `make gunicorn`
> Run the app with gunicorn


## Graphql

`/graphql`

To see the full schema auto-generated go to [schema.graphql](/graphql/schema.graphql), it is as a documentation for api.

```graphql
type Mutations {
  createCart: CreateCart
  deleteCart: DeleteCart
  putProductToCart(payload: PutProductInput!): [ProductCart]
  removeProductOfCart(productId: String!): [ProductCart]
  payCart(payload: PayCartInput!): PayCart
}

type Query {
  cart: [ProductCart]
  product(productId: String!): Item
  products(offset: Int = 0, limit: Int = 10): Products
}
```

## Docker

#### Building

```
docker-compose build
```


#### Running

```
docker-compose up
```

> API Running on: localhost:3000/graphql

#

by <a href="https://github.com/jeovazero">@jeovazero</a>
