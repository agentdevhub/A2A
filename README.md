![image info](images/A2A_banner.png) 


**_一个开放协议，实现不透明智能体应用之间的通信与互操作。_** 


<!-- TOC --> 


- [Agent2Agent Protocol A2A](#agent2agent-protocol-a2a)
  - [快速入门](#快速入门)
  - [贡献指南](#贡献指南)
  - [未来计划](#未来计划)
  - [关于项目](#关于项目)


<!-- /TOC --> 


企业采用AI面临的最大挑战之一是实现不同框架和供应商构建的智能体协同工作。为此我们创建了开放的*Agent2Agent（A2A）协议*，这是一种促进跨生态系统智能体通信的协作方案。Google主导这个行业级开放协议倡议，因为我们坚信该协议**通过为智能体提供通用语言——无论其构建框架或供应商——将成为多智能体通信的关键支撑**。

借助*A2A*，智能体可以相互展示能力、协商与用户的交互方式（通过文本、表单或双向音视频），同时确保安全协作。

### **实战演示** 
观看[演示视频](https://storage.googleapis.com/gweb-developer-goog-blog-assets/original_videos/A2A_demo_v4.mp4)了解A2A如何实现不同智能体框架的无缝通信。

### 核心概念
Agent2Agent（A2A）协议促进独立AI智能体间的通信，核心概念如下：

* **Agent Card（智能体名片）：** 位于`/.well-known/agent.json`的公共元数据文件，描述智能体的能力、技能、端点URL和认证要求。客户端通过此文件进行服务发现。
* **A2A Server（服务端）：** 实现A2A协议方法（定义于[JSON规范](/specification)）的HTTP端点。负责接收请求并管理任务执行。
* **A2A Client（客户端）：** 使用A2A服务的应用或其他智能体。通过`tasks/send`等请求与A2A服务端交互。
* **Task（任务）：** 任务是最小工作单元。客户端通过发送消息（`tasks/send`或`tasks/sendSubscribe`）创建任务。每个任务有唯一ID，经历`submitted`（已提交）、`working`（执行中）、`input-required`（需输入）、`completed`（已完成）、`failed`（失败）、`canceled`（取消）等状态。
* **Message（消息）：** 表示客户端（`role: "user"`）与智能体（`role: "agent"`）之间的交互轮次。消息由多个Part组成。
* **Part（内容块）：** 消息或产物的基本内容单元，包含`TextPart`（文本）、`FilePart`（文件，支持内联字节或URI）或`DataPart`（结构化JSON数据，如表单）。
* **Artifact（产物）：** 任务执行过程中生成的结果（如生成的文件、结构化数据），同样由Part构成。
* **Streaming（流式通信）：** 针对长任务，支持`streaming`能力的服务端可使用`tasks/sendSubscribe`。客户端通过Server-Sent Events（SSE）接收`TaskStatusUpdateEvent`或`TaskArtifactUpdateEvent`事件，实时获取进度。
* **Push Notifications（推送通知）：** 支持`pushNotifications`的服务端可通过`tasks/pushNotification/set`配置客户端提供的webhook URL，主动推送任务更新。

### **典型工作流**
1. **服务发现：** 客户端从服务端的well-known URL获取Agent Card
2. **任务启动：** 客户端发送包含初始消息和唯一Task ID的`tasks/send`或`tasks/sendSubscribe`请求
3. **任务处理：**
   * **（流式模式）：** 服务端通过SSE推送状态更新和产物
   * **（同步模式）：** 服务端同步处理任务并返回最终`Task`对象
4. **交互（可选）：** 若任务进入`input-required`状态，客户端使用相同Task ID继续发送消息
5. **任务完成：** 任务最终进入终止状态（`completed`/`failed`/`canceled`）

### **快速入门**
* 📚 阅读[技术文档](https://google.github.io/A2A/#/documentation)了解协议能力
* 📝 查看协议的[JSON规范](/specification)
* 🎬 使用[示例代码](/samples)体验A2A
   * A2A客户端/服务端示例（[Python](/samples/python/common)、[JS](/samples/js/src)）
   * [多智能体Web应用](/demo/README.md)
   * 命令行工具（[Python](/samples/python/hosts/cli/README.md)、[JS](/samples/js/README.md)）
* 🤖 通过[示例智能体](/samples/python/agents/README.md)学习如何接入不同框架
   * [Agent Developer Kit (ADK)](/samples/python/agents/google_adk/README.md)
   * [CrewAI](/samples/python/agents/crewai/README.md)
   * [LangGraph](/samples/python/agents/langgraph/README.md)
   * [Genkit](/samples/js/src/agents/README.md)
* 📑 查阅关键主题
   * [A2A与MCP](https://google.github.io/A2A/#/topics/a2a_and_mcp.md)
   * [智能体发现机制](https://google.github.io/A2A/#/topics/agent_discovery.md)
   * [企业级支持](https://google.github.io/A2A/#/topics/enterprise_ready.md)
   * [推送通知详解](https://google.github.io/A2A/#/topics/push_notifications.md)

### **贡献指南**
欢迎贡献！请阅读[贡献指南](CONTRIBUTING.md)开始参与。\
有疑问？加入[GitHub讨论区](https://github.com/google/A2A/discussions/)。\
协议改进建议请提交至[GitHub Issues](https://github.com/google/A2A/issues)。\
私有反馈可通过[Google表单](https://docs.google.com/forms/d/e/1FAIpQLScS23OMSKnVFmYeqS2dP7dxY3eTyT7lmtGLUa8OJZfP4RTijQ/viewform)提交

### **未来计划**
协议改进方向与示例增强计划：

**协议增强：**
* **智能体发现：**
   * 在`AgentCard`中规范化授权方案和可选凭证
* **智能体协作：**
   * 研究`QuerySkill()`方法用于动态检查未声明技能
* **任务生命周期与UX：**
   * 支持任务中动态UX协商（如中途启用音视频）
* **客户端方法与传输：**
   * 扩展客户端发起的方法支持
   * 提升流式通信可靠性和推送通知机制

**示例与文档：**
* 简化"Hello World"示例
* 增加框架集成示例和特性演示
* 完善客户端/服务端通用库文档
* 从JSON Schema生成可读文档

### **关于项目**
A2A协议是由Google LLC运营的开源项目，遵循[许可协议](LICENSE)，欢迎社区共同贡献。
