from flask import Blueprint, request, redirect, url_for, render_template

recipe_bp = Blueprint('recipe', __name__, url_prefix='/recipes')

@recipe_bp.route('/search', methods=['GET'])
def search():
    """
    透過關鍵字搜尋食譜。
    輸入：?q=關鍵字
    輸出：渲染 templates/recipe/list.html
    """
    pass

@recipe_bp.route('/random', methods=['GET'])
def random_recipe():
    """
    從資料庫隨機抽取一筆食譜。
    輸出：導向詳細頁 /recipes/<id>
    """
    pass

@recipe_bp.route('/new', methods=['GET', 'POST'])
def new():
    """
    GET: 渲染新增食譜的 HTML 表單 (templates/recipe/form.html)。
    POST: 接收表單與圖片，處理並存入資料庫，成功後重導向至詳細頁。
    """
    pass

@recipe_bp.route('/<int:id>', methods=['GET'])
def detail(id):
    """
    顯示單一食譜的詳細資訊與圖片。
    輸出：渲染 templates/recipe/detail.html
    """
    pass

@recipe_bp.route('/<int:id>/edit', methods=['GET', 'POST'])
def edit(id):
    """
    GET: 渲染包含既有資料的編輯表單 (templates/recipe/form.html)。
    POST: 更新食譜資料 (包含圖片處理)，成功後重導向至詳細頁。
    """
    pass

@recipe_bp.route('/<int:id>/delete', methods=['POST'])
def delete(id):
    """
    刪除該食譜 (與關聯圖片)。
    輸出：重導向至首頁 /
    """
    pass

@recipe_bp.route('/<int:id>/favorite', methods=['POST'])
def favorite(id):
    """
    將食譜加入/移除最愛清單。
    輸出：重導向回原頁面
    """
    pass
