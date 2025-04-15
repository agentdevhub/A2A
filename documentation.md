# Agent2Agent 协议 (A2A)

开放协议，实现代理间互操作，弥合**不透明**代理系统间的鸿沟。
<img src="images/a2a_actors.png" width="70%" style="margin:20px auto;display:block;">

<!-- TOC -->

- [Agent2Agent Protocol A2A](#agent2agent-protocol-a2a)
  - [反馈与变更](#反馈与变更)
  - [核心原则](#核心原则)
  - [详细讨论](#详细讨论)
  - [概述](#概述)
    - [参与者](#参与者)
    - [传输协议](#传输协议)
    - [认证与授权](#认证与授权)
  - [Agent Card](#agent-card)
    - [发现机制](#发现机制)
    - [数据表示](#数据表示)
  - [代理间通信](#代理间通信)
  - [核心对象](#核心对象)
    - [Task](#task)
    - [Artifact](#artifact)
    - [Message](#message)
    - [Part](#part)
    - [推送通知](#推送通知)
- [示例方法与JSON响应](#示例方法与json响应)
  - [Agent Card](#agent-card)
  - [发送任务](#发送任务)
  - [获取任务](#获取任务)
  - [取消任务](#取消任务)
  - [设置任务推送通知](#设置任务推送通知)
  - [获取任务推送配置](#获取任务推送配置)
  - [多轮对话](#多轮对话)
  - [流式支持](#流式支持)
    - [重新订阅任务](#重新订阅任务)
  - [非文本媒体](#非文本媒体)
  - [结构化输出](#结构化输出)
  - [错误处理](#错误处理)

<!-- /TOC -->

## 反馈与变更

A2A是持续演进的项目，将根据社区反馈调整。本仓库包含初始规范、文档和[示例代码](https://github.com/google/A2A/tree/main/samples)。我们将持续更新更多特性、示例和库。当规范成熟为生产级SDK时将发布1.0版本。

## 核心原则

A2A代理通过交换上下文、状态、指令和数据（而非内存、思维或工具）完成任务：

- **简单性**：复用现有标准
- **企业级就绪**：认证、安全、隐私、追踪、监控
- **异步优先**：支持长时任务与人机协同
- **多模态支持**：文本、音视频、表单等
- **执行不透明**：代理无需共享内部逻辑

### 详细讨论

- [A2A与MCP](topics/a2a_and_mcp.md?id=a2a-❤%ef%b8%8f-mcp)
- [企业级就绪](topics/enterprise_ready.md?id=enterprise-readiness)
- [推送通知](topics/push_notifications.md?id=remote-agent-to-client-updates)
- [代理发现](topics/agent_discovery.md?id=discovering-agent-cards)

## 概述

### 参与者

协议包含三类角色：

- **用户**  
  使用代理系统完成任务的自然人或服务
- **客户端**  
  代表用户请求代理执行操作的实体
- **远程代理（服务端）**  
  提供服务的黑盒代理

### 传输协议

基于HTTP通信，支持SSE流式更新。采用[JSON-RPC 2.0](https://www.jsonrpc.org/specification)作为数据交换格式。

### 异步支持

支持标准请求/响应模式与轮询机制，同时提供SSE流式更新和断线推送通知。

### 认证与授权

遵循[OpenAPI认证规范](https://swagger.io/docs/specification/v3_0/authentication/)，通过HTTP头传递凭证材料。代理需在[Agent Card](#agent-card)中声明认证要求。

> 注意：若任务执行中需要额外凭证（如访问特定工具），代理应返回`input-required`状态并通过Authentication结构说明要求。

## Agent Card

### 发现机制

推荐代理在`/.well-known/agent.json`路径发布Agent Card。支持DNS发现和私有注册表（如Agent Catalog）。

### 数据表示

```typescript
interface AgentCard {
  name: string;                    // 可读名称（如"菜谱助手"）
  description: string;             // 功能描述
  url: string;                     // 服务端点
  provider?: {                     // 供应商信息
    organization: string;
    url: string;
  };
  version: string;                 // 版本号
  documentationUrl?: string;       // 文档链接
  capabilities: {                  // 支持能力
    streaming?: boolean;           // SSE支持
    pushNotifications?: boolean;   // 推送通知支持
    stateTransitionHistory?: boolean; // 状态历史记录
  };
  authentication: {                // 认证要求
    schemes: string[];             // 认证方案（如OAuth2）
    credentials?: string;          // 私有凭证
  };
  defaultInputModes: string[];     // 默认输入类型
  defaultOutputModes: string[];    // 默认输出类型
  skills: {                        // 技能列表
    id: string;                    // 技能ID
    name: string;                  // 技能名称
    description: string;           // 技能描述
    tags: string[];                // 标签（如"烹饪"）
    examples?: string[];           // 使用示例
    inputModes?: string[];         // 技能专用输入类型
    outputModes?: string[];        // 技能专用输出类型
  }[];
}
```

## 代理间通信

围绕**任务完成**展开，通过Task对象实现协作。任务可能立即完成或长期运行，客户端可通过轮询或推送获取更新。

## 核心对象

### Task

```typescript
interface Task {
  id: string;                     // 任务唯一标识
  sessionId?: string;             // 会话ID
  status: TaskStatus;             // 当前状态
  history?: Message[];            // 消息历史
  artifacts?: Artifact[];         // 输出工件
  metadata?: Record<string, any>; // 扩展元数据
}

interface TaskStatus {
  state: TaskState;               // 状态枚举
  message?: Message;              // 状态关联消息
  timestamp?: string;             // ISO时间戳
}

type TaskState = 
  | "submitted"                   // 已提交
  | "working"                     // 处理中
  | "input-required"              // 需输入
  | "completed"                   // 已完成
  | "canceled"                    // 已取消
  | "failed"                      // 失败
  | "unknown";                    // 未知
```

### Artifact

```typescript
interface Artifact {
  name?: string;                  // 工件名称
  description?: string;           // 描述
  parts: Part[];                  // 内容部件
  metadata?: Record<string, any>; // 元数据
  index: number;                  // 索引号
  append?: boolean;               // 是否追加内容
  lastChunk?: boolean;            // 末位标识
}
```

### Message

```typescript
interface Message {
  role: "user" | "agent";         // 发送方角色
  parts: Part[];                  // 内容部件
  metadata?: Record<string, any>; // 元数据
}
```

### Part

```typescript
interface TextPart {
  type: "text";
  text: string;
}

interface FilePart {
  type: "file";
  file: {
    name?: string;
    mimeType?: string;
    bytes?: string;  // base64内容
    uri?: string;    // 资源地址
  };
}

interface DataPart {
  type: "data";
  data: Record<string, any>;
}

type Part = (TextPart | FilePart | DataPart) & {
  metadata: Record<string, any>;
};
```

### 推送通知

```typescript
interface PushNotificationConfig {
  url: string;                    // 回调地址
  token?: string;                 // 任务专属令牌
  authentication?: {              // 认证配置
    schemes: string[];
    credentials?: string;
  };
}

interface TaskPushNotificationConfig {
  id: string;                     // 任务ID
  pushNotificationConfig: PushNotificationConfig;
}
```

# 示例方法与JSON响应

## Agent Card

```json
{
  "name": "Google Maps Agent",
  "description": "路线规划与导航助手",
  "url": "https://maps-agent.google.com",
  "provider": {
    "organization": "Google",
    "url": "https://google.com"
  },
  "version": "1.0.0",
  "authentication": {
    "schemes": ["OAuth2"]
  },
  "defaultInputModes": ["text/plain"],
  "defaultOutputModes": ["text/plain", "application/html"],
  "capabilities": {
    "streaming": true,
    "pushNotifications": false
  },
  "skills": [
    {
      "id": "route-planner",
      "name": "路线规划",
      "description": "两点间路线规划",
      "tags": ["地图", "导航"],
      "outputModes": ["application/html", "video/mp4"]
    }
  ]
}
```

## 发送任务

```json
// 请求
{
  "jsonrpc": "2.0",
  "id": 1,
  "method":"tasks/send",
  "params": {
    "id": "de38c76d-d54c-436c-8b9f-4c2703648d64",
    "message": {
      "role":"user",
      "parts": [{"type":"text","text": "讲个笑话"}]
    }
  }
}

// 响应
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": {
    "id": "de38c76d-d54c-436c-8b9f-4c2703648d64",
    "status": {"state": "completed"},
    "artifacts": [{
      "parts": [{"type":"text","text":"为什么鸡过马路？去对面！"}]
    }]
  }
}
```

## 获取任务

```json
// 请求
{
  "jsonrpc": "2.0",
  "id": 1,
  "method":"tasks/get",
  "params": {"id": "de38c76d-d54c-436c-8b9f-4c2703648d64"}
}

// 响应
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": {
    "id": "de38c76d-d54c-436c-8b9f-4c2703648d64",
    "status": {"state": "completed"},
    "artifacts": [{
      "parts": [{"type":"text","text":"为什么鸡过马路？去对面！"}]
    }]
  }
}
```

## 取消任务

```json
// 请求
{
  "jsonrpc": "2.0",
  "id": 1,
  "method":"tasks/cancel",
  "params": {"id": "de38c76d-d54c-436c-8b9f-4c2703648d64"}
}

// 响应
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": {
    "id": "de38c76d-d54c-436c-8b9f-4c2703648d64",
    "status": {"state": "canceled"}
  }
}
```

## 设置任务推送通知

```json
// 请求
{
  "jsonrpc": "2.0",
  "id": 1,
  "method":"tasks/pushNotification/set",
  "params": {
    "id": "de38c76d-d54c-436c-8b9f-4c2703648d64",
    "pushNotificationConfig": {
      "url": "https://example.com/callback",
      "authentication": {"schemes": ["jwt"]}
    }
  }
}

// 响应
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": {
    "pushNotificationConfig": {
      "url": "https://example.com/callback",
      "authentication": {"schemes": ["jwt"]}
    }
  }
}
```

## 多轮对话

```json
// 请求1
{
  "method":"tasks/send",
  "params": {
    "message": {
      "parts": [{"type":"text","text": "申请新手机"}]
    }
  }
}

// 响应1
{
  "result": {
    "status": {
      "state": "input-required",
      "message": {"parts": [{"type":"text","text":"选择手机类型(iPhone/Android)"}]}
    }
  }
}

// 请求2
{
  "method":"tasks/send",
  "params": {
    "message": {"parts": [{"type":"text","text": "Android"}]}
  }
}

// 响应2
{
  "result": {
    "status": {"state": "completed"},
    "artifacts": [{
      "parts": [{"type":"text","text":"已为您订购Android设备，订单号R12443"}]
    }]
  }
}
```

## 流式支持

```json
// 请求
{
  "method":"tasks/sendSubscribe",
  "params": {
    "message": {
      "parts": [
        {"type":"text","text": "撰写长论文"},
        {"type":"file","file": {/*...*/}}
      ]
    }
  }
}

// 流式响应
data: {"result": {"status": {"state": "working"}}}
data: {"result": {"artifact": {"parts": [{"text":"<章节1...>"}]}}}
data: {"result": {"artifact": {"parts": [{"text":"<章节2...>"], "append":true}}}
data: {"result": {"status": {"state": "completed"}, "final": true}}
```

### 重新订阅任务

A disconnected client may resubscribe to a remote agent that supports streaming to receive Task updates via SSE.

```json
//Request
{
  "method":"tasks/resubscribe",
  "params": {
    "id": "de38c76d-d54c-436c-8b9f-4c2703648d64",
    "metadata": {}
  }
}
//Response
data: {
  "jsonrpc": "2.0",
  "id": 1,
  "result": {
    "id": "de38c76d-d54c-436c-8b9f-4c2703648d64",
    "artifact":[
      "parts": [
        {"type":"text", "text": "<section 2...>"}
      ],
      "index": 0,
      "append": true,
      "lastChunk":false
    ]
  }
}
data: {
  "jsonrpc": "2.0",
  "id": 1,
  "result": {
    "id": "de38c76d-d54c-436c-8b9f-4c2703648d64",
    "artifact":[
      "parts": [
        {"type":"text", "text": "<section 3...>"}
      ],
      "index": 0,
      "append": true,
      "lastChunk": true
    ]   
  }
}

data: {
  "jsonrpc": "2.0",
  "id": 1,
  "result": {
    "id": 1,
    "status": {
      "state": "completed",
      "timestamp":"2025-04-02T16:59:35.331844"
    },
    "final": true
  }
}
```

## 非文本媒体

```json
// 请求
{
  "method":"tasks/send",
  "params": {
    "message": {
      "parts": [
        {"type":"text","text": "分析报告"},
        {"type":"file","file": {"mimeType":"application/pdf"}}
      ]
    }
  }
}

// 响应
{
  "result": {
    "status": {"state": "working"},
    "artifacts": [{"parts": [{"type":"text","text":"<分析结果>"}]}]
  }
}
```

## 结构化输出

```json
// 请求
{
  "method":"tasks/send",
  "params": {
    "message": {
      "parts": [{
        "type":"text",
        "text": "显示未解决IT工单",
        "metadata": {
          "mimeType": "application/json",
          "schema": {/*...*/}
        }
      }]
    }
  }
}

// 响应
{
  "result": {
    "message": {
      "parts": [{"text":"[{\"ticketNumber\":\"REQ12312\",...}]"}]
    }
  }
}
```

## 错误处理

| 错误码 | 描述                 |
|--------|----------------------|
| -32700 | JSON解析错误         |
| -32600 | 无效请求             |
| -32601 | 方法不存在           |
| -32001 | 任务不存在           |
| -32005 | 内容类型不兼容       |

```typescript
interface ErrorMessage {
  code: number;
  message: string;
  data?: any;
}
```

The following are the standard JSON-RPC error codes that the server can respond with for error scenarios:

| Error Code         | Message          | Description                                      |
| :----------------- | :--------------- | :----------------------------------------------- |
| \-32700            | JSON parse error | Invalid JSON was sent                            |
| \-32600            | Invalid Request  | Request payload validation error                 |
| \-32601            | Method not found | Not a valid method                               |
| \-32602            | Invalid params   | Invalid method parameters                        |
| \-32603            | Internal error   | Internal JSON-RPC error                          |
| \-32000 to \-32099 | Server error     | Reserved for implementation specific error codes |
| \-32001            | Task not found   | Task not found with the provided id              |
| \-32002            | Task cannot be canceled  | Task cannot be canceled by the remote agent|
| \-32003            | Push notifications not supported | Push Notification is not supported by the agent|
| \-32004            | Unsupported operation   | Operation is not supported                        |
| \-32005            | Incompatible content types   | Incompatible content types between client and an agent  |