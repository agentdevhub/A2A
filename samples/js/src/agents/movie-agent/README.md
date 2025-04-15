```# 电影信息代理

该代理使用 TMDB API 回答关于电影的查询。运行步骤如下：

```bash
export TMDB_API_KEY=<api_key> # 请参考 https://developer.themoviedb.org/docs/getting-started
export GEMINI_API_KEY=<api_key>
npm run agents:movie-agent
```

代理服务将在 `http://localhost:41241` 上启动。
```