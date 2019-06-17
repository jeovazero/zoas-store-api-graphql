# Zoas Store Backend

<div align="center">

[![Build Status](https://travis-ci.com/jeovazero/zoas-store-api-graphql.svg?branch=master)](https://travis-ci.com/jeovazero/zoas-store-api-graphql)
[![Coverage Status](https://coveralls.io/repos/github/jeovazero/zoas-store-api-graphql/badge.svg?branch=master)](https://coveralls.io/github/jeovazero/zoas-store-api-graphql?branch=master)
[![black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)

</div>

A project of api graphql for a fictitious ecommerce (Zoas Store)

It used in the project:

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


**This version is only for tests :construction:, not for production**

**It still has some enhancements to do** :fire:


## Scripts :page_facing_up:

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

#### `make genSchema`
> Generate the _flaskr/graphqlr/schema.graphql_ file

#### `make formatterLinter`
> Run the `black` and `flake8`


### Environment Variables

The environment variables used are:

- POSTGRES_USER
- POSTGRES_PASSWORD
- POSTGRES_DB
- POSTGRES_PORT
- POSTGRES_HOST


## Graphql

`/graphql`

To see the full schema auto-generated go to [schema.graphql](/flaskr/graphqlr/schema.graphql), it is as a documentation for api.

```graphql
type Mutations {
  createCart(input: CreateCartInput!): CreateCartPayload
  deleteCart(input: DeleteCartInput!): DeleteCartPayload
  putProductToCart(input: PutProductToCartInput!): PutProductToCartPayload
  removeProductOfCart(input: RemoveProductOfCartInput!): RemoveProductOfCartPayload
  payCart(input: PayCartInput!): PayCartPayload
}

type Query {
  cart: [ProductCart]
  product(id: ID!): Product
  products(before: String, after: String, first: Int, last: Int): ProductConnection
  node(id: ID!): Node
}
```

#### Custom errors

A custom error come in the format:
> An additional `code` field in the error object
```
{
  "errors": [
    {
      "message": "The product quantity must be greater than zero and less than total",
      "code": "INVALID_PRODUCT_QUANTITY"
    }
  ],
  "data": {
    "putProductToCart": null
  }
}
```

| Code | Message |
| ---- | ----- |
| INVALID_SESSION | "The session has expired or is invalid" |
| INVALID_PRODUCT_QUANTITY | "The product quantity must be greater than zero and less than total" |
| INVALID_PRODUCT_ID | "The product with provided id not exist" |
| INVALID_CREDIT_CARD | "Problems in credit card informations" |
| LACK_OF_STOCK | "The product 'product_name' has lack in the stock" |


## Examples of API use

**1. Get products of store**

```sh
curl localhost:3000/graphql \
-H "Content-Type: application/json" \
-d @- << EOF
{
    "query":
    "query {
       products(first: 5){
         pageInfo {
           hasNextPage
         }
         edges{
           cursor
           node {
             title
             price
             id
           }
         }
       }
    }"
}
EOF
```
> Getting the 5 first items

> This `query products` is a [Relay Connection](https://facebook.github.io/relay/graphql/connections.htm)

**2. Create a cart (session of user)**

```sh
curl localhost:3000/graphql \
-c "zoas.cookie" \
-H "Content-Type: application/json" \
-d @- << EOF
{
    "query":
    "mutation {
       createCart(input: { clientMutationId: \"b5e27614-8ee4-47ad-b1b6-60417d41e91c\" }){
         confirmation
         clientMutationId
       }
    }"
}
EOF
```

> For all mutations you must pass a `clientMutationId` conforms [Relay Input Object Mutation](https://facebook.github.io/relay/graphql/mutations.htm)

> It will create a session for the user creating a cookie

> The browser handle it automatically, but the `curl` command not made this, then use `-c "zoas.cookie"` to create a cookie and `-b "zoas.cookie"` to use the cookie

> All operations using `cart` you must send the cookie (The browser do it automatically)

**3. Put a product in the cart**

```sh
curl localhost:3000/graphql \
-b "zoas.cookie" \
-H "Content-Type: application/json" \
-d @- << EOF
{
    "query":
    "mutation {
       putProductToCart(input: {
         clientMutationId: \"c6e24c6d-d12a-419f-9ad7-d41b81debd04\",
         id: \"UHJvZHVjdDox\",
         quantity: 4
       }){
         payload {
            title
            description
         }
         clientMutationId
       }
    }"
}
EOF
```

**4. Get the products of cart**

```sh
curl localhost:3000/graphql \
-b "zoas.cookie" \
-H "Content-Type: application/json" \
-d @- << EOF
{
    "query":
    "query {
       cart {
         id
         title
         description
         price
       }
    }"
}
EOF
```

## Docker :whale:

#### Building

```
docker-compose build
```


#### Running

```
docker-compose up
```

> API Running on: localhost:3000/graphql

> Access it to do interactive graphql queries

> This version is not for production

#

by <a href="https://github.com/jeovazero">@jeovazero</a>
