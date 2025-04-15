# 示例代码

本代码用于演示A2A能力的技术规范演进过程。示例代码分为3个子目录：

* [**Common**](/samples/python/common)  
所有示例代理和应用都使用的通用代码，用于通过HTTP实现A2A通信。

* [**Agents**](/samples/python/agents/README.md)  
使用多种框架编写的示例代理程序，演示工具操作场景。所有示例均使用通用的A2AServer。

* [**Hosts**](/samples/python/hosts/README.md)  
使用A2AClient的主机应用程序。包含一个CLI命令行界面（演示单代理任务完成）、可连接多个代理的mesop网页应用，以及可将任务分派给多个远程A2A代理的编排代理。

## 先决条件

- Python 3.13 或更高版本
- UV

## 运行示例

需要同时运行一个（或多个）[agent](/samples/python/agents/README.md) A2A服务器和任意一个[host application](/samples/python/hosts/README.md)。

以下示例演示如何运行langgraph代理与Python CLI主机的交互：

1. 进入samples/python目录：