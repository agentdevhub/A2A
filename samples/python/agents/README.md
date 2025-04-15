## 示例智能体

本目录下的所有智能体均为基于不同框架构建的示例，展示了不同的技术能力。每个智能体均可作为独立的 A2A 服务器运行。

每个智能体均可按照其 README 中的说明作为独立的 A2A 服务器运行。默认情况下，各智能体将在本地主机的不同端口上运行（可通过命令行参数覆盖默认设置）。

要与此类服务器交互，请在宿主应用（如 CLI）中使用 A2AClient。详见[宿主应用](/samples/python/hosts/README.md)。

* [**Google ADK**](/samples/python/agents/google_adk/README.md)  
用于（模拟）填写费用报销单的示例智能体。展示了多轮交互能力以及通过 A2A 返回/回复网页表单的功能。

* [**LangGraph**](/samples/python/agents/langgraph/README.md)  
具备货币转换能力的示例智能体。展示了多轮交互、工具调用和流式更新功能。

* [**CrewAI**](/samples/python/agents/crewai/README.md)  
支持图像生成的示例智能体。展示了多轮交互能力以及通过 A2A 发送图像的功能。