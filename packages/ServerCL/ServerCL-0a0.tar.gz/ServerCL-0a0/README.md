## ServerCL

ServerCL is a library I had originally wanted to make so that I could use it only for my Sixth Form computing project to add local multiplayer to the game however realised that it would be just a little bit extra to make it more modifiable so that it could be used by a multitude of things.

Using ServerCL, you can register events, sending and receiving information both server and client side with completely customisable effects and minimal effort. 

To get started hosting a server is as simple as

```py
import ServerCL

my_server = ServerCL.Server(ServerCL.MACHINE_IP, ServerCL.GET_OPEN_PORT())

my_server.start()
```

This can then of course be customised using registering events to make something like an easy program that allows you to send and receive text information!

#### For more information including tutorials and documentation, visit the wiki @ [Github](https://github.com/shauncameron/server-server_client/wiki)