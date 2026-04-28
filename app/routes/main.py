from flask import Blueprint, render_template

main_bp = Blueprint('main', __name__)

@main_bp.route('/', methods=['GET'])
def index():
    """
    顯示首頁，列出所有食譜（可分頁）。
    對應模板：templates/index.html
    """
    pass

@main_bp.route('/tags/<int:tag_id>', methods=['GET'])
def tag_filter(tag_id):
    """
    顯示特定標籤底下的食譜。
    對應模板：templates/recipe/list.html
    """
    pass
