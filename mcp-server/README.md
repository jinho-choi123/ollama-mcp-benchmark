
## Description
This directory setup mcp-filesystem-server that runs with nodejs.

## Prerequisites
- Install Node.js **v22.14.0** using [fnm](https://github.com/Schniz/fnm)

## Getting Started
1. Make a directory that mcp-filesystem-server will play in. You can use any existing directory, but it is recommended to create a seperate directory for this.
```bash
$ mkdir filesys
```
2. Open run_filesys_mcp_server.sh and change the `./filesys/` to the directory you created in step 1.
```bash
$ vim run_filesys_mcp_server.sh
```
3. Run the script to start the server.
```bash
$ ./run_filesys_mcp_server.sh
```
4. (Optional) To debug the server, you can run mcp inspector.
```bash
$ ./run_mcp_inspector.sh
```


