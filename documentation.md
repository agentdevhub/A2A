# Agent2Agent 协议（A2A）

一个实现智能体间互操作的开放协议，弥合**不透明**智能体系统之间的鸿沟。
<img src="images/a2a_actors.png" width="70%" style="margin:20px auto;display:block;">

<!-- TOC -->

- [Agent2Agent Protocol A2A](#agent2agent-protocol-a2a)
  - [反馈与变更](#反馈与变更)
  - [核心原则](#核心原则)
  - [详细讨论](#详细讨论)
  - [概览](#概览)
    - [参与者](#参与者)
    - [传输层](#传输层)
    - [身份验证与授权](#身份验证与授权)
  - [智能体卡片](#智能体卡片)
    - [发现机制](#发现机制)
    - [表示形式](#表示形式)
  - [智能体间通信](#智能体间通信)
  - [核心对象](#核心对象)
    - [任务](#任务)
    - [产物](#产物)
    - [消息](#消息)
    - [内容片段](#内容片段)
    - [推送通知](#推送通知)
- [示例方法与JSON响应](#示例方法与json响应)
  - [智能体卡片](#智能体卡片-1)
  - [发送任务](#发送任务)
  - [获取任务](#获取任务)
  - [取消任务](#取消任务)
  - [设置任务推送通知](#设置任务推送通知)
  - [获取任务推送通知](#获取任务推送通知)
  - [多轮对话](#多轮对话)
  - [流式支持](#流式支持)
    - [重新订阅任务](#重新订阅任务)
  - [非文本媒体](#非文本媒体)
  - [结构化输出](#结构化输出)
  - [错误处理](#错误处理)

<!-- /TOC -->

## 反馈与变更

A2A 是持续演进中的协议，将根据社区反馈进行调整。本仓库包含初始规范、文档和[示例代码](https://github.com/google/A2A/tree/main/samples)。我们将持续更新更多功能、示例、规范和库。当规范和示例达到生产级SDK标准时，将发布1.0版本并保持稳定更新。

## 核心原则

通过A2A，智能体可在不共享记忆、思考过程或工具的情况下为用户完成任务。智能体通过原生模态交换上下文、状态、指令和数据：

- **简洁性**：复用现有标准
- **企业级支持**：身份验证、安全、隐私、追踪、监控
- **异步优先**：支持（超）长时任务和人工介入
- **模态无关**：支持文本、音视频、表单、iframe等
- **执行不透明**：智能体无需共享思考过程、计划或工具

### 详细讨论

- [A2A与MCP](topics/a2a_and_mcp.md?id=a2a-❤%ef%b8%8f-mcp)
- [企业级支持](topics/enterprise_ready.md?id=enterprise-readiness)
- [推送通知](topics/push_notifications.md?id=remote-agent-to-client-updates)
- [智能体发现](topics/agent_discovery.md?id=discovering-agent-cards)

## 概览

### 参与者

A2A协议包含三类参与者：

- **用户**  
  使用智能体系统完成任务的最终用户（人类或服务）
- **客户端**  
  代表用户向不透明智能体发起操作请求的实体（服务/智能体/应用）
- **远端智能体（服务端）**  
  作为A2A服务端的不透明（"黑盒"）智能体

### 传输层

协议使用HTTP作为客户端与远端智能体间的传输层。根据双方能力，可使用SSE支持流式更新。

A2A采用[JSON-RPC 2.0](https://www.jsonrpc.org/specification)作为通信数据交换格式。

### 异步支持

A2A客户端和服务端可使用标准请求/响应模式轮询更新。同时支持通过SSE进行流式更新，以及在断开连接时接收[推送通知](/topics/push_notifications.md?id=remote-agent-to-client-updates)。

### 身份验证与授权

A2A将智能体建模为企业级应用（因其不透明性不共享工具和资源），从而快速实现企业级互操作。

遵循[OpenAPI认证规范](https://swagger.io/docs/specification/v3_0/authentication/)。关键点：A2A协议内不交换身份信息，凭证材料通过HTTP头传输，不在载荷中携带。

服务端需在[智能体卡片](#智能体卡片)中发布认证要求，详细讨论参见[企业级支持](topics/enterprise_ready.md)。

> 注意：若智能体需要额外凭证（如使用特定工具），应返回`Input-Required`状态并携带认证结构。客户端需通过带外方式获取凭证。

## 智能体卡片

支持A2A的远端智能体需发布JSON格式的**智能体卡片**，描述其能力/技能和认证机制。客户端据此选择最佳智能体进行通信。

### 发现机制

推荐托管路径：https://`base url`/.well-known/agent.json。兼容DNS发现机制，也支持私有注册中心（如"智能体目录"）。详见[发现文档](topics/agent_discovery.md?id=discovering-agent-cards)。

### 表示形式

Following is the proposed representation of an Agent Card

```typescript
// An AgentCard conveys key information:
// - Overall details (version, name, description, uses)
// - Skills: A set of capabilities the agent can perform
// - Default modalities/content types supported by the agent.
// - Authentication requirements
interface AgentCard {
  // Human readable name of the agent.
  // (e.g. "Recipe Agent")
  name: string;
  // A human-readable description of the agent. Used to assist users and
  // other agents in understanding what the agent can do.
  // (e.g. "Agent that helps users with recipes and cooking.")
  description: string;
  // A URL to the address the agent is hosted at.
  url: string;
  // The service provider of the agent
  provider?: {
    organization: string;
    url: string;
  };
  // The version of the agent - format is up to the provider. (e.g. "1.0.0")
  version: string;
  // A URL to documentation for the agent.
  documentationUrl?: string;
  // Optional capabilities supported by the agent.
  capabilities: {
    streaming?: boolean; // true if the agent supports SSE
    pushNotifications?: boolean; // true if the agent can notify updates to client
    stateTransitionHistory?: boolean; //true if the agent exposes status change history for tasks
  };
  // Authentication requirements for the agent.
  // Intended to match OpenAPI authentication structure.
  authentication: {
    schemes: string[]; // e.g. Basic, Bearer
    credentials?: string; //credentials a client should use for private cards
  };
  // The set of interaction modes that the agent
  // supports across all skills. This can be overridden per-skill.
  defaultInputModes: string[]; // supported mime types for input
  defaultOutputModes: string[]; // supported mime types for output
  // Skills are a unit of capability that an agent can perform.
  skills: {
    id: string; // unique identifier for the agent's skill
    name: string; //human readable name of the skill
    // description of the skill - will be used by the client or a human
    // as a hint to understand what the skill does.
    description: string;
    // Set of tagwords describing classes of capabilities for this specific
    // skill (e.g. "cooking", "customer support", "billing")
    tags: string[];
    // The set of example scenarios that the skill can perform.
    // Will be used by the client as a hint to understand how the skill can be
    // used. (e.g. "I need a recipe for bread")
    examples?: string[]; // example prompts for tasks
    // The set of interaction modes that the skill supports
    // (if different than the default)
    inputModes?: string[]; // supported mime types for input
    outputModes?: string[]; // supported mime types for output
  }[];
}
```

## Agent-to-Agent Communication

The communication between a Client and a Remote Agent is oriented towards **_task completion_** where agents collaboratively fulfill an end-user’s request. A Task object allows a Client and a Remote Agent to collaborate for completing the submitted task.

A task can be completed by a remote agent immediately or it can be long-running. For long-running tasks, the client may poll the agent for fetching the latest status. Agents can also push notifications to the client via SSE (if connected) or through an external notification service.

## Core Objects

### Task

A Task is a stateful entity that allows Clients and Remote Agents to achieve a specific outcome and generate results. Clients and Remote Agents exchange Messages within a Task. Remote Agents generate results as Artifacts.

A Task is always created by a Client and the status is always determined by the Remote Agent. Multiple Tasks may be part of a common session (denoted by optional sessionId) if required by the client. To do so, the Client sets an optional sessionId when creating the Task.

The agent may:

- fulfill the request immediately
- schedule work for later
- reject the request
- negotiate a different modality
- ask the client for more information
- delegate to other agents and systems

Even after fulfilling the goal, the client can request more information or a change in the context of that same Task. (For example client: "draw a picture of a rabbit", agent: "&lt;picture&gt;", client: "make it red").

Tasks are used to transmit [Artifacts](#artifact) (results) and [Messages](#message) (thoughts, instructions, anything else). Tasks maintain a status and an optional history of status and Messages.

```typescript
interface Task {
  id: string; // unique identifier for the task
  sessionId: string; // client-generated id for the session holding the task.
  status: TaskStatus; // current status of the task
  history?: Message[];
  artifacts?: Artifact[]; // collection of artifacts created by the agent.
  metadata?: Record<string, any>; // extension metadata
}
// TaskState and accompanying message.
interface TaskStatus {
  state: TaskState;
  message?: Message; //additional status updates for client
  timestamp?: string; // ISO datetime value
}
// sent by server during sendSubscribe or subscribe requests
interface TaskStatusUpdateEvent {
  id: string;
  status: TaskStatus;
  final: boolean; //indicates the end of the event stream
  metadata?: Record<string, any>;
}
// sent by server during sendSubscribe or subscribe requests
interface TaskArtifactUpdateEvent {
  id: string;
  artifact: Artifact;
  metadata?: Record<string, any>;
}
// Sent by the client to the agent to create, continue, or restart a task.
interface TaskSendParams {
  id: string;
  sessionId?: string; //server creates a new sessionId for new tasks if not set
  message: Message;
  historyLength?: number; //number of recent messages to be retrieved
  // where the server should send notifications when disconnected.
  pushNotification?: PushNotificationConfig;
  metadata?: Record<string, any>; // extension metadata
}
type TaskState =
  | "submitted"
  | "working"
  | "input-required"
  | "completed"
  | "canceled"
  | "failed"
  | "unknown";
```

### Artifact

Agents generate Artifacts as an end result of a Task. Artifacts are immutable, can be named, and can have multiple parts. A streaming response can append parts to existing Artifacts.

A single Task can generate many Artifacts. For example, "create a webpage" could create separate HTML and image Artifacts.

```typescript
interface Artifact {
  name?: string;
  description?: string;
  parts: Part[];
  metadata?: Record<string, any>;
  index: number;
  append?: boolean;
  lastChunk?: boolean;
}
```

### Message

A Message contains any content that is not an Artifact. This can include things like agent thoughts, user context, instructions, errors, status, or metadata.

All content from a client comes in the form of a Message. Agents send Messages to communicate status or to provide instructions (whereas generated results are sent as Artifacts).

A Message can have multiple parts to denote different pieces of content. For example, a user request could include a textual description from a user and then multiple files used as context from the client.

```typescript
interface Message {
  role: "user" | "agent";
  parts: Part[];
  metadata?: Record<string, any>;
}
```

### Part

A fully formed piece of content exchanged between a client and a remote agent as part of a Message or an Artifact. Each Part has its own content type and metadata.

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
    // oneof {
    bytes?: string; //base64 encoded content
    uri?: string;
    //}
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

### Push Notifications

A2A supports a secure notification mechanism whereby an agent can notify a client of an update outside of a connected session via a PushNotificationService. Within and across enterprises, it is critical that the agent verifies the identity of the notification service, authenticates itself with the service, and presents an identifier that ties the notification to the executing Task.

The target server of the PushNotificationService should be considered a separate service, and is not guaranteed (or even expected) to be the client directly. This PushNotificationService is responsible for authenticating and authorizing the agent and for proxying the verified notification to the appropriate endpoint (which could be anything from a pub/sub queue, to an email inbox or other service, etc).

For contrived scenarios with isolated client-agent pairs (e.g. local service mesh in a contained VPC, etc.) or isolated environments without enterprise security concerns, the client may choose to simply open a port and act as its own PushNotificationService. Any enterprise implementation will likely have a centralized service that authenticates the remote agents with trusted notification credentials and can handle online/offline scenarios. (This should be thought of similarly to a mobile Push Notification Service).

```typescript
interface PushNotificationConfig {
  url: string;
  token?: string; // token unique to this task/session
  authentication?: {
    schemes: string[];
    credentials?: string;
  };
}
interface TaskPushNotificationConfig {
  id: string; //task id
  pushNotificationConfig: PushNotificationConfig;
}
```

# Sample Methods and JSON Responses

## Agent Card

```json
//agent card
{
  "name": "Google Maps Agent",
  "description": "Plan routes, remember places, and generate directions",
  "url": "https://maps-agent.google.com",
  "provider": {
    "organization": "Google",
    "url": "https://google.com"
  },
  "version": "1.0.0",
  "authentication": {
    "schemes": "OAuth2"
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
      "name": "Route planning",
      "description": "Helps plan routing between two locations",
      "tags": ["maps", "routing", "navigation"],
      "examples": [
        "plan my route from Sunnyvale to Mountain View",
        "what's the commute time from Sunnyvale to San Francisco at 9AM",
        "create turn by turn directions from Sunnyvale to Mountain View"
      ],
      // can return a video of the route
      "outputModes": ["application/html", "video/mp4"]
    },
    {
      "id": "custom-map",
      "name": "My Map",
      "description": "Manage a custom map with your own saved places",
      "tags": ["custom-map", "saved-places"],
      "examples": [
        "show me my favorite restaurants on the map",
        "create a visual of all places I've visited in the past year"
      ],
      "outputModes": ["application/html"]
    }
  ]
}
```

## Send a Task

Allows a client to send content to a remote agent to start a new Task, resume an interrupted Task or reopen a completed Task. A Task interrupt may be caused due to an agent requiring additional user input or a runtime error.

```json
//Request
{
  "jsonrpc": "2.0",
  "id": 1,
  "method":"tasks/send",
  "params": {
    "id": "de38c76d-d54c-436c-8b9f-4c2703648d64",
    "message": {
      "role":"user",
      "parts": [{
        "type":"text",
        "text": "tell me a joke"
      }]
    },
    "metadata": {}
  }
}
//Response
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": {
    "id": "de38c76d-d54c-436c-8b9f-4c2703648d64",
    "sessionId": "c295ea44-7543-4f78-b524-7a38915ad6e4",
    "status": {
      "state": "completed",
    },
    "artifacts": [{
      "name":"joke",
      "parts": [{
          "type":"text",
          "text":"Why did the chicken cross the road? To get to the other side!"
        }]
      }],
    "metadata": {}
  }
}
```

## Get a Task

Clients may use this method to retrieve the generated Artifacts for a Task. The agent determines the retention window for Tasks previously submitted to it. An agent may return an error code for Tasks that were past the retention window for an agent or for Tasks that are short-lived and not persisted by the agent.

The client may also request the last N items of history of the Task which will include all Messages, in order, sent by client and server. By default this is 0 (no history).

```json
//Request
{
  "jsonrpc": "2.0",
  "id": 1,
  "method":"tasks/get",
  "params": {
    "id": "de38c76d-d54c-436c-8b9f-4c2703648d64",
    "historyLength": 10,
    "metadata": {}
  }
}
//Response
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": {
    "id": "de38c76d-d54c-436c-8b9f-4c2703648d64",
    "sessionId": "c295ea44-7543-4f78-b524-7a38915ad6e4",
    "status": {
      "state": "completed"
    },
    "artifacts": [{
      "parts": [{
        "type":"text",
        "text":"Why did the chicken cross the road? To get to the other side!"
      }]
    }],
    "history":[
      {
        "role": "user",
        "parts": [
          {
            "type": "text",
            "text": "tell me a joke"
          }
        ]
      }
    ],
    "metadata": {}
  }
}
```

## Cancel a Task

A client may choose to cancel previously submitted Tasks as shown below.

```json
//Request
{
  "jsonrpc": "2.0",
  "id": 1,
  "method":"tasks/cancel",
  "params": {
    "id": "de38c76d-d54c-436c-8b9f-4c2703648d64",
    "metadata": {}
  }
}
//Response
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": {
    "id": 1,
    "sessionId": "c295ea44-7543-4f78-b524-7a38915ad6e4",
    "status": {
      "state": "canceled"
    },
    "metadata": {}
  }
}
```

## Set Task Push Notifications

Clients may configure a push notification URL for receiving an update on Task status change.

```json
//Request
{
  "jsonrpc": "2.0",
  "id": 1,
  "method":"tasks/pushNotification/set",
  "params": {
    "id": "de38c76d-d54c-436c-8b9f-4c2703648d64",
    "pushNotificationConfig": {
      "url": "https://example.com/callback",
      "authentication": {
        "schemes": ["jwt"]
      }
    }
  }
}
//Response
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": {
    "id": "de38c76d-d54c-436c-8b9f-4c2703648d64",
    "pushNotificationConfig": {
      "url": "https://example.com/callback",
      "authentication": {
        "schemes": ["jwt"]
      }
    }
  }
}
```

## Get Task Push Notifications

Clients may retrieve the currently configured push notification configuration for a Task using this method.

```json
//Request
{
  "jsonrpc": "2.0",
  "id": 1,
  "method":"tasks/pushNotification/get",
  "params": {
    "id": "de38c76d-d54c-436c-8b9f-4c2703648d64"
  }
}
//Response
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": {
    "id": "de38c76d-d54c-436c-8b9f-4c2703648d64",
    "pushNotificationConfig": {
      "url": "https://example.com/callback",
      "authentication": {
        "schemes": ["jwt"]
      }
    }
  }
}
```

## Multi-turn Conversations

A Task may pause to be executed on the remote agent if it requires additional user input. When a Task is in `input-required` state, the client is required to provide additional input for the Task to resume processing on the remote agent.

The Message included in the `input-required` state must include the details indicating what the client must do. For example "fill out a form" or "log into SaaS service foo". If this includes structured data, the instruction should be sent as one `Part` and the structured data as a second `Part`.

```json
//Request - seq 1
{
  "jsonrpc": "2.0",
  "id": 1,
  "method":"tasks/send",
  "params": {
    "id": "de38c76d-d54c-436c-8b9f-4c2703648d64",
    "message": {
      "role":"user",
      "parts": [{
        "type":"text",
        "text": "request a new phone for me"
      }]
    },
    "metadata": {}
  }
}
//Response - seq 2
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": {
    "id": "de38c76d-d54c-436c-8b9f-4c2703648d64",
    "sessionId": "c295ea44-7543-4f78-b524-7a38915ad6e4",
    "status": {
      "state": "input-required",
      "message": {
        "parts": [{
          "type":"text",
          "text":"Select a phone type (iPhone/Android)"
        }]
      }
    },
    "metadata": {}
  }
}
//Request - seq 3
{
  "jsonrpc": "2.0",
  "id": 2,
  "method":"tasks/send",
  "params": {
    "id": "de38c76d-d54c-436c-8b9f-4c2703648d64",
    "sessionId": "c295ea44-7543-4f78-b524-7a38915ad6e4",
    "message": {
      "role":"user",
      "parts": [{
        "type":"text",
        "text": "Android"
      }]
    },
    "metadata": {}
  }
}
//Response - seq 4
{
  "jsonrpc": "2.0",
  "id": 2,
  "result": {
    "id": 1,
    "sessionId": "c295ea44-7543-4f78-b524-7a38915ad6e4",
    "status": {
      "state": "completed"
    },
    "artifacts": [{
      "name": "order-confirmation",
      "parts": [{
          "type":"text",
          "text":"I have ordered a new Android device for you. Your request number is R12443"
        }],
      "metadata": {}
    }],
    "metadata": {}
  }
}
```

## Streaming Support

For clients and remote agents capable of communicating over HTTP with SSE, clients can send the RPC request with method `tasks/sendSubscribe` when creating a new Task. The remote agent can respond with a stream of TaskStatusUpdateEvents (to communicate status changes or instructions/requests) and TaskArtifactUpdateEvents (to stream generated results).
Note that TaskArtifactUpdateEvents can append new parts to existing Artifacts. Clients
can use `task/get` to retrieve the entire Artifact outside of the streaming.
Agents must set final: true attribute at the end of the stream or if the agent is interrupted and require additional user input.

```json
//Request
{
  "method":"tasks/sendSubscribe",
  "params": {
    "id": "de38c76d-d54c-436c-8b9f-4c2703648d64",
    "sessionId": "c295ea44-7543-4f78-b524-7a38915ad6e4",
    "message": {
      "role":"user",
      "parts": [{
        "type":"text",
        "text": "write a long paper describing the attached pictures"
      },{
        "type":"file",
        "file": {
           "mimeType": "image/png",
           "data":"<base64-encoded-content>"
        }
      }]
    },
    "metadata": {}
  }
}

//Response
data: {
  "jsonrpc": "2.0",
  "id": 1,
  "result": {
    "id": 1,
    "status": {
      "state": "working",
      "timestamp":"2025-04-02T16:59:25.331844"
    },
    "final": false
  }
}

data: {
  "jsonrpc": "2.0",
  "id": 1,
  "result": {
    "id": 1,    
    "artifact": [
      "parts": [
        {"type":"text", "text": "<section 1...>"}
      ],
      "index": 0,
      "append": false,      
      "lastChunk": false
    ]
  }
}
data: {
  "jsonrpc": "2.0",
  "id": 1,
  "result": {
    "id": 1,  
    "artifact": [
      "parts": [
        {"type":"text", "text": "<section 2...>"}
      ],
      "index": 0,
      "append": true,      
      "lastChunk": false
    ]
  }
}
data: {
  "jsonrpc": "2.0",
  "id": 1,
  "result": {
    "id": 1,    
    "artifact": [
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

### Resubscribe to Task

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

## Non-textual Media

Following is an example interaction between a client and an agent with non-textual data.

```json
//Request - seq 1
{
  "jsonrpc": "2.0",
  "id": 9,
  "method":"tasks/send",
  "params": {
    "id": "de38c76d-d54c-436c-8b9f-4c2703648d64",
    "sessionId": "c295ea44-7543-4f78-b524-7a38915ad6e4",
    "message": {
      "role":"user",
      "parts": [{
        "type":"text",
        "text": "Analyze the attached report and generate high level overview"
      },{
        "type":"file",
        "file": {
           "mimeType": "application/pdf",
           "data":"<base64-encoded-content>"
        }
      }]
    },
    "metadata": {}
  }
}
//Response - seq 2
{
  "jsonrpc": "2.0",
  "id": 9,
  "result": {
    "id": "de38c76d-d54c-436c-8b9f-4c2703648d64",
    "sessionId": "c295ea44-7543-4f78-b524-7a38915ad6e4",
    "status": {
      "state": "working",
      "message": {
        "role": "agent",
        "parts": [{
          "type":"text",
          "text":"analysis in progress, please wait"
        }],
        "metadata": {}
       }
     },
    "metadata": {}
  }
}
//Request - seq 3
{
  "jsonrpc": "2.0",
  "id": 10,
  "method":"tasks/get",
  "params": {
    "id": "de38c76d-d54c-436c-8b9f-4c2703648d64",
    "metadata": {}
  }
}
//Response - seq 4
{
  "jsonrpc": "2.0",
  "id": 9,
  "result": {
    "id": "de38c76d-d54c-436c-8b9f-4c2703648d64",
    "sessionId": "c295ea44-7543-4f78-b524-7a38915ad6e4",
    "status": {
      "state": "completed"
     },
    "artifacts": [{
      "parts": [{
        "type":"text",
        "text":"<generated analysis content>"
       }],
       "metadata": {}
     }],
    "metadata": {}
  }
}
```

## Structured output

Both the client or the agent can request structured output from the other party.

```json
//Request
{
  "jsonrpc": "2.0",
  "id": 9,
  "method":"tasks/send",
  "params": {
    "id": "de38c76d-d54c-436c-8b9f-4c2703648d64",
    "sessionId": "c295ea44-7543-4f78-b524-7a38915ad6e4",
    "message": {
      "role":"user",
      "parts": [{
        "type":"text",
        "text": "Show me a list of my open IT tickets",
        "metadata": {
          "mimeType": "application/json",
          "schema": {
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "ticketNumber": { "type": "string" },
                "description": { "type": "string" }
              }
            }
          }
        }
      }]
    },
    "metadata": {}
  }
}
//Response
{
  "jsonrpc": "2.0",
  "id": 9,
  "result": {
    "id": "de38c76d-d54c-436c-8b9f-4c2703648d64",
    "sessionId": "c295ea44-7543-4f78-b524-7a38915ad6e4",
    "status": {
      "state": "working",
      "message": {
        "role": "agent",
        "parts": [{
            "type":"text",
            "text":"[{\"ticketNumber\":\"REQ12312\",\"description\":\"request for VPN access\"},{\"ticketNumber\":\"REQ23422\",\"description\":\"Add to DL - team-gcp-onboarding\"}]"
        }],
        "metadata": {}
      }
    },
    "metadata": {}
  }
}
```

## Error Handling

Following is the ErrorMessage format for the server to respond to the client when it encounters an error processing the client request.

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
