# A2A Client (JS)

本目录包含 Agent-to-Agent (A2A) 通信协议的 TypeScript 客户端实现。

## `client.ts`

该文件定义了 `A2AClient` 类，提供通过 HTTP 使用 JSON-RPC 与 A2A 服务器交互的方法。

### 核心特性:

- **JSON-RPC 通信:** 遵循 JSON-RPC 2.0 规范处理请求发送和响应接收（支持标准响应和通过服务器发送事件实现的流式响应）
- **A2A 方法实现:** 提供标准 A2A 方法包括 `sendTask`, `sendTaskSubscribe`, `getTask`, `cancelTask`, `setTaskPushNotification`, `getTaskPushNotification` 和 `resubscribeTask`
- **错误处理:** 提供基础网络错误和 JSON-RPC 错误处理
- **流式支持:** 通过服务器发送事件 (SSE) 管理实时任务更新 (`sendTaskSubscribe`, `resubscribeTask`)
- **可扩展性:** 支持为不同环境（如 Node.js）提供自定义 `fetch` 实现

### 基础用法