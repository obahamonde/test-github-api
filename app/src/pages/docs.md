---
title: Docs
---

<div class="text-center">
  <Icon icon="mdi-document" class="text-4xl text-primary -mb-2 m-auto" />
  <h1 class="text-primary">Core Concepts</h1>
</div>

## About HTTP

HTTP (Hypertext Transfer Protocol) is a layer 7 TCP Protocol for communication around the web. It enables the exchange of data between clients (such as web browsers) and servers (which host web applications and content). The HTTP protocol follows a request-response model, where clients send requests to servers, and servers respond with the requested data or status information.

Clients initiate communication by sending an HTTP request to a specific URL (Uniform Resource Locator). The request includes an HTTP verb, such as `GET`, `POST`, `PUT`, `DELETE`, or `PATCH`, which indicates the desired action to be performed on the server's resources. In addition, clients can include headers in the request to provide additional information, such as content types or authorization credentials.

Upon receiving a request, the server processes it and generates an HTTP response. The response typically includes a status code indicating the outcome of the request, such as 200 (OK) for successful requests, 404 (Not Found) for resources that cannot be located, or 500 (Internal Server Error) for server-side issues. The response also contains a body that carries the requested data or any relevant error messages.

HTTP supports various content types, allowing clients and servers to exchange structured data. Common content types include JSON (JavaScript Object Notation) for data serialization, XML (eXtensible Markup Language) for structured documents, and form data for submitting data via HTML forms. Clients and servers can specify the content type using the "Content-Type" header.

The HTTP protocol also includes mechanisms for establishing and maintaining stateful interactions between clients and servers. Techniques like cookies and session management enable the server to recognize and track clients across multiple requests, providing a personalized experience.

## About REST APIs

REST (Representational State Transfer) APIs provide a way for clients to interact with server-side resources over the web using standard HTTP protocols.

Swagger/OpenAPI: Swagger (now known as OpenAPI) is an specification that provides guidelines to design, document, and consume REST APIs allowing developers to define API endpoints, request/response payloads, headers, and other details in a machine-readable format. Swagger tools can generate interactive documentation, client SDKs, and server stubs based on this specification.

JSON (JavaScript Object Notation): JSON is a lightweight data interchange format commonly used in REST APIs. It provides a human-readable and machine-readable way to represent structured data. JSON objects consist of key-value pairs and can be nested to form complex data structures.

Serialization and Deserialization: Serialization is the process of converting data objects (such as model instances) into a suitable format for transmission or storage, like JSON. Deserialization, on the other hand, is the reverse process of converting received data (e.g., JSON) into native data objects. This process enables easy exchange of data between clients and servers.

Headers: HTTP headers carry additional metadata in both requests and responses. They can convey information like content type (using the "Content-Type" header), authentication credentials (using the "Authorization" header), caching directives (using the "Cache-Control" header), and more. Headers provide flexibility and customization options in API communication.

APIs empower us to create robust and scalable web services. By adhering to industry best practices and using tools like Swagger, we can streamline API development, documentation, and client integration, promoting efficient collaboration between API providers and consumers.

## About Server Sent Events and WebSockets

### WebSockets

WebSockets is a communication protocol that provides full-duplex communication between a client and a server over a single, long-lived connection. Unlike traditional HTTP, which follows a request-response model, WebSockets enable real-time, bidirectional communication, allowing both the client and the server to initiate data transmission.

With WebSockets, a persistent connection is established between the client and the server, allowing them to send messages to each other at any time. This two-way communication eliminates the need for repeated polling or refreshing of the web page to receive updates. WebSockets are particularly useful for real-time applications such as chat applications, collaborative editing tools, or live data streaming.

WebSockets use the WebSocket protocol, typically running on top of TCP, to establish the connection. The WebSocket protocol employs an upgrade mechanism during the initial handshake to switch from the regular HTTP protocol to the WebSocket protocol. Once the connection is established, both the client and server can send messages to each other using a simple message-based communication model.

### Server-Sent Events (SSE)

Server-Sent Events (SSE) is a unidirectional communication technology that enables the server to send updates to the client over a single, long-lived HTTP connection. Unlike WebSockets, SSE is primarily designed for server-to-client communication, with the server initiating the data transmission.

With SSE, the client establishes a regular HTTP connection to the server and sends a request to a specific URL. Instead of providing a response with the complete data immediately, the server holds the connection open and sends periodic updates, known as events, as they occur. These events can be simple text or structured data encoded in formats like JSON.

SSE leverages the EventSource API on the client-side, which provides an interface for handling incoming events. The client can register event listeners to receive and process the events sent by the server. SSE is well-suited for scenarios where the server needs to push real-time updates, such as stock tickers, news feeds, or live sports scores.

SSE relies on the simplicity of the HTTP protocol and works with existing web infrastructure, including proxies and load balancers. It allows for easy integration with server-side technologies and does not require any special server-side setup or additional protocols.

## About Databases

### FaunaDB and FQL:

FaunaDB is a distributed, globally consistent database designed for modern applications. It combines the benefits of SQL and NoSQL databases and provides a flexible data model with strong consistency guarantees. FaunaDB uses a query language called Fauna Query Language (FQL) for data manipulation and retrieval. FQL offers expressive querying capabilities, including support for transactions, indexes, and user-defined functions. With FaunaDB and FQL, we can build scalable and transactional applications while maintaining data integrity.

### Scalability Issues with SQL Databases:

SQL databases have traditionally faced challenges when it comes to scalability, especially in scenarios with high data volumes or heavy read and write loads. Scaling SQL databases often involves vertical scaling (increasing hardware resources of a single server) or horizontal scaling (distributing data across multiple servers). However, these approaches have limitations, such as potential performance bottlenecks, increased complexity, and difficulty in maintaining data consistency across nodes.

### Serverless Databases and Scalability:

Serverless databases have emerged as an alternative approach to address scalability challenges. These databases, such as FaunaDB and Amazon DynamoDB, offer automatic scaling and resource allocation based on demand. They handle infrastructure provisioning and scaling transparently, allowing us to focus on application logic rather than managing database resources. Serverless databases can scale to handle massive workloads and can adapt dynamically to fluctuations in traffic, making them well-suited for modern, cloud-native applications.

Serverless databases provide a pay-as-you-go model, where users only pay for the resources consumed during actual usage. This approach helps optimize costs and eliminates the need for capacity planning and overprovisioning.

Additionally, serverless databases often offer other advantages such as built-in security, high availability, and fault tolerance. They handle replication, data backups, and failover automatically, reducing the burden to manage these aspects.

By leveraging serverless databases, is possible to build highly scalable applications without worrying about the underlying infrastructure, enabling focus on delivering value and innovation.

# About the Project

The primary goal was to develop an asynchronous ODM for FaunaDB, since was found as the most suitable bullet to kill most of the birds. That idea then evolved into a full python backend framework. The project was developed using Python 3.8.10 and FaunaDB 2.12.0. It took part of FaunaDB codebase and integrated it with three primary modules, the `api`, `odm` and `client` modules, the overall architecture of the solution is as follows:

<img src='/aiofauna.drawio.svg'/>

<br/>
<br/>
<br/>
