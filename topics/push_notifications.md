# 远程代理至客户端的更新

<!-- TOC -->

- [远程代理至客户端的更新](#远程代理至客户端的更新)
    - [连接状态](#连接状态)
        - [断开连接](#断开连接)
        - [设置任务通知](#设置任务通知)
        - [代理安全](#代理安全)
        - [通知接收方安全](#通知接收方安全)
            - [非对称密钥](#非对称密钥)
            - [对称密钥](#对称密钥)
            - [OAuth](#oauth)
            - [Bearer Token](#bearer-token)
        - [其他注意事项](#其他注意事项)
            - [重放攻击防护](#重放攻击防护)
            - [密钥轮换](#密钥轮换)

<!-- /TOC -->

某些任务可能需要数分钟、数小时甚至数天才能完成（例如*"将样品寄送到佛罗里达州的客户处并在送达时通知我"*）。A2A 代理需要支持长期通信机制，这包括连接状态和断开状态下的通信。

客户端可通过代理卡片检查代理是否支持 streaming 和 pushNotifications 能力：
<pre>
{
  "name": "your-agent-name",
  "description": "your-agent-description"
  ...

  "capabilities": {
    <b>"streaming": true,</b>
    <b>"pushNotifications": false,</b>
    "stateTransitionHistory": false
  }

  ...
}
</pre>

代理可通过以下方式获取任务执行更新：
1. **持久连接**：客户端可通过 HTTP + 服务器推送事件（Server-sent events）与代理建立持久连接。代理可通过这些连接向各客户端发送任务更新。

2. **推送通知**：代理可将完整的最新 Task 对象负载发送至客户端指定的推送通知 URL。此机制类似于某些平台的 webhook。
无论客户端是否订阅了任务，均可为其任务设置通知。当代理将任务处理至终止状态（如 "completed"、"input-required" 等）并生成完整的状态关联消息及产物时，应发送通知。

无论客户端是否订阅了任务，均可为其任务设置通知信息。代理应在适当时机发送通知，例如当任务进入终止状态（如 "completed"、"input-required" 等）并生成完整的状态关联消息及产物时。

## 连接状态
在连接状态下，代理间通过 Task（及相关）消息进行更新。客户端和远程代理可通过同一连接并行处理多个任务。

客户端使用 [Task/Send](/documentation.md#send-a-task) 更新当前任务或响应代理需求。远程代理在流式传输时通过 [Task Updates](/documentation.md#streaming-support) 响应，非流式传输时通过 [Task](/documentation.md#get-a-task) 响应。非流式传输时，客户端可定期轮询。

若连接中断，代理可通过 [Task/Resubscribe](/documentation.md#resubscribe-to-task) 方法恢复连接并获取实时更新。

## 断开连接
针对断连场景，A2A 支持推送通知机制，代理可通过 [PushNotificationConfig](/documentation.md#push-notifications) 在非连接会话期间通知客户端更新。在企业内外部，代理必须验证通知服务身份、完成服务认证，并提供与执行任务关联的标识符。

通知服务（NotificationService）应视为独立于客户端代理的服务，不保证也不预期由客户端直接运行。该服务负责代理的认证鉴权，并将验证后的通知代理至适当端点（可能是 pub/sub 队列、电子邮件收件箱或其他通知服务等）。

在特殊场景下（如 VPC 内的本地服务网格），客户端可选择自行开放端口作为通知服务。但建议企业级部署使用集中式服务，通过可信通知凭证认证远程代理，并处理在线/离线场景。此类服务类似于具备独立认证鉴权控制的移动推送通知服务。

## 设置任务通知
客户端需通过设置任务推送通知配置来异步接收任务更新。应生成 taskId 并通过 "tasks/pushNotification/set" RPC 或直接在 "tasks/send"、"tasks/sendSubscribe" 的 `pushNotification` 参数中设置通知配置。

<pre>
interface PushNotificationConfig {
  url: string;
  token?: string; // 该任务/会话的唯一令牌
  authentication?: {
    schemes: string[];
    credentials?: string;
  }
}

interface TaskPushNotificationConfig {
  id: string; //任务ID
  pushNotificationConfig: PushNotificationConfig;
}

// 发送任务请求（含推送通知配置）
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
    "pushNotification": {
      "url": "https://example.com/callback",
      "authentication": {
        "schemes": ["bearer"]
      }
    },
    "metadata": {}
  }
}

//响应
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

// 设置推送通知配置请求
{
  "jsonrpc": "2.0",
  "id": 1,
  "method":"tasks/pushNotification/set",
  "params": {
    "id": "de38c76d-d54c-436c-8b9f-4c2703648d64",    
    "pushNotificationConfig": {
      "url": "https://example.com/callback",
      "authentication": {
        "schemes": ["bearer"]
      }
    }
  }
}

//响应
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": {
    "id": "de38c76d-d54c-436c-8b9f-4c2703648d64",    
    "pushNotificationConfig": {
      "url": "https://example.com/callback",
      "authentication": {
        "schemes": ["bearer"]
      }
    }
  }
}
</pre>

## 代理安全
代理不应盲目信任客户端指定的推送通知 URL。推荐采用以下安全实践：

1. 通过 GET 挑战请求验证 URL
    * 挑战请求可使用相同 URL，并通过查询参数或标头携带 validationToken
    * 通知服务（或简单场景下的客户端）需返回相同 validationToken
    * 该机制可防止恶意客户端诱导代理对 URL 发起 DDoS 攻击
    * 代理可在注册 URL 时执行一次性验证或定期检查
    <pre>
    GET https://abc.com/callback-path?validationToken=randomString
    Content-Length: 0

    HTTP/1.1 200 OK
    Content-Type: text/plain

    randomString
    </pre>

    示例实现可参考 [LangGraph](https://github.com/google/A2A/blob/main/samples/python/agents/langgraph/task_manager.py) 的 `set_push_notification_info` 方法和 [CLI 推送监听器](https://github.com/google/A2A/blob/main/samples/python/hosts/cli/push_notification_listener.py)

2. 通知服务身份验证
    * 可要求通知服务使用预设密钥对 validationToken 签名
    * 密钥可由代理生成（专用于本次挑战）
    * 若使用对称密钥认证，通知服务可用相同密钥签名

## 通知接收方安全
通知接收方应验证通知真实性。常用方法如下（更多安全方案参见 https://webhooks.fyi）：

[JWT + JWKS 非对称密钥示例](https://github.com/google/A2A/blob/main/samples/python/agents/langgraph/__main__.py) 和 [CLI 主机实现](https://github.com/google/A2A/blob/main/samples/python/hosts/cli/__main__.py)

#### 非对称密钥
使用 ECDSA、RSA 等算法生成公私钥对：
1. 通知服务生成密钥对时，需将私钥提供给代理。通知服务保留公钥验证代理签名
2. 代理生成密钥对时：
    * 手动向接收方提供公钥
    * 通过 JWKS 协议提供公钥

代理可使用私钥签名请求负载，或在标头提供 JWT 令牌。JWT 协议标准化了 keyId、时间戳等字段。

#### 对称密钥
双方使用共享密钥签名验证。通知服务使用相同密钥重新签名验证。可使用 JWT 生成签名令牌。

非对称密钥优势在于私钥仅代理持有，降低泄露风险。

#### OAuth
代理从 OAuth 服务器获取令牌，并在请求中提供。通知服务提取令牌并向 OAuth 服务器验证。

#### Bearer Token
任一方生成承载令牌。若由接收方生成，需通过任务推送通知配置提供给代理。

因令牌以明文传输存在泄露风险，建议使用签名机制（非对称/对称密钥）验证负载真实性。

## 其他注意事项
#### 重放攻击防护
在 JWT 中使用 iat 字段或自定义标头记录事件时间戳。建议拒绝超过 5 分钟的历史事件。时间戳应参与签名计算以验证其真实性。
#### 密钥轮换
推荐实现零停机密钥轮换。JWKS 允许代理发布新旧公钥，通知接收方应能使用所有有效密钥验证请求。