# 基于A2A协议的LangGraph货币转换智能体

本示例演示了如何使用[LangGraph](https://langchain-ai.github.io/langgraph/)构建货币转换智能体并通过A2A协议进行交互。该实现支持多轮对话和流式响应功能。

## 工作原理

本智能体采用LangGraph结合Google Gemini，通过ReAct智能体模式提供货币汇率查询服务。A2A协议实现了标准化交互，允许客户端发送请求并接收实时更新。