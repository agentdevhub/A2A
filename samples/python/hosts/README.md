## Hosts

作为 A2A 客户端的示例应用或代理程序，与 A2A 服务器进行协作。

* [CLI](/samples/python/hosts/cli)  
  用于与 A2A 服务器交互的命令行工具。通过命令行指定服务器位置后，CLI 客户端会查找 agent card 并根据输入指令循环执行任务。

* [Orchestrator Agent](/samples/python/hosts/multiagent)  
  基于 Google ADK 构建的 A2A 通信代理，可将任务委派给远程代理。包含维护多个 Remote Agents 集合的 Host Agent（本身也是一个代理），能够将任务分派给一个或多个 Remote Agents。每个 RemoteAgent 都是通过 A2AClient 委派给 A2A 服务器的代理程序。

* [MultiAgent Web Host](/demo/README.md)  
*该组件位于 [demo](/demo/README.md) 目录*  
  可视化展示多代理 A2A 对话的网页应用（使用 [Orchestrator Agent](/samples/python/hosts/multiagent)），支持呈现文本、图像和网页表单内容，并提供独立标签页用于可视化任务状态、历史记录以及已知的 agent cards。