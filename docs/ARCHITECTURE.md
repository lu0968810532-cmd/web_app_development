# 系統架構設計文件 (ARCHITECTURE) - 食譜收藏夾

本文件基於 PRD（產品需求文件）定義「食譜收藏夾」的系統架構，包含技術選型、資料夾結構、元件關係與關鍵設計決策。

## 1. 技術架構說明

本專案採用傳統 Web 應用程式架構，前後端不分離，由伺服器端負責渲染 HTML。

### 選用技術與原因
*   **後端框架：Python + Flask**
    *   **原因**：Flask 是輕量級的 Python Web 框架，適合快速開發中小型應用程式。食譜收藏夾的 MVP 需求單純，Flask 能提供足夠的彈性與快速開發的優勢。
*   **模板引擎：Jinja2**
    *   **原因**：Flask 內建支援 Jinja2，能方便地將後端資料注入 HTML 模板中，動態渲染頁面，符合不採用前後端分離的技術限制。
*   **資料庫：SQLite (搭配 SQLAlchemy ORM)**
    *   **原因**：SQLite 是輕量級的檔案型資料庫，不需額外架設資料庫伺服器，非常適合單機或桌面端應用情境，也方便使用者直接備份資料庫檔案。使用 SQLAlchemy ORM 可以有效防範 SQL Injection 並簡化資料庫操作。
*   **前端技術：HTML / CSS / 少量 JavaScript**
    *   **原因**：以伺服器渲染為主，JavaScript 僅用於輔助增強使用者體驗（如：圖片上傳預覽、表單驗證等）。

### Flask MVC 模式說明
雖然 Flask 本身不強制要求 MVC 架構，但專案將採用類似 MVC (Model-View-Controller) 的設計模式來組織程式碼：
*   **Model (模型)**：負責定義資料結構與資料庫互動邏輯。例如：`Recipe`、`Tag` 等 SQLAlchemy 類別，處理資料的 CRUD 與關聯。
*   **View (視圖)**：負責呈現使用者介面。在這裡指的是 Jinja2 模板（`.html` 檔案），負責將 Controller 傳遞的資料渲染成最終的網頁。
*   **Controller (控制器)**：負責接收使用者請求、處理商業邏輯並回傳回應。在 Flask 中即為 **Routes (路由)**，例如處理 `/recipes` 的 GET/POST 請求，呼叫 Model 取得資料後，再交由 View 渲染。

## 2. 專案資料夾結構

以下為專案的建議資料夾結構：

```text
web_app_development/
├── app/                      # 應用程式主要程式碼
│   ├── __init__.py           # Flask App 初始化、設定載入與擴充套件註冊
│   ├── models/               # 資料庫模型 (Model)
│   │   ├── __init__.py
│   │   └── recipe.py         # 食譜與標籤相關資料表定義
│   ├── routes/               # 路由與控制器邏輯 (Controller)
│   │   ├── __init__.py
│   │   ├── main.py           # 首頁與一般路由
│   │   └── recipe.py         # 食譜 CRUD 相關路由
│   ├── templates/            # Jinja2 HTML 模板 (View)
│   │   ├── base.html         # 基礎共用模板 (Navbar, Footer, 共用 CSS/JS)
│   │   ├── index.html        # 首頁 / 隨機選餐
│   │   └── recipe/           # 食譜相關頁面
│   │       ├── list.html     # 食譜列表與搜尋結果
│   │       ├── detail.html   # 食譜詳細內容
│   │       └── form.html     # 新增/編輯食譜表單
│   └── static/               # 靜態資源
│       ├── css/
│       │   └── style.css     # 自訂樣式表
│       ├── js/
│       │   └── main.js       # 前端互動邏輯 (如圖片預覽)
│       └── uploads/          # 使用者上傳的圖片存放區
├── instance/                 # 執行個體特定資料 (不加入版本控制)
│   └── database.db           # SQLite 資料庫檔案
├── docs/                     # 專案文件
│   ├── PRD.md                # 產品需求文件
│   └── ARCHITECTURE.md       # 系統架構文件
├── .gitignore                # Git 忽略清單
├── requirements.txt          # Python 依賴套件清單
└── app.py                    # 應用程式啟動入口 (Entry point)
```

## 3. 元件關係圖

以下是系統運作的元件關係圖，展示了使用者從瀏覽器發出請求到資料庫讀寫的流程。

```mermaid
flowchart TD
    Browser[瀏覽器 (Browser)]
    
    subgraph Flask Application [Flask 應用程式]
        Route[Flask Route<br/>(Controller)]
        Template[Jinja2 Template<br/>(View)]
        Model[SQLAlchemy Model<br/>(Model)]
    end
    
    DB[(SQLite 資料庫)]
    FileSys[本地檔案系統<br/>(圖片上傳)]

    %% 請求流程
    Browser -- "1. 發送 HTTP 請求 (GET/POST)" --> Route
    
    %% 資料處理
    Route -- "2. 查詢 / 寫入資料" --> Model
    Model -. "3. 回傳資料物件" .-> Route
    Model <--> DB
    
    %% 檔案處理
    Route -- "儲存 / 讀取圖片" --> FileSys
    
    %% 渲染流程
    Route -- "4. 傳遞資料並渲染" --> Template
    Template -. "5. 產出 HTML" .-> Route
    
    %% 回應流程
    Route -- "6. 回傳 HTTP 回應 (HTML)" --> Browser
    
    %% 靜態資源請求
    Browser -- "請求靜態資源 (CSS/JS/圖片)" --> FileSys
```

## 4. 關鍵設計決策

1.  **採用伺服器端渲染 (SSR) 而非前後端分離 (SPA)**
    *   **原因**：考量到專案目標為 MVP 及單機/桌面端應用情境，伺服器端渲染 (Flask + Jinja2) 能大幅降低開發複雜度，不需要維護獨立的前端專案與 API 介接，且能快速達成表單提交、列表顯示等核心功能。
2.  **使用 SQLite 作為資料庫**
    *   **原因**：符合「單機應用程式」的需求。SQLite 不需要獨立的 Server Process，資料以單一檔案 (`instance/database.db`) 存在，這使得使用者備份、轉移資料庫的成本極低（只需複製一個檔案），非常適合食譜收藏夾的使用情境。
3.  **圖片直接儲存於本地檔案系統 (`static/uploads/`)**
    *   **原因**：不依賴外部的雲端儲存服務（如 AWS S3），確保應用程式能完全在本地離線運行。在圖片上傳時，將透過後端邏輯限制檔案大小，並重新命名確保檔名唯一，以避免應用程式資料夾過度膨脹或檔名衝突。
4.  **採用 Blueprint 模組化路由**
    *   **原因**：雖然目前功能單純，但將路由依功能拆分（例如 `main.py` 處理首頁與隨機選餐，`recipe.py` 處理食譜 CRUD）可以讓程式碼結構更清晰，未來若要擴充功能（如標籤管理獨立為一個模組）也更易於維護。
