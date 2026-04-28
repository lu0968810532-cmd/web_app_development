# 流程圖文件 (FLOWCHART) - 食譜收藏夾

本文件基於 PRD 與系統架構，呈現「食譜收藏夾」的使用者流程、系統序列圖與功能清單對照表。

## 1. 使用者流程圖（User Flow）

此流程圖描述使用者進入系統後，可以進行的各項主要操作路徑。

```mermaid
flowchart LR
    A([使用者開啟系統]) --> B[首頁 / 食譜列表]
    
    B --> C{選擇操作}
    
    %% 瀏覽與檢索
    C -->|搜尋食譜| D[輸入關鍵字搜尋]
    D --> E[顯示搜尋結果列表]
    E --> F[點擊查看食譜詳細內容]
    
    C -->|依標籤/收藏瀏覽| G[點選標籤 / 最愛分類]
    G --> H[顯示分類結果列表]
    H --> F
    
    C -->|不知道吃什麼| I[點擊隨機選餐]
    I --> F
    
    %% 食譜管理
    C -->|新增食譜| J[進入新增食譜表單]
    J --> K[填寫標題、食材、步驟並上傳圖片]
    K --> L{送出表單}
    L -->|成功| F
    L -->|失敗/未填完整| J
    
    %% 詳細頁內操作
    F --> M{詳細頁操作}
    M -->|編輯| N[進入編輯食譜表單]
    N --> K
    M -->|刪除| O[確認刪除]
    O --> B
    M -->|切換收藏狀態| P[更新最愛狀態]
    P --> F
    M -->|回首頁| B
```

## 2. 系統序列圖（Sequence Diagram）

此序列圖描述「新增食譜並上傳圖片」的核心系統互動流程。

```mermaid
sequenceDiagram
    actor User as 使用者
    participant Browser as 瀏覽器 (HTML/JS)
    participant Flask as Flask Route (Controller)
    participant FileSys as 本地檔案系統
    participant DB as SQLite (Model)

    User->>Browser: 填寫食譜內容、選擇圖片並點擊送出
    Browser->>Flask: POST /recipes/new (含表單資料與圖片)
    
    %% 後端處理流程
    Flask->>Flask: 驗證表單欄位是否完整
    alt 欄位驗證失敗
        Flask-->>Browser: 回傳錯誤訊息，重新渲染表單
        Browser-->>User: 顯示錯誤提示
    else 驗證成功
        alt 有上傳圖片
            Flask->>FileSys: 限制大小、重新命名並儲存至 static/uploads/
            FileSys-->>Flask: 儲存成功，回傳檔案路徑
        end
        
        Flask->>DB: INSERT INTO recipes (標題, 食材, 步驟, 圖片路徑)
        DB-->>Flask: 新增成功
        
        Flask-->>Browser: Redirect (302) 到詳細頁面 (/recipes/<id>)
        Browser->>Flask: GET /recipes/<id>
        Flask->>DB: SELECT * FROM recipes WHERE id = <id>
        DB-->>Flask: 回傳食譜資料
        Flask-->>Browser: 渲染詳細頁 HTML
        Browser-->>User: 顯示新增成功的食譜內容
    end
```

## 3. 功能清單對照表

以下為 MVP 階段主要功能的 URL 路徑與 HTTP 方法規劃：

| 功能名稱 | 對應 URL 路徑 | HTTP 方法 | 說明 |
| :--- | :--- | :--- | :--- |
| **首頁 / 所有食譜** | `/` 或 `/recipes` | `GET` | 顯示食譜列表，支援分頁 |
| **關鍵字搜尋** | `/recipes/search` | `GET` | 透過 `?q=關鍵字` 進行搜尋 |
| **隨機選餐** | `/recipes/random` | `GET` | 從資料庫隨機抽取一筆並導向詳細頁 |
| **新增食譜 (表單)** | `/recipes/new` | `GET` | 渲染新增食譜的 HTML 表單 |
| **新增食譜 (送出)** | `/recipes/new` | `POST` | 接收表單與圖片，處理並存入資料庫 |
| **食譜詳細內容** | `/recipes/<int:id>` | `GET` | 顯示單一食譜的詳細資訊與圖片 |
| **編輯食譜 (表單)** | `/recipes/<int:id>/edit` | `GET` | 渲染包含既有資料的編輯表單 |
| **編輯食譜 (送出)** | `/recipes/<int:id>/edit` | `POST` | 更新食譜資料 (可換圖片) |
| **刪除食譜** | `/recipes/<int:id>/delete` | `POST` | 刪除該食譜 (與關聯圖片) |
| **標籤過濾** | `/tags/<int:tag_id>` | `GET` | 顯示特定標籤底下的食譜 |
| **切換收藏狀態** | `/recipes/<int:id>/favorite` | `POST` | 將食譜加入/移除最愛清單 |

> 註：由於 HTML 表單原生不支援 `PUT` / `DELETE`，因此表單送出（如更新、刪除）皆統一使用 `POST` 方法，並可視需求在路徑加上 `/edit` 或 `/delete` 標識。
