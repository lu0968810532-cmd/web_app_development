# 路由設計文件 (ROUTES) - 食譜收藏夾

本文件基於 PRD 與架構設計，規劃 Flask 的路由與頁面對應關係。

## 1. 路由總覽表格

| 功能 | HTTP 方法 | URL 路徑 | 對應模板 | 說明 |
| :--- | :--- | :--- | :--- | :--- |
| **首頁 / 食譜列表** | GET | `/` | `templates/index.html` | 顯示所有食譜，依時間倒序排列 |
| **標籤過濾** | GET | `/tags/<tag_id>` | `templates/recipe/list.html` | 顯示特定標籤底下的食譜 |
| **關鍵字搜尋** | GET | `/recipes/search` | `templates/recipe/list.html` | 透過 `?q=關鍵字` 搜尋標題或食材 |
| **隨機選餐** | GET | `/recipes/random` | — (重導向) | 隨機挑選一筆並導向食譜詳情頁 |
| **新增食譜頁面** | GET | `/recipes/new` | `templates/recipe/form.html` | 顯示新增表單 |
| **建立食譜** | POST | `/recipes/new` | — (重導向) | 接收表單與圖片，存入 DB 後重導向至詳情頁 |
| **食譜詳情** | GET | `/recipes/<id>` | `templates/recipe/detail.html` | 顯示單一食譜 |
| **編輯食譜頁面** | GET | `/recipes/<id>/edit` | `templates/recipe/form.html` | 顯示編輯表單，帶入原資料 |
| **更新食譜** | POST | `/recipes/<id>/edit` | — (重導向) | 接收表單，更新 DB 後重導向至詳情頁 |
| **刪除食譜** | POST | `/recipes/<id>/delete` | — (重導向) | 刪除資料與圖片，重導向至首頁 |
| **切換收藏** | POST | `/recipes/<id>/favorite`| — (重導向) | 切換最愛狀態，重導向回原頁面 |

## 2. 每個路由的詳細說明

### 2.1 首頁與分類 (main_bp)

*   **`GET /`**
    *   **輸入**：無（可接受 `?page=n` 分頁）
    *   **處理邏輯**：呼叫 `Recipe.get_all()`
    *   **輸出**：渲染 `templates/index.html`
*   **`GET /tags/<tag_id>`**
    *   **輸入**：URL 路徑參數 `tag_id`
    *   **處理邏輯**：查詢該標籤，取得 `Tag.recipes`
    *   **輸出**：渲染 `templates/recipe/list.html`
    *   **錯誤處理**：若標籤不存在回傳 404

### 2.2 食譜相關 (recipe_bp)

*   **`GET /recipes/search`**
    *   **輸入**：URL 參數 `?q=xxx`
    *   **處理邏輯**：使用 SQLAlchemy `ilike` 查詢標題或食材包含關鍵字的食譜
    *   **輸出**：渲染 `templates/recipe/list.html`
*   **`GET /recipes/random`**
    *   **處理邏輯**：從資料庫隨機取得 1 筆 `Recipe` (例如 `ORDER BY RANDOM() LIMIT 1`)
    *   **輸出**：重導向至 `/recipes/<id>`，若無食譜則導向首頁並顯示提示
*   **`GET /recipes/new`**
    *   **輸出**：渲染 `templates/recipe/form.html`，傳入空白表單
*   **`POST /recipes/new`**
    *   **輸入**：表單欄位 (`title`, `ingredients`, `steps`, `notes`, 上傳的 `image`)
    *   **處理邏輯**：儲存圖片至 `static/uploads/`，呼叫 `Recipe.create(...)`
    *   **輸出**：重導向至 `/recipes/<new_id>`
    *   **錯誤處理**：若 `title` 空白或格式錯誤，重繪表單並顯示錯誤訊息
*   **`GET /recipes/<id>`**
    *   **輸入**：URL 路徑參數 `id`
    *   **處理邏輯**：呼叫 `Recipe.get_by_id(id)`
    *   **輸出**：渲染 `templates/recipe/detail.html`
    *   **錯誤處理**：若食譜不存在回傳 404
*   **`GET /recipes/<id>/edit`**
    *   **處理邏輯**：呼叫 `Recipe.get_by_id(id)`
    *   **輸出**：渲染 `templates/recipe/form.html` 並帶入該食譜資料
*   **`POST /recipes/<id>/edit`**
    *   **輸入**：表單欄位與可能的圖片
    *   **處理邏輯**：處理新圖片（若有），呼叫 `Recipe.update(id, ...)`
    *   **輸出**：重導向至 `/recipes/<id>`
*   **`POST /recipes/<id>/delete`**
    *   **處理邏輯**：刪除關聯圖片，呼叫 `Recipe.delete(id)`
    *   **輸出**：重導向至 `/`
*   **`POST /recipes/<id>/favorite`**
    *   **處理邏輯**：取得食譜，反轉 `is_favorite` 的布林值，更新 DB
    *   **輸出**：重導向回 `request.referrer`（發出請求的上一頁）

## 3. Jinja2 模板清單

所有模板皆預設繼承自 `templates/base.html`：

*   **`templates/base.html`**：全站共用外框（Navbar、Footer、引入 CSS/JS 檔案）
*   **`templates/index.html`**：首頁，包含推薦區域、最近食譜列表
*   **`templates/recipe/list.html`**：共用列表頁，用於顯示「搜尋結果」或「標籤過濾結果」
*   **`templates/recipe/detail.html`**：單筆食譜的完整資訊顯示頁（含圖片、操作按鈕）
*   **`templates/recipe/form.html`**：共用表單頁，透過傳入參數決定是「新增」或「編輯」模式

## 4. 路由骨架程式碼

路由的 Python 骨架程式碼已建立於 `app/routes/` 中，包含：
*   `app/routes/main.py`
*   `app/routes/recipe.py`
