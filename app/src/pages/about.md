---
title: About
---

<div class="text-center">
  <Icon icon="mdi-information" class="text-4xl text-primary -mb-2 m-auto" />
  <h1 class="text-primary">Why AioFauna?</h1>
</div>

## What is AioFauna?

It's an opinionated full-stack framework for building Web Applications built on top of Aiohttp, Pydantic and FaunaDB and heavily influenced by FastAPI.

## Why AioFauna?

### Why FaunaDB?

The goal of the project is to build an Stack like MERN, LAMP or MEAN but with a python backend for full stack developers So picking the main database was the most crucial decission to make.
I chose FaunaDB because is suitable for the widest variety of uses cases since it has the following characteristics:

- Is Serverless (No O&M burden = NoOps)
- It's Globally distributed through a CDN so adding an additional layer of caching or message queueing will be optional and constrained to specific use cases.
- Is timezone aware, so you can query data based on the user's timezone.
- Is document based and relational at the same time, so and ODM could be built on top of it.
- It's extensible through an expression based functional language (FQL) with a rich set of features, so you can build complex queries and mutations.
- It has a generous Free Tier, so you can build a prototype or a small application without paying a dime.
- It's also a Graph based databse so it supports complex relational scenarios like social networks.
- **q**: `aiofauna` provides the `_Expr` object and FaunaClient as classmethods, so you can use the native driver directly to query your models from the class objects by wrapping a `Query` object with `_Expr` and passing it to the `FaunaClient` instance.
- **CRUD methods**: `aiofauna` provides CRUD operations out of the box:
  - **`get`**: instance coroutine that retrieves a single document by ref.
  - **`find_unique`**: classmethod coroutine that retrieves a single document by a unique field.
  - **`find_many`** to retrieve multiple documents by an indexed field.
  - `all` to retrieve all documents from a collection.
  - `create` to create a new document from an instance of the model.
  - `save` to upsert a document from an instance of the model.
  - `update` to update a document from the class object by providing the `ref` and the `data` to update as keyword arguments.
  - `delete` to delete a document from the class object by providing the `ref` as a keyword argument.
  - `delete_unique` to delete a document from the class object by providing the `ref` as a keyword argument.
  - `exists` to check if a document exists by providing the `ref` as a keyword argument.
  - `query` to query documents from the class object by providing the `Query` object as an string argument.
  - `gen_ts` to generate the TypeScript definition for the model.
  - `gen_store` to generate the Pinia store for the model.
  - `provision` to provision the collection and indexes and unique constraints for the model based on the `ModelField` object created by the `Field` factory function metadata.
  - The `ref` and `ts` fields are optional properties that are created when a document instance is created on the database and forms part of the schema definition.
  - All the fields and properties are correctly serialized via custom encoders and decoders and the `ModelField` object is used to validate the data before it's sent to the database.
  - The `ModelField` object is also used to generate the TypeScript definition for the model and the Pinia store.
  - The `ModelField` object is also used to provision the collection and indexes and unique constraints for the model.

### Why Aiohttp?

- It's a mature framework with a rich set of features built on top of asyncio and maintained by the Python Core Team.
- It provides both sides of the coin, the server and the client, enabling you to build a full stack application with a single framework, there will be little need to use other frameworks or libraries.
- It's extensible through middlewares and plugins, since the ecosystem is so rich not enough known yet, it enabled developers to customize the DX and leverage the shortcomings and advantages of the framework.
- It's fast, since it's built on top of asyncio and uvloop, it's one of the fastest frameworks out there.
- `Application` is the main object often used as singleton that can be used to store global state and share it across the application. It's `aiofauna` subclass `Api` enabled all the rich features provided by aiofauna such as automatic documentation, automatic serialization and deserialization of data between the database and the client, auto-provisioning, decorators, etc.
- `Request` object on REST endpoints is disoluted into the request signature in a FastAPI fashion way, by injecting directly the parameters into the endpoint function signature, according to the type annotations.
- `@sse` and `@webSocket` decorators with `path` and `query` params and no boilerplate code allow to explore further the capabilities of the framework by using Server Send Events and real time communication with WebSockets.
- `Swagger UI` can be accessed at `/docs` and speeds up development by providing quick feedback of the API that's being developed.
- `OpenAPI` can be accessed at `/openapi.json` and can be used to generate the client code for the API.
- `HTTPClient` wraps `ClientSession` and provides a simple interface to make different kind of HTTP requests to third party resources allowing developers to build seamless integrations without extra boilerplate code or dependencies.

## Why Pydantic?

- This is such a retorical question, but I'll answer it anyway, because it's the best data validation library out there hands down.
- It's extensible through custom validators and types, so you can build your own validators and types and use them across your application.
- It's fast, since it's built on top of dataclasses and uses the `__slots__` attribute to store the data, it's one of the fastest data validation libraries out there.
- It's flexible, since it's built on top of dataclasses, it's easy to extend and customize.
- It allows for some kind of metaprogramming through `ModelField` objects, so you can build your own custom validators and types and use them across your application.
- It's well documented and maintained by the community.

<br/>

<br/>
