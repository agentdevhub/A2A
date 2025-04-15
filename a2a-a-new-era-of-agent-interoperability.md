```![A2A protocol](https://s2.loli.net/2025/04/15/1h4Wt6MCdr9YGqf.jpg)

## **智能体互操作性的新时代**

AI智能体通过自主处理大量日常重复性或复杂任务，为提升人类生产力提供了独特机遇。当前，企业正加速构建和部署自主智能体，从订购新笔记本电脑到辅助客服代表，再到供应链规划支持，全方位实现工作流程的规模化、自动化和智能化。

要充分发挥智能体AI的潜力，关键在于让这些智能体能在跨越数据孤岛和应用程序的动态多智能体生态中协作。通过实现不同厂商或框架开发的智能体之间的互操作性，不仅能增强自主性并实现生产力倍增，还能有效降低长期运营成本。

**今日，我们联合超过50家技术合作伙伴**——包括Atlassian、Box、Cohere、Intuit、Langchain、MongoDB、PayPal、Salesforce、SAP、ServiceNow、UKG和Workday等技术企业，以及埃森哲、波士顿咨询、凯捷、德勤、HCLTech、印孚瑟斯、毕马威、麦肯锡、普华永道、TCS和Wipro等领先服务商——**共同推出名为Agent2Agent（A2A）的全新开放协议**。该协议将支持AI智能体在不同企业平台或应用程序之间安全交换信息并协调行动。我们相信A2A框架能为客户创造显著价值，使其AI智能体能够在整个企业应用生态中协同工作。

这一合作标志着行业对未来的共同愿景：无论底层技术如何，AI智能体都能无缝协作，实现复杂企业工作流程自动化，推动效率与创新达到前所未有的高度。

A2A作为开放协议，与Anthropic的模型上下文协议（MCP）形成互补。基于谷歌在规模化智能体系统领域的内部经验，A2A协议专门针对大规模多智能体系统部署中的痛点设计。开发者可借此构建能与任何遵循协议的智能体连接的解决方案，用户也能灵活组合不同厂商的智能体。更重要的是，企业将获得跨平台和云环境管理智能体的标准化方法。我们认为，这种普适互操作性是实现协作型AI智能体全部潜能的关键。

![Google Cloud - Partners contributing to the Agent 2 Agent protocol - Accenture, Arize, Articul, ask-ai, Atlassian, BCG, Box, c3.ai, Capgemini, Chronosphere, Cognizant, Cohere, Colibra, Contextual.ai, Cotality, Datadog, and more](https://s2.loli.net/2025/04/15/TXCcAzlnGZRMfiw.png)

## A2A设计原则

在与合作伙伴共同设计协议时，我们遵循五大核心原则：

- **释放智能体潜能**：支持智能体以原生非结构化模态协作，即使不共享内存、工具和上下文。实现真正多智能体场景，而非将智能体局限为"工具"

- **立足现有标准**：基于HTTP、SSE、JSON-RPC等通用标准构建，便于与企业现有IT架构集成

- **默认安全机制**：支持企业级认证授权，与OpenAPI的认证方案保持同等安全级别

- **长时任务支持**：灵活应对从即时任务到需数小时甚至数日深度研究的场景，在人机协同过程中提供实时反馈、通知和状态更新

- **多模态适配**：突破文本限制，支持音视频流等多样化交互形式

## **A2A工作原理**

![流程图展示远程智能体与客户端智能体之间的安全协作、任务与状态管理、用户体验协商及能力发现等数据交互](https://s2.loli.net/2025/04/15/2gzAnGsMECYjJ85.png)

A2A协议协调"客户端"智能体与"远程"智能体的交互。客户端负责任务规划与传达，远程端负责执行并反馈。核心功能包括：

- **能力发现**：通过JSON格式的"智能体卡片"公示能力，客户端可择优调用

- **任务管理**：以任务生命周期为核心，支持即时完成或长时协作，产出称为"成果物"

- **智能体协作**：通过消息传递上下文、回复、成果物或用户指令

- **用户体验协商**：消息中的"部件"支持富媒体格式（如图像），通过内容类型协商确保与用户界面能力（如iframe、视频、Web表单等）适配

详见[协议草案](https://github.com/google/A2A)。

## **现实案例：人才招聘**

<video autoplay="" loop="" muted="" playsinline="" poster="https://storage.googleapis.com/gweb-developer-goog-blog-assets/original_videos/wagtailvideo-jtw5bpu9_thumb.jpg" style="display: inline-block; vertical-align: baseline; box-sizing: border-box; width: 790px; height: 390px;"></video>

右键点击在新标签页中查看

通过Agentspace统一界面，招聘经理可指示智能体筛选符合要求的软件工程师候选人。智能体将协调多个专业智能体完成人才搜寻，用户确认后自动安排面试，最终由另一智能体完成背景调查。该案例展示了跨系统智能体协作如何简化招聘流程。

## **智能体互操作性的未来**

A2A有望开启智能体互操作的新纪元，推动创新并构建更强大的智能系统。我们相信该协议将引领智能体无缝协作解决复杂问题、提升人类生活质量的未来。

我们承诺与合作伙伴及社区共建开放生态，以开源形式发布协议并建立清晰的贡献路径。访问[A2A网站](https://google.github.io/A2A)查阅[完整草案](https://github.com/google/A2A)、代码示例及应用场景，了解参与方式。预计今年晚些时候将推出生产就绪版本。

## **合作伙伴评价**

### **技术合作伙伴**

**Atlassian**  
> A2A协议将帮助Rovo智能体实现规模化发现、协调与推理，推动更丰富的委托与协作形式  
——Brendan Haire，AI平台工程副总裁

**Cohere**  
> A2A确保隔离环境中也能实现可信协作，使企业能在不妥协管控的前提下规模化创新  
——Autumn Moulder，工程副总裁

**LangChain**  
> 智能体间交互是必然趋势，我们期待与谷歌共同制定满足开发者需求的协议标准  
——Harrison Chase，联合创始人兼CEO

**MongoDB**  
> 结合MongoDB混合搜索能力与A2A协议，将重新定义零售、制造等行业的AI应用未来  
——Andrew Davidson，产品高级副总裁

### **服务合作伙伴**

**埃森哲**  
> A2A是连接领域专属智能体的桥梁，能激发集体智慧解决复杂挑战  
——Scott Alfieri，全球负责人

**德勤**  
> 该协议将极大加速智能体AI的行业应用进程  
——Gopal Srinivasan

**TCS**  
> A2A是语义互操作性新时代的基石，我们自豪引领这场变革  
——Anupam Singhal，制造业务总裁

**印孚瑟斯**  
> 开放协议是规模化AI创新的基础，我们致力于推进智能体互操作性  
——Nagendra P Bandaru，技术服务全球主管```