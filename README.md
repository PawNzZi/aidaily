# MCP Demo
[![smithery badge](https://smithery.ai/badge/@PawNzZi/aidaily)](https://smithery.ai/server/@PawNzZi/aidaily)

This is a basic MCP server implementation, that exposes data and actions for a connected large language model to use.

## Example usage for ChatGPT

Give the following instructions to ChatGPT after starting the server

```
- You are connected to a remote tool MCP Demo. 
- I will describe the usage of functions it contains, the schemas for each function's arguments, and the expected return format.

1. resources/list: Get a list of available resources. Takes no arguments, returns an array of resources with URIs and MIME types

2. tools/list: Get a list of available tools. Takes no arguments, returns an array of tool names

3. tools/call : Use a tool. Required parameters: 'name': The string name of the tool you want to use, 'params': A dictionary representing the tool's arguments

4. prompts/get: Retrieve a prompt. Required parameter: 'name': The string name of the prompt you want to retrieve, returns a string of the prompt text

Thank you, and welcome to MCP Demo
```

## Get Started

### Installing via Smithery

To install MCP Demo for Claude Desktop automatically via [Smithery](https://smithery.ai/server/@PawNzZi/aidaily):

```bash
npx -y @smithery/cli install @PawNzZi/aidaily --client claude
```

### Resources

The MCP Demo includes example resources that can be queried:

```
resources = [
  {"name": "Hello World", "uri": "text://hello-world", "mimeType": "text/plain"},
  {"name": "Introduction to Large Language Models", "uri": "text://introduction-to-llms", "mimeType": "text/plain"}
]

```

A line from an `Introduction to Large Language Models`
```
1. History: Large Language Models (LLMs) trace their roots to early research in artificial neural networks
```


The returned JSON-encoded response of the `tools/list` call should look something like:
```
{"jsonrpc":"2.0","id":1,"result":[{"name":"Example Tool","input":"Prompt","output":"Reply"}]}

```

Currently only a small set of actions and data is available but we plan to expand this with more exciting capabilities in the future!

## Installation

Ensure python is installed on the system and then do the following:

```
git clone THIS_REPOSITORY

pip install . 
```

Setup the .env with an `API_KEY="YOUR_KEY"`

## Run

Run the server with

```
python3 -m mcp_server
```

The server listens on port 8080
