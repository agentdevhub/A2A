![image info](images/A2A_banner.png)

**_开放协议实现不透明智能体应用间的通信与互操作_**

<!-- TOC -->

- [Agent2Agent Protocol A2A](#agent2agent-protocol-a2a)
    - [快速开始](#快速开始)
    - [参与贡献](#参与贡献)
    - [路线规划](#路线规划)
    - [关于项目](#关于项目)

<!-- /TOC -->

企业AI应用面临的核心挑战，在于如何让不同框架与厂商构建的智能体实现协同工作。为此我们推出开放*Agent间通信协议（A2A）*，为跨生态智能体建立统一通信标准。Google主导这一行业开放协议，因为我们相信该协议将成为**多智能体通信的关键基础设施——无论智能体基于何种框架或厂商构建，都能通过通用语言实现对话**。  
通过*A2A*，智能体可相互展示能力特征，协商用户交互方式（文本、表单或双向音视频），并在安全环境下实现协作。

### **效果演示**

观看演示视频，了解A2A如何实现不同智能体框架间的无缝通信：

<video width="100%" controls>
  <source src="https://storage.googleapis.com/gweb-developer-goog-blog-assets/original_videos/A2A_demo_v4.mp4?X-Goog-Algorithm=GOOG4-RSA-SHA256&X-Goog-Credential=storage-bucket-access%40gweb-developers-gblog-cms.google.com.iam.gserviceaccount.com%2F20250408%2Fauto%2Fstorage%2Fgoog4_request&X-Goog-Date=20250408T174915Z&X-Goog-Expires=86400&X-Goog-SignedHeaders=host&X-Goog-Signature=089d124afdf68c35b97e8042262f686a66681d24b8e21d0586537026faf36598da2ab9ad3bb2d8312e88cba10f443dda33eeb899c500a22b7374a79cf75c4bffd62ab095b45c07dbb4853d796d925123df94bd4b10b36c7bd4dc63aa984784b5a50e2ae7b238457d04b2410682943e2d514c4b530aa82c1a245ee834322f1676a363fa5913a318fe093f7769be17480303aeaee49f7d102ffbad7f9f5ab674386b5b10204d32bc7037d1524617cf21eccb739745a25d6e88cdce7c9fc121923cebbca5d96de0a7014d17953ee7c1c819f3e3ad150ef6d1fbc4730bd8317eb6e5d2c72cb51aebccdc85a2c78b101bc61852b63df6700ba2fed47f10a9ecfa1c16" type="video/mp4">
  您的浏览器不支持视频播放
</video>

### 核心概念

Agent间通信协议（A2A）为独立AI智能体提供通信框架，主要概念包括：

*   **Agent Card（智能体档案）**：位于`/.well-known/agent.json`的公开元数据文件，描述智能体的能力、技能、端点URL及鉴权要求，用于客户端发现
*   **A2A服务端**：实现A2A协议方法（定义于[协议规范](/specification)）的HTTP端点，负责接收请求并管理任务执行
*   **A2A客户端**：使用A2A服务的应用或其他智能体，通过向服务端URL发送请求（如`tasks/send`）实现交互
*   **Task（任务）**：工作执行的核心单元。客户端通过发送消息（`tasks/send`或`tasks/sendSubscribe`）创建任务，任务具有唯一ID并经历状态流转（`submitted`待处理、`working`执行中、`input-required`需输入、`completed`已完成、`failed`失败、`canceled`已取消）
*   **Message（消息）**：客户端（`role: "user"`）与智能体（`role: "agent"`）间的通信单元，包含多个`Part`内容块
*   **Part（内容块）**：消息或产物的基础内容单元，支持`TextPart`文本块、`FilePart`文件块（内联字节或URI）、`DataPart`数据块（结构化JSON如表单）
*   **Artifact（产物）**：任务执行过程中生成的输出（如生成文件、结构化数据），同样由多个`Part`组成
*   **Streaming（流式传输）**：支持`streaming`能力的服务端可使用`tasks/sendSubscribe`处理长任务，客户端通过服务器推送事件（SSE）接收`TaskStatusUpdateEvent`状态更新或`TaskArtifactUpdateEvent`产物更新
*   **Push Notifications（推送通知）**：支持`pushNotifications`的服务端可通过客户端配置的webhook URL（通过`tasks/pushNotification/set`设置）主动推送任务更新

**典型交互流程：**

1.  **发现阶段**：客户端从服务端标准路径获取Agent Card
2.  **初始化阶段**：客户端发送`tasks/send`或`tasks/sendSubscribe`请求，包含初始用户消息及唯一Task ID
3.  **处理阶段**：
    *   **流式模式**：服务端通过SSE事件实时推送任务进展
    *   **同步模式**：服务端同步处理任务并返回最终`Task`对象
4.  **交互阶段（可选）**：若任务进入`input-required`状态，客户端使用相同Task ID通过`tasks/send`或`tasks/sendSubscribe`发送后续消息
5.  **完成阶段**：任务最终进入终止状态（`completed`/`failed`/`canceled`）

### **快速开始**

* 📚 阅读[技术文档](https://a2a.agentdevhub.com/A2A/#/documentation)理解协议能力
* 📝 查看协议结构的[JSON规范](/specification)
* 🎬 使用[示例项目](/samples)体验A2A实战
    * A2A客户端/服务端示例（[Python](/samples/python/common), [JS](/samples/js/src)）
    * [多智能体Web应用](/demo/README.md)
    * CLI工具（[Python](/samples/python/hosts/cli/README.md), [JS](/samples/js/README.md)）
* 🤖 通过[示例智能体](/samples/python/agents/README.md)了解如何将A2A接入不同框架
    * [Agent Developer Kit (ADK)](/samples/python/agents/google_adk/README.md)
    * [CrewAI](/samples/python/agents/crewai/README.md)
    * [LangGraph](/samples/python/agents/langgraph/README.md)
    * [Genkit](/samples/js/src/agents/README.md)
* 📑 查阅专题文档掌握协议细节 
    * [A2A与MCP](https://a2a.agentdevhub.com/A2A/#/topics/a2a_and_mcp.md)
    * [智能体发现](https://a2a.agentdevhub.com/A2A/#/topics/agent_discovery.md)
    * [企业级就绪](https://a2a.agentdevhub.com/A2A/#/topics/enterprise_ready.md)
    * [推送通知](https://a2a.agentdevhub.com/A2A/#/topics/push_notifications.md) 

### **参与贡献**

我们欢迎贡献！请查阅[贡献指南](CONTRIBUTING.md)开始参与。\
有疑问？加入GitHub Discussions参与社区讨论。\
协议改进建议请提交至GitHub Issues。\
如需私密反馈，请填写[此表单](https://docs.google.com/forms/d/e/1FAIpQLScS23OMSKnVFmYeqS2dP7dxY3eTyT7lmtGLUa8OJZfP4RTijQ/viewform)

### **路线规划**

未来计划包含协议改进与示例增强：

**协议增强：**

*   **智能体发现**：
    *   在`AgentCard`中标准化授权方案与可选凭证
*   **智能体协作**：
    *   研究`QuerySkill()`方法用于动态检查未声明的技能
*   **任务生命周期与UX**：
    *   支持任务过程中动态调整交互方式（如中途启用音视频）
*   **客户端方法与传输**：
    *   探索扩展客户端初始化方法（超越任务管理）
    *   提升流式传输可靠性及推送通知机制

**示例与文档增强：**

*   简化"Hello World"示例
*   新增框架集成示例与特性演示
*   完善通用客户端/服务端库文档
*   从JSON Schema生成可读性更强的HTML文档

### **关于项目**

A2A协议是由Google LLC主导的开源项目，遵循[许可协议](LICENSE)，欢迎社区共同参与建设。
