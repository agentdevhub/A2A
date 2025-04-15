# 发现Agent Card

<!-- TOC -->

- [发现Agent Card](#发现agent-card)
  - [开放发现](#开放发现)
  - [策展式发现（基于注册中心）](#策展式发现基于注册中心)
  - [私有发现（基于API）](#私有发现基于api)
  - [保护Agent Card的安全](#保护agent-card的安全)

<!-- /TOC -->

A2A的[AgentCard](/documentation.md#agent-card)规范了发现过程中共享数据的*格式*，但发现这些Agent Card的方式是无限的。我们期待这是一个开放的讨论话题，并希望从社区中获得更多创意。

以下是我们当前的思路。

## 开放发现
建议企业将Agent Card托管在标准化路径下，具体为：https://`DOMAIN`/.well-known/agent.json。客户端可通过DNS解析已知或发现的域名，向该路径发送简单的`GET`请求以获取Agent Card。

这种方式使得网络爬虫和应用程序能够轻松发现已知或已配置域名的Agent。这本质上将发现过程简化为“找到一个域名”。

## 策展式发现（基于注册中心）
我们预见企业应用将通过目录接口提供精心维护的Agent注册中心。这将支持更多企业场景，例如由管理员维护的、公司或团队专属的Agent注册中心。

*我们**正在**考虑在协议中增加注册中心支持——欢迎通过[反馈渠道](https://github.com/google/A2A/blob/main/README.md#contributing)分享您的观点及潜在应用场景*

## 私有发现（基于API）
未来必然会出现私有“Agent仓库”或专有Agent，它们通过自定义API在封闭环境中交换Agent Card。

*我们**目前不打算**将私有发现API纳入A2A协议范围——欢迎通过[反馈渠道](https://github.com/google/A2A/blob/main/README.md#contributing)说明您认为此类API应被标准化的场景*

## 保护Agent Card的安全
Agent Card可能包含敏感信息。实现者可通过身份验证和授权机制来保护Agent Card。例如，在组织内部，即使是标准化路径的开放发现也可通过mTLS进行保护，并限制特定客户端的访问。注册中心和私有发现API应要求身份验证，并根据不同身份返回不同的信息。

需注意：实现者可能在Agent Card中包含凭证信息（如API密钥）。强烈建议此类信息**必须**在无身份验证时完全不可见。