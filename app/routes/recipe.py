from flask import Blueprint, request, redirect, url_for, render_template, flash, current_app
from app.models.recipe import Recipe, Tag
from app.models import db
from sqlalchemy.sql.expression import func
import os
from werkzeug.utils import secure_filename

recipe_bp = Blueprint('recipe', __name__, url_prefix='/recipes')

def save_image(image_file):
    if not image_file or not image_file.filename:
        return None
    filename = secure_filename(image_file.filename)
    if filename:
        upload_folder = current_app.config['UPLOAD_FOLDER']
        filepath = os.path.join(upload_folder, filename)
        image_file.save(filepath)
        return filename
    return None

@recipe_bp.route('/search', methods=['GET'])
def search():
    q = request.args.get('q', '')
    if q:
        recipes = Recipe.query.filter(
            (Recipe.title.ilike(f'%{q}%')) | (Recipe.ingredients.ilike(f'%{q}%'))
        ).all()
        title = f"搜尋結果：{q}"
    else:
        recipes = []
        title = "請輸入搜尋關鍵字"
    return render_template('recipe/list.html', recipes=recipes, title=title)

@recipe_bp.route('/random', methods=['GET'])
def random_recipe():
    recipe = Recipe.query.order_by(func.random()).first()
    if recipe:
        return redirect(url_for('recipe.detail', id=recipe.id))
    else:
        flash('目前還沒有任何食譜，趕快來新增一筆吧！', 'warning')
        return redirect(url_for('main.index'))

@recipe_bp.route('/new', methods=['GET', 'POST'])
def new():
    if request.method == 'POST':
        title = request.form.get('title')
        if not title:
            flash('食譜標題為必填', 'error')
            return redirect(url_for('recipe.new'))
        
        ingredients = request.form.get('ingredients')
        steps = request.form.get('steps')
        notes = request.form.get('notes')
        
        image_file = request.files.get('image')
        image_path = save_image(image_file)
        
        # 處理標籤
        tag_names = request.form.get('tags', '').split(',')
        tags = []
        for name in tag_names:
            name = name.strip()
            if name:
                tag = Tag.query.filter_by(name=name).first()
                if not tag:
                    tag = Tag.create(name=name)
                if tag:
                    tags.append(tag)
                
        recipe = Recipe.create(
            title=title, ingredients=ingredients, steps=steps, notes=notes,
            image_path=image_path, tags=tags
        )
        if recipe:
            flash('新增成功！', 'success')
            return redirect(url_for('recipe.detail', id=recipe.id))
        else:
            flash('新增失敗，請稍後再試', 'error')
            
    return render_template('recipe/form.html', recipe=None)

@recipe_bp.route('/<int:id>', methods=['GET'])
def detail(id):
    recipe = Recipe.get_by_id(id)
    if not recipe:
        flash('找不到該食譜', 'error')
        return redirect(url_for('main.index'))
    return render_template('recipe/detail.html', recipe=recipe)

@recipe_bp.route('/<int:id>/edit', methods=['GET', 'POST'])
def edit(id):
    recipe = Recipe.get_by_id(id)
    if not recipe:
        flash('找不到該食譜', 'error')
        return redirect(url_for('main.index'))
        
    if request.method == 'POST':
        title = request.form.get('title')
        if not title:
            flash('食譜標題為必填', 'error')
            return redirect(url_for('recipe.edit', id=id))
            
        kwargs = {
            'title': title,
            'ingredients': request.form.get('ingredients'),
            'steps': request.form.get('steps'),
            'notes': request.form.get('notes'),
        }
        
        image_file = request.files.get('image')
        if image_file and image_file.filename:
            kwargs['image_path'] = save_image(image_file)
            
        tag_names = request.form.get('tags', '').split(',')
        tags = []
        for name in tag_names:
            name = name.strip()
            if name:
                tag = Tag.query.filter_by(name=name).first()
                if not tag:
                    tag = Tag.create(name=name)
                if tag:
                    tags.append(tag)
        kwargs['tags'] = tags
        
        if Recipe.update(id, **kwargs):
            flash('更新成功！', 'success')
            return redirect(url_for('recipe.detail', id=id))
        else:
            flash('更新失敗，請稍後再試', 'error')
            
    return render_template('recipe/form.html', recipe=recipe)

@recipe_bp.route('/<int:id>/delete', methods=['POST'])
def delete(id):
    if Recipe.delete(id):
        flash('食譜已刪除', 'success')
    else:
        flash('刪除失敗', 'error')
    return redirect(url_for('main.index'))

@recipe_bp.route('/<int:id>/favorite', methods=['POST'])
def favorite(id):
    recipe = Recipe.get_by_id(id)
    if recipe:
        Recipe.update(id, is_favorite=not recipe.is_favorite)
    return redirect(request.referrer or url_for('recipe.detail', id=id))
