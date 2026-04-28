from flask import Blueprint, render_template, request
from app.models.recipe import Recipe, Tag

main_bp = Blueprint('main', __name__)

@main_bp.route('/', methods=['GET'])
def index():
    """顯示首頁，列出所有食譜"""
    recipes = Recipe.get_all()
    return render_template('index.html', recipes=recipes)

@main_bp.route('/tags/<int:tag_id>', methods=['GET'])
def tag_filter(tag_id):
    """顯示特定標籤底下的食譜"""
    tag = Tag.get_by_id(tag_id)
    if not tag:
        return render_template('recipe/list.html', recipes=[], title="標籤不存在")
    return render_template('recipe/list.html', recipes=tag.recipes, title=f"標籤：{tag.name}")
