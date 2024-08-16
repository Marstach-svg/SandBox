from flask import Blueprint,render_template, url_for, redirect, abort, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from sandbox_system import db
from sandbox_system.models import Blog, BlogCategory, BlogFavorite, OtherBlog
from sandbox_system.blogs.form import BlogForm, BlogSearchForm, BlogCategoryForm, BlogFavoriteForm, OtherBlogForm
from sandbox_system.blogs.image import add_image


blogs = Blueprint('blogs', __name__)


#全てのブログの一覧ページ
@blogs.route('/blog_list', methods=['GET', 'POST'])
def blog_list():
    form = BlogSearchForm()
    category_form = BlogCategoryForm()
    if category_form.validate_on_submit():
        new_category = BlogCategory(category=category_form.category.data)
        db.session.add(new_category)
        db.session.commit()
        flash('カテゴリが追加されました')
        return redirect(url_for('blogs.blog_list'))
    blog_categories = BlogCategory.query.order_by(BlogCategory.id.asc()).all()
    page = request.args.get('page', 1, type=int)
    blogs = Blog.query.order_by(Blog.id.desc()).paginate(page=page, per_page=5)
    otherblogs = OtherBlog.query.order_by(OtherBlog.id.desc()).paginate(page=page, per_page=5)
    return render_template('blog/blog_list.html', form=form, blog_categories=blog_categories, blogs=blogs, otherblogs=otherblogs, category_form=category_form)

#sandboxブログの一覧ページ
@blogs.route('/sandbox_blog_list', methods=['GET', 'POST'])
def sandbox_blog_list():
    form = BlogSearchForm()
    category_form = BlogCategoryForm()
    if category_form.validate_on_submit():
        new_category = BlogCategory(category=category_form.category.data)
        db.session.add(new_category)
        db.session.commit()
        flash('カテゴリが追加されました')
        return redirect(url_for('blogs.sandbox_blog_list'))
    blog_categories = BlogCategory.query.order_by(BlogCategory.id.asc()).all()
    page = request.args.get('page', 1, type=int)
    blogs = Blog.query.order_by(Blog.id.desc()).paginate(page=page, per_page=10)
    return render_template('blog/sandbox_blog_list.html', form=form, blog_categories=blog_categories, blogs=blogs, category_form=category_form)

#他サイトブログの一覧ページ
@blogs.route('/other_blog_list', methods=['GET', 'POST'])
def other_blog_list():
    form = BlogSearchForm()
    category_form = BlogCategoryForm()
    if category_form.validate_on_submit():
        new_category = BlogCategory(category=category_form.category.data)
        db.session.add(new_category)
        db.session.commit()
        flash('カテゴリが追加されました')
        return redirect(url_for('blogs.other_blog_list'))
    page = request.args.get('page', 1, type=int)
    blog_categories = BlogCategory.query.order_by(BlogCategory.id.asc()).all()
    otherblogs = OtherBlog.query.order_by(OtherBlog.id.desc()).paginate(page=page, per_page=10)
    return render_template('blog/other_blog_list.html', form=form, otherblogs=otherblogs, blog_categories=blog_categories, category_form=category_form)

#sandboxブログ作成ページ
@blogs.route('/blog_create', methods=['GET', 'POST'])
@login_required
def blog_create():
    form = BlogForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture = add_image(form.picture.data)
        else:
            picture = ''
        blog = Blog(title=form.title.data, summary=form.summary.data, text=form.text.data, image=picture, user_id=current_user.id, category_id=form.category.data)
        db.session.add(blog)
        db.session.commit()
        flash('ブログを投稿しました')
        return redirect(url_for('blogs.blog_list'))
    return render_template('blog/blog_create.html', form=form)

#他サイトブログサムネ作成ページ
@blogs.route('/other_blog_create', methods=['GET', 'POST'])
@login_required
def other_blog_create():
    form = OtherBlogForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture = add_image(form.picture.data)
        else:
            picture = ''
        otherblog = OtherBlog(title=form.title.data, summary=form.summary.data, url=form.url.data, text=form.text.data, image=picture, category_id=form.category.data)
        db.session.add(otherblog)
        db.session.commit()
        flash('ブログを追加しました')
        return redirect(url_for('blogs.other_blog_list'))
    return render_template('blog/other_blog_create.html', form=form)

#sandboxブログ詳細ページ
@blogs.route('/<int:blog_id>/blog')
def blog(blog_id):
    blog = Blog.query.get_or_404(blog_id)
    form = BlogSearchForm()
    favorite_form = BlogFavoriteForm()
    blog_categories = BlogCategory.query.order_by(BlogCategory.id.asc()).all()
    if BlogFavorite.query.filter_by(user_id=current_user.id, blog_id=blog_id).first():
        favorite_blog = BlogFavorite.query.filter_by(user_id=current_user.id, blog_id=blog_id).first()
    else:
        favorite_blog = ''
    return render_template('blog/blog.html', blog=blog, form=form, favorite_form=favorite_form, blog_categories=blog_categories, favorite_blog=favorite_blog, blog_id=blog_id)

#全てのブログ検索
@blogs.route('/blog_search', methods=['GET', 'POST'])
def blog_search():
    form = BlogSearchForm()
    category_form = BlogCategoryForm()
    searchtext = ''
    if form.validate_on_submit():
        searchtext = form.searchtext.data
    elif request.method == 'GET':
        form.searchtext.data == ''
    if category_form.validate_on_submit():
        new_category = BlogCategory(category=category_form.category.data)
        db.session.add(new_category)
        db.session.commit()
        flash('カテゴリが追加されました')
        return redirect(url_for('blogs.blog_list'))
    page = request.args.get('page', 1, type=int)
    blogs = Blog.query.filter((Blog.text.contains(searchtext)) | (Blog.title.contains(searchtext)) | (Blog.summary.contains(searchtext))).order_by(Blog.id.desc()).paginate(page=page, per_page=10)
    otherblogs = OtherBlog.query.filter((OtherBlog.text.contains(searchtext)) | (OtherBlog.title.contains(searchtext)) | (OtherBlog.summary.contains(searchtext))).order_by(OtherBlog.id.desc()).paginate(page=page, per_page=10)
    blog_categories = BlogCategory.query.order_by(BlogCategory.id.asc()).all()
    return render_template('blog/blog_list.html', blogs=blogs, otherblogs=otherblogs, blog_categories=blog_categories, form=form, category_form=category_form, searchtext=searchtext)

#sandboxブログ検索
@blogs.route('/sandbox_blog_search', methods=['GET', 'POST'])
def sandbox_blog_search():
    form = BlogSearchForm()
    category_form = BlogCategoryForm()
    searchtext = ''
    if form.validate_on_submit():
        searchtext = form.searchtext.data
    elif request.method == 'GET':
        form.searchtext.data == ''
    if category_form.validate_on_submit():
        new_category = BlogCategory(category=category_form.category.data)
        db.session.add(new_category)
        db.session.commit()
        flash('カテゴリが追加されました')
        return redirect(url_for('blogs.sandbox_blog_list'))
    page = request.args.get('page', 1, type=int)
    blogs = Blog.query.filter((Blog.text.contains(searchtext)) | (Blog.title.contains(searchtext)) | (Blog.summary.contains(searchtext))).order_by(Blog.id.desc()).paginate(page=page, per_page=10)
    blog_categories = BlogCategory.query.order_by(BlogCategory.id.asc()).all()
    return render_template('blog/blog_list.html', blogs=blogs, blog_categories=blog_categories, form=form, category_form=category_form, searchtext=searchtext)

#お気に入りブログ内検索
@blogs.route('/favorite_blog_search', methods=['GET', 'POST'])
def favorite_blog_search():
    form = BlogSearchForm()
    searchtext = ''
    if form.validate_on_submit():
        searchtext = form.searchtext.data
    elif request.method == 'GET':
        form.searchtext.data == ''
    page = request.args.get('page', 1, type=int)
    blog_categories = BlogCategory.query.order_by(BlogCategory.id.asc()).all()
    favorite_blogs = BlogFavorite.query.filter_by(user_id=current_user.id).all()
    blogs = ''
    if favorite_blogs:
        for favorite_blog in favorite_blogs:
            favorite_all_blogs = Blog.query.filter_by(id=favorite_blog.blog_id).first()
            if favorite_all_blogs:
                blogs = favorite_all_blogs.query.filter((Blog.text.contains(searchtext)) | (Blog.title.contains(searchtext)) | (Blog.summary.contains(searchtext))).order_by(Blog.id.desc()).paginate(page=page, per_page=10)
                return render_template('user/my_page/my_favorite.html', form=form, blog_categories=blog_categories, blogs=blogs, searchtext=searchtext)
    return render_template('user/my_page/my_favorite.html', form=form, blog_categories=blog_categories, blogs=blogs, searchtext=searchtext)

#他サイトブログ検索
@blogs.route('/other_blog_search', methods=['GET', 'POST'])
def other_blog_search():
    form = BlogSearchForm()
    category_form = BlogCategoryForm()
    searchtext = ''
    if form.validate_on_submit():
        searchtext = form.searchtext.data
    elif request.method == 'GET':
        form.searchtext.data == ''
    page = request.args.get('page', 1, type=int)
    otherblogs = OtherBlog.query.filter((OtherBlog.text.contains(searchtext)) | (OtherBlog.title.contains(searchtext)) | (OtherBlog.summary.contains(searchtext))).order_by(OtherBlog.id.desc()).paginate(page=page, per_page=10)
    return render_template('blog/other_blog_list.html', otherblogs=otherblogs, form=form, category_form=category_form, searchtext=searchtext)

#全てのブログでカテゴリ検索
@blogs.route('/<int:blog_category_id>/category_blog', methods=['GET', 'POST'])
def category_blog(blog_category_id):
    form = BlogSearchForm()
    category_form = BlogCategoryForm()
    if category_form.validate_on_submit():
        new_category = BlogCategory(category=category_form.category.data)
        db.session.add(new_category)
        db.session.commit()
        flash('カテゴリが追加されました')
        return redirect(url_for('blogs.blog_list'))
    blog_category = BlogCategory.query.filter_by(id=blog_category_id).first()
    page = request.args.get('page', 1, type=int)
    blogs = Blog.query.filter_by(category_id=blog_category_id).order_by(Blog.id.desc()).paginate(page=page, per_page=5)
    otherblogs = OtherBlog.query.filter_by(category_id=blog_category_id).order_by(OtherBlog.id.desc()).paginate(page=page, per_page=5)
    blog_categories = BlogCategory.query.order_by(BlogCategory.id.asc()).all()
    return render_template('blog/blog_list.html', blogs=blogs, otherblogs=otherblogs, blog_categories=blog_categories, form=form, category_form=category_form, blog_category=blog_category)

#sandboxブログでカテゴリ検索
@blogs.route('/<int:blog_category_id>/sandbox_category_blog', methods=['GET', 'POST'])
def sandbox_category_blog(blog_category_id):
    form = BlogSearchForm()
    category_form = BlogCategoryForm()
    if category_form.validate_on_submit():
        new_category = BlogCategory(category=category_form.category.data)
        db.session.add(new_category)
        db.session.commit()
        flash('カテゴリが追加されました')
        return redirect(url_for('blogs.sandbox_blog_list'))
    blog_category = BlogCategory.query.filter_by(id=blog_category_id).first()
    page = request.args.get('page', 1, type=int)
    blogs = Blog.query.filter_by(category_id=blog_category_id).order_by(Blog.id.desc()).paginate(page=page, per_page=10)
    blog_categories = BlogCategory.query.order_by(BlogCategory.id.asc()).all()
    return render_template('blog/sandbox_blog_list.html', blogs=blogs, blog_categories=blog_categories, form=form, category_form=category_form, blog_category=blog_category)

#他サイトブログでカテゴリ検索
@blogs.route('/<int:blog_category_id>/other_category_blog', methods=['GET', 'POST'])
def other_category_blog(blog_category_id):
    form = BlogSearchForm()
    category_form = BlogCategoryForm()
    if category_form.validate_on_submit():
        new_category = BlogCategory(category=category_form.category.data)
        db.session.add(new_category)
        db.session.commit()
        flash('カテゴリが追加されました')
        return redirect(url_for('blogs.other_blog_list'))
    blog_category = BlogCategory.query.filter_by(id=blog_category_id).first()
    page = request.args.get('page', 1, type=int)
    otherblogs = OtherBlog.query.filter_by(category_id=blog_category_id).order_by(OtherBlog.id.desc()).paginate(page=page, per_page=10)
    blog_categories = BlogCategory.query.order_by(BlogCategory.id.asc()).all()
    return render_template('blog/other_blog_list.html', otherblogs=otherblogs, blog_categories=blog_categories, form=form, category_form=category_form, blog_category=blog_category)

#お気に入りブログでカテゴリ検索
@blogs.route('/<int:blog_category_id>/favorite_category_blog', methods=['GET', 'POST'])
def favorite_category_blog(blog_category_id):
    form = BlogSearchForm()
    blog_category = BlogCategory.query.filter_by(id=blog_category_id).first()
    blog_categories = BlogCategory.query.order_by(BlogCategory.id.asc()).all()
    favorite_blogs = BlogFavorite.query.filter_by(user_id=current_user.id).all()
    page = request.args.get('page', 1, type=int)
    blogs = ''
    if favorite_blogs:
        for favorite_blog in favorite_blogs:
            favorite_all_blogs = Blog.query.filter_by(id=favorite_blog.blog_id).filter_by(category_id=blog_category_id).first()
        blogs = favorite_all_blogs.query.order_by(Blog.id.desc()).paginate(page=page, per_page=10)
        return render_template('user/my_page/my_favorite.html', form=form, blog_categories=blog_categories, blogs=blogs, blog_category=blog_category)
    return render_template('blog/sandbox_blog_list.html', blogs=blogs, blog_categories=blog_categories, form=form, blog_category=blog_category)

#著者検索（sandboxブログ）
@blogs.route('/<int:user_id>/user_blog', methods=['GET', 'POST'])
def user_blog(user_id):
    form = BlogSearchForm()
    category_form = BlogCategoryForm()
    if category_form.validate_on_submit():
        new_category = BlogCategory(category=category_form.category.data)
        db.session.add(new_category)
        db.session.commit()
        flash('カテゴリが追加されました')
        return redirect(url_for('blogs.blog_list'))
    blog_user = Blog.query.filter_by(user_id=user_id).first()
    page = request.args.get('page', 1, type=int)
    blogs = Blog.query.filter_by(user_id=user_id).order_by(Blog.id.desc()).paginate(page=page, per_page=10)
    blog_categories = BlogCategory.query.order_by(BlogCategory.id.asc()).all()
    return render_template('blog/sandbox_blog_list.html', blogs=blogs, blog_categories=blog_categories, form=form, category_form=category_form, blog_user=blog_user)

#ブログお気に入り登録
@blogs.route('/<int:blog_id>/blog_favorite', methods=['GET', 'POST'])
@login_required
def blog_favorite(blog_id):
    favorite_form = BlogFavoriteForm()
    if favorite_form.submit():
        favorite_blog =  BlogFavorite(user_id=current_user.id, blog_id=blog_id)
        db.session.add(favorite_blog)
        db.session.commit()
        flash('ブログがお気に入り登録されました')
        return redirect(url_for('blogs.blog', blog_id=blog_id))
    else:
        abort(403)

#ブログお気に入り削除
@blogs.route('/<int:blog_id>/blog_favorite_delete', methods=['GET', 'POST'])
@login_required
def blog_favorite_delete(blog_id):
    favorite_form = BlogFavoriteForm()
    if favorite_form.submit():
        favorite_blog = BlogFavorite.query.filter_by(user_id=current_user.id, blog_id=blog_id).first()
        db.session.delete(favorite_blog)
        db.session.commit()
        flash('ブログがお気に入りから削除されました')
        return redirect(url_for('blogs.blog', blog_id=blog_id))
    return redirect(url_for('blogs.blog', blog_id=blog_id))

#お気に入り一覧
@blogs.route('/my_favorite_list', methods=['GET', 'POST'])
@login_required
def my_favorite_list():
    form = BlogSearchForm()
    blog_categories = BlogCategory.query.order_by(BlogCategory.id.asc()).all()
    page = request.args.get('page', 1, type=int)
    favorite_blogs = BlogFavorite.query.filter_by(user_id=current_user.id).all()
    blogs = ''
    if favorite_blogs:
        for favorite_blog in favorite_blogs:
            favorite_all_blogs = Blog.query.filter_by(id=favorite_blog.blog_id).first()
        blogs = favorite_all_blogs.query.order_by(Blog.id.desc()).paginate(page=page, per_page=10)
        return render_template('user/my_page/my_favorite.html', form=form, blog_categories=blog_categories, blogs=blogs)
    return render_template('user/my_page/my_favorite.html', form=form, blog_categories=blog_categories, blogs=blogs)

#ブログ管理
@blogs.route('/blog_maintenance')
@login_required
def blog_maintenance():
    if not current_user.is_administrator():
        abort(403)
    page = request.args.get('page', 1, type=int)
    blogs = Blog.query.order_by(Blog.id).paginate(page=page, per_page=10)
    return render_template('maintenance/blog_maintenance.html', blogs=blogs)

#ブログカテゴリ管理
@blogs.route('/category_maintenance')
@login_required
def category_maintenance():
    if not current_user.is_administrator():
        abort(403)
    page = request.args.get('page', 1, type=int)
    categories = BlogCategory.query.order_by(BlogCategory.id).paginate(page=page, per_page=10)
    return render_template('maintenance/category_maintenance.html', categories=categories)
