## 演示 Web 应用

本演示应用展示Agent之间通过A2A进行通信的场景。

![image](/images/a2a_demo_arch.png)

* 前端采用 [mesop](https://github.com/mesop-dev/mesop) Web 框架构建，负责渲染终端用户与"Host Agent"之间的对话内容。当前支持渲染文本内容、思考气泡、网页表单（向Agent请求输入）和图片，更多内容类型即将推出

* [Host Agent](/samples/python/hosts/multiagent/host_agent.py) 是基于 Google ADK 构建的Agent，负责将用户请求分发给 Remote Agents

* 每个 [Remote Agent](/samples/python/hosts/multiagent/remote_agent_connection.py) 都是运行在 Google ADK 环境中的 A2AClient。每个Remote Agent都会获取A2AServer的[AgentCard](https://google.github.io/A2A/#documentation?id=agent-card)，并通过A2A代理所有请求

## 功能特性

<需要快速演示gif>

### 动态添加Agent
点击网页应用中的机器人图标，输入Remote Agent的AgentCard地址，应用将自动获取卡片信息并将该Remote Agent添加到本地已知Agent列表

### 与单个或多个Agent对话
点击聊天按钮开始新对话或继续现有对话。对话请求将首先发送至Host Agent，再由其分发给一个或多个Remote Agent

当Agent返回复杂内容（如图片或网页表单）时，前端会在对话视图中直接渲染这些内容。Remote Agent会负责在A2A格式与Web应用原生格式之间进行内容转换

### 探索A2A任务
点击历史记录可查看Web应用与所有Agent（Host Agent和Remote Agents）之间的消息往来

点击任务列表可查看来自Remote Agents的所有A2A任务更新

## 环境要求

- Python 3.12 或更高版本
- UV 工具
- 支持A2A协议的Agent服务端（[参考示例](/samples/python/agents/README.md)）

## 运行示例

1. 进入demo ui目录: