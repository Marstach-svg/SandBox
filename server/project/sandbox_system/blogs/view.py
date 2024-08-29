from flask import Blueprint,render_template, url_for, redirect, abort, flash, request
from flask_login import login_required, current_user

from sandbox_system import db
from sandbox_system.models import Blog, BlogCategory, BlogFavorite, OtherBlog, BlogComment
from sandbox_system.blogs.form import BlogForm, BlogCategoryForm, BlogFavoriteForm, OtherBlogForm, BlogCommentForm
from sandbox_system.blogs.image import add_image


blogs = Blueprint('blogs', __name__)


#sandboxブログの一覧ページ
@blogs.route('/sandbox_blog_list', methods=['GET', 'POST'])
def sandbox_blog_list():
    category_form = BlogCategoryForm()
    if category_form.validate_on_submit():
        if current_user.is_authenticated:
            new_category = BlogCategory(category=category_form.category.data)
            db.session.add(new_category)
            db.session.commit()
            flash('カテゴリが追加されました')
            return redirect(url_for('blogs.sandbox_blog_list'))
        else:
            flash('ログインが必要です')
            return redirect(url_for('users.login'))
    if BlogCategory.query.first():
        blog_categories = BlogCategory.query.order_by(BlogCategory.id.asc()).all()
    else:
        blog_categories = ''
    page = request.args.get('page', 1, type=int)
    if Blog.query.first():
        blogs = Blog.query.order_by(Blog.id.desc()).paginate(page=page, per_page=10)
    else:
        blogs = ''
    if OtherBlog.query.first():
        recent_other_blogs = OtherBlog.query.order_by(OtherBlog.id.desc()).limit(3).all()
    else:
        recent_other_blogs = ''
    return render_template('blog/sandbox_blog_list.html', blog_categories=blog_categories, blogs=blogs, category_form=category_form, recent_other_blogs=recent_other_blogs)

#他サイトブログの一覧ページ
@blogs.route('/other_blog_list', methods=['GET', 'POST'])
def other_blog_list():
    category_form = BlogCategoryForm()
    if category_form.validate_on_submit():
        if current_user.is_authenticated:
            new_category = BlogCategory(category=category_form.category.data)
            db.session.add(new_category)
            db.session.commit()
            flash('カテゴリが追加されました')
            return redirect(url_for('blogs.other_blog_list'))
        else:
            flash('ログインが必要です')
            return redirect(url_for('users.login'))
    page = request.args.get('page', 1, type=int)
    if BlogCategory.query.first():
        blog_categories = BlogCategory.query.order_by(BlogCategory.id.asc()).all()
    else:
        blog_categories = ''
    if OtherBlog.query.first():
        otherblogs = OtherBlog.query.order_by(OtherBlog.id.desc()).paginate(page=page, per_page=10)
    else:
        otherblogs = ''
    if Blog.query.first():
        recent_blogs = Blog.query.order_by(Blog.id.desc()).limit(3).all()
    else:
        recent_blogs = ''
    return render_template('blog/other_blog_list.html', otherblogs=otherblogs, blog_categories=blog_categories, category_form=category_form, recent_blogs=recent_blogs)

#お気に入り一覧
@blogs.route('/my_favorite_list', methods=['GET', 'POST'])
@login_required
def my_favorite_list():
    if BlogCategory.query.first():
        blog_categories = BlogCategory.query.order_by(BlogCategory.id.asc()).all()
    else:
        blog_categories = ''
    page = request.args.get('page', 1, type=int)
    if BlogFavorite.query.filter_by(favorite_user_id=current_user.id).first():
        blogs = BlogFavorite.query.filter_by(favorite_user_id=current_user.id).order_by(BlogFavorite.id.desc()).paginate(page=page, per_page=10)
    else:
        blogs = ''
    return render_template('user/my_page/my_favorite.html', blog_categories=blog_categories, blogs=blogs)

#自分のブログ一覧
@blogs.route('/my_blog_list', methods=['GET', 'POST'])
@login_required
def my_blog_list():
    if BlogCategory.query.first():
        blog_categories = BlogCategory.query.order_by(BlogCategory.id.asc()).all()
    else:
        blog_categories = ''
    page = request.args.get('page', 1, type=int)
    if Blog.query.filter_by(user_id=current_user.id).first():
        blogs = Blog.query.filter_by(user_id=current_user.id).order_by(Blog.id.desc()).paginate(page=page, per_page=10)
    else:
        blogs = ''
    return render_template('user/my_page/my_blog.html', blog_categories=blog_categories, blogs=blogs)

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
        return redirect(url_for('blogs.sandbox_blog_list'))
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
@blogs.route('/<int:blog_id>/blog', methods=['GET', 'POST'])
def blog(blog_id):
    blog = Blog.query.get_or_404(blog_id)
    favorite_form = BlogFavoriteForm()
    comment_form = BlogCommentForm()
    if comment_form.validate_on_submit():
        blog_comment = BlogComment(user_id=current_user.id, blog_id=blog_id, comment=comment_form.comment.data)
        db.session.add(blog_comment)
        db.session.commit()
        flash('コメントを投稿しました')
        return redirect(url_for('blogs.blog', blog_id=blog_id))
    if BlogCategory.query.first():
        blog_categories = BlogCategory.query.order_by(BlogCategory.id.asc()).all()
    else:
        blog_categories = ''
    if current_user.is_authenticated:
        if BlogFavorite.query.filter_by(favorite_user_id=current_user.id, blog_id=blog_id).first():
            favorite_blog = BlogFavorite.query.filter_by(favorite_user_id=current_user.id, blog_id=blog_id).first()
        else:
            favorite_blog = ''
    else:
        favorite_blog = ''
    if OtherBlog.query.first():
        recent_other_blogs = OtherBlog.query.order_by(OtherBlog.id.desc()).limit(3).all()
    else:
        recent_other_blogs = ''
    if BlogComment.query.filter_by(blog_id=blog_id).first():
        blog_comments = BlogComment.query.filter_by(blog_id=blog_id).order_by(BlogComment.id.asc()).all()
    else:
        blog_comments = ''
    return render_template('blog/blog.html', blog=blog, favorite_form=favorite_form, blog_categories=blog_categories, blog_id=blog_id, favorite_blog=favorite_blog, recent_other_blogs=recent_other_blogs, comment_form=comment_form, blog_comments=blog_comments)

#ブログ削除
@blogs.route('/<int:blog_id>/delete_blog', methods=['GET', 'POST'])
@login_required
def delete_blog(blog_id):
    blog = Blog.query.get_or_404(blog_id)
    if not blog.author == current_user :
        if not current_user.is_administrator():
            abort(403)
    if BlogFavorite.query.filter_by(blog_id=blog_id).first():
        favorite_blogs = BlogFavorite.query.filter_by(blog_id=blog_id).all()
    else:
        favorite_blogs = ''
    if BlogComment.query.filter_by(blog_id=blog_id).first():
        blog_comments = BlogComment.query.filter_by(blog_id=blog_id).all()
    else:
        blog_comments = ''
    #BlogFavoriteがBlogに外部キーでつながっているため、外部キーエラーを避けるためにBlogFavoriteのデータを先にdeleteしなければならない
    if blog_comments:
        for blog_comment in blog_comments:
            db.session.delete(blog_comment)
            db.session.commit()
    if favorite_blogs:
        for favorite_blog in favorite_blogs:
            db.session.delete(favorite_blog)
            db.session.commit()
    db.session.delete(blog)
    db.session.commit()
    flash('ブログ投稿が削除されました')
    return redirect(url_for('blogs.sandbox_blog_list'))

#他ブログ削除
@blogs.route('/<int:otherblog_id>/delete_other_blog', methods=['GET', 'POST'])
@login_required
def delete_other_blog(otherblog_id):
    otherblog = OtherBlog.query.get_or_404(otherblog_id)
    if not current_user.is_administrator():
        abort(403)
    db.session.delete(otherblog)
    db.session.commit()
    flash('ブログ投稿が削除されました')
    return redirect(url_for('blogs.other_blog_list'))

#ブログ編集
@blogs.route('/<int:blog_id>/blog_update', methods=['GET', 'POST'])
@login_required
def blog_update(blog_id):
    form = BlogForm()
    blog = Blog.query.get_or_404(blog_id)
    if not blog.author == current_user:
        if not current_user.is_administrator():
            abort(403)
    if form.validate_on_submit():
        blog.title = form.title.data
        if form.picture.data:
            blog.image = add_image(form.picture.data)
        blog.catagory_id = form.category.data
        blog.text = form.text.data
        blog.summary = form.summary.data
        db.session.commit()
        flash('ブログ投稿が更新されました')
        return redirect(url_for('blogs.blog', blog_id=blog.id))
    elif request.method == 'GET':
        form.title.data = blog.title
        form.picture.data = blog.image
        form.category.data = blog.category_id
        form.text.data = blog.text
        form.summary.data = blog.summary
    return render_template('blog/blog_update.html', form=form)

#ブログカテゴリ削除
@blogs.route('/<int:category_id>/delete_category', methods=['GET', 'POST'])
@login_required
def delete_category(category_id):
    if Blog.query.filter_by(category_id=category_id).first():
        flash('このカテゴリはブログに登録されているため削除できません')
        return redirect(url_for('blogs.sandbox_blog_list'))
    else:
        category = BlogCategory.query.get_or_404(category_id)
        db.session.delete(category)
        db.session.commit()
        flash('カテゴリが削除されました')
        return redirect(url_for('blogs.sandbox_blog_list'))

#ブログコメント削除
@blogs.route('/<int:blog_id>/<int:comment_id>/<int:user_id>/delete_comment', methods=['GET', 'POST'])
@login_required
def delete_comment(blog_id, comment_id, user_id):
    if not current_user.id == user_id :
        if not current_user.is_administrator():
            abort(403)
    comment = BlogComment.query.get_or_404(comment_id)
    db.session.delete(comment)
    db.session.commit()
    flash('コメントが削除されました')
    return redirect(url_for('blogs.blog', blog_id=blog_id))

#sandboxブログ検索
@blogs.route('/sandbox_blog_search', methods=['GET', 'POST'])
def sandbox_blog_search():
    category_form = BlogCategoryForm()
    if request.form.get('sandbox_blog_search'):
        searchtext = request.form.get('sandbox_blog_search')
    else:
        searchtext = ''
    if category_form.validate_on_submit():
        new_category = BlogCategory(category=category_form.category.data)
        db.session.add(new_category)
        db.session.commit()
        flash('カテゴリが追加されました')
        return redirect(url_for('blogs.sandbox_blog_list'))
    page = request.args.get('page', 1, type=int)
    if Blog.query.filter((Blog.text.contains(searchtext)) | (Blog.title.contains(searchtext)) | (Blog.summary.contains(searchtext))).first():
        blogs = Blog.query.filter((Blog.text.contains(searchtext)) | (Blog.title.contains(searchtext)) | (Blog.summary.contains(searchtext))).order_by(Blog.id.desc()).paginate(page=page, per_page=10)
    else:
        blogs = ''
    if BlogCategory.query.first():
        blog_categories = BlogCategory.query.order_by(BlogCategory.id.asc()).all()
    else:
        blog_categories = ''
    if OtherBlog.query.first():
        recent_other_blogs = OtherBlog.query.order_by(OtherBlog.id.desc()).limit(3).all()
    else:
        recent_other_blogs = ''
    return render_template('blog/sandbox_blog_list.html', blogs=blogs, blog_categories=blog_categories, category_form=category_form, searchtext=searchtext, recent_other_blogs=recent_other_blogs)

#他サイトブログ検索
@blogs.route('/other_blog_search', methods=['GET', 'POST'])
def other_blog_search():
    category_form = BlogCategoryForm()
    if category_form.validate_on_submit():
        new_category = BlogCategory(category=category_form.category.data)
        db.session.add(new_category)
        db.session.commit()
        flash('カテゴリが追加されました')
        return redirect(url_for('blogs.other_blog_list'))
    searchtext = ''
    if request.form.get('other_blog_search'):
        searchtext = request.form.get('other_blog_search')
    else:
        searchtext = ''
    page = request.args.get('page', 1, type=int)
    if OtherBlog.query.filter((OtherBlog.text.contains(searchtext)) | (OtherBlog.title.contains(searchtext)) | (OtherBlog.summary.contains(searchtext))).first():
        otherblogs = OtherBlog.query.filter((OtherBlog.text.contains(searchtext)) | (OtherBlog.title.contains(searchtext)) | (OtherBlog.summary.contains(searchtext))).order_by(OtherBlog.id.desc()).paginate(page=page, per_page=10)
    else:
        otherblogs = ''
    if BlogCategory.query.first():
        blog_categories = BlogCategory.query.order_by(BlogCategory.id.asc()).all()
    else:
        blog_categories = ''
    if Blog.query.first():
        recent_blogs = Blog.query.order_by(Blog.id.desc()).limit(3).all()
    else:
        recent_blogs = ''
    return render_template('blog/other_blog_list.html', otherblogs=otherblogs, category_form=category_form, searchtext=searchtext, blog_categories=blog_categories, recent_blogs=recent_blogs)

#お気に入りブログ内検索
@blogs.route('/favorite_blog_search', methods=['GET', 'POST'])
@login_required
def favorite_blog_search():
    if request.form.get('favorite_blog_search'):
        searchtext = request.form.get('favorite_blog_search')
    else:
        searchtext = ''
    page = request.args.get('page', 1, type=int)
    if BlogCategory.query.first():
        blog_categories = BlogCategory.query.order_by(BlogCategory.id.asc()).all()
    else:
        blog_categories = ''
    if BlogFavorite.query.filter_by(favorite_user_id=current_user.id).first():
        blogs = BlogFavorite.query.filter_by(favorite_user_id=current_user.id).filter((BlogFavorite.text.contains(searchtext)) | (BlogFavorite.title.contains(searchtext)) | (BlogFavorite.summary.contains(searchtext))).order_by(BlogFavorite.id.desc()).paginate(page=page, per_page=10)
    else:
        blogs = ''
    return render_template('user/my_page/my_favorite.html', blog_categories=blog_categories, blogs=blogs, searchtext=searchtext)

#自分のブログ内検索
@blogs.route('/my_blog_search', methods=['GET', 'POST'])
def my_blog_search():
    if request.form.get('my_blog_search'):
        searchtext = request.form.get('my_blog_search')
    else:
        searchtext = ''
    page = request.args.get('page', 1, type=int)
    if BlogCategory.query.first():
        blog_categories = BlogCategory.query.order_by(BlogCategory.id.asc()).all()
    else:
        blog_categories = ''
    if Blog.query.filter_by(user_id=current_user.id).first():
        blogs = Blog.query.filter_by(user_id=current_user.id).filter((Blog.text.contains(searchtext)) | (Blog.title.contains(searchtext)) | (Blog.summary.contains(searchtext))).order_by(Blog.id.desc()).paginate(page=page, per_page=10)
    else:
        blogs = ''
    return render_template('user/my_page/my_blog.html', blog_categories=blog_categories, blogs=blogs, searchtext=searchtext)

#sandboxブログでカテゴリ検索
@blogs.route('/<int:blog_category_id>/sandbox_category_blog', methods=['GET', 'POST'])
def sandbox_category_blog(blog_category_id):
    category_form = BlogCategoryForm()
    if category_form.validate_on_submit():
        new_category = BlogCategory(category=category_form.category.data)
        db.session.add(new_category)
        db.session.commit()
        flash('カテゴリが追加されました')
        return redirect(url_for('blogs.sandbox_blog_list'))
    blog_category = BlogCategory.query.filter_by(id=blog_category_id).first()
    page = request.args.get('page', 1, type=int)
    if Blog.query.filter_by(category_id=blog_category_id).first():
        blogs = Blog.query.filter_by(category_id=blog_category_id).order_by(Blog.id.desc()).paginate(page=page, per_page=10)
    else:
        blogs = ''
    blog_categories = BlogCategory.query.order_by(BlogCategory.id.asc()).all()
    if OtherBlog.query.first():
        recent_other_blogs = OtherBlog.query.order_by(OtherBlog.id.desc()).limit(3).all()
    else:
        recent_other_blogs = ''
    return render_template('blog/sandbox_blog_list.html', blogs=blogs, blog_categories=blog_categories, category_form=category_form, blog_category=blog_category, recent_other_blogs=recent_other_blogs)

#他サイトブログでカテゴリ検索
@blogs.route('/<int:blog_category_id>/other_category_blog', methods=['GET', 'POST'])
def other_category_blog(blog_category_id):
    category_form = BlogCategoryForm()
    if category_form.validate_on_submit():
        new_category = BlogCategory(category=category_form.category.data)
        db.session.add(new_category)
        db.session.commit()
        flash('カテゴリが追加されました')
        return redirect(url_for('blogs.other_blog_list'))
    blog_category = BlogCategory.query.filter_by(id=blog_category_id).first()
    page = request.args.get('page', 1, type=int)
    if OtherBlog.query.filter_by(category_id=blog_category_id).first():
        otherblogs = OtherBlog.query.filter_by(category_id=blog_category_id).order_by(OtherBlog.id.desc()).paginate(page=page, per_page=10)
    else:
        otherblogs = ''
    blog_categories = BlogCategory.query.order_by(BlogCategory.id.asc()).all()
    if Blog.query.first():
        recent_blogs = Blog.query.order_by(Blog.id.desc()).limit(3).all()
    else:
        recent_blogs = ''
    return render_template('blog/other_blog_list.html', otherblogs=otherblogs, blog_categories=blog_categories, category_form=category_form, blog_category=blog_category, recent_blogs=recent_blogs)

#お気に入りブログでカテゴリ検索
@blogs.route('/<int:blog_category_id>/favorite_category_blog', methods=['GET', 'POST'])
@login_required
def favorite_category_blog(blog_category_id):
    blog_category = BlogCategory.query.filter_by(id=blog_category_id).first()
    blog_categories = BlogCategory.query.order_by(BlogCategory.id.asc()).all()
    page = request.args.get('page', 1, type=int)
    if BlogFavorite.query.filter_by(favorite_user_id=current_user.id).first():
        blogs = BlogFavorite.query.filter_by(favorite_user_id=current_user.id).filter_by(category_id=blog_category_id).order_by(BlogFavorite.id.desc()).paginate(page=page, per_page=10)
    else:
        blogs = ''
    return render_template('user/my_page/my_favorite.html', blogs=blogs, blog_categories=blog_categories, blog_category=blog_category)

#自分のブログでカテゴリ検索
@blogs.route('/<int:blog_category_id>/my_category_blog', methods=['GET', 'POST'])
def my_category_blog(blog_category_id):
    blog_category = BlogCategory.query.filter_by(id=blog_category_id).first()
    blog_categories = BlogCategory.query.order_by(BlogCategory.id.asc()).all()
    page = request.args.get('page', 1, type=int)
    if Blog.query.filter_by(user_id=current_user.id).first():
        blogs = Blog.query.filter_by(user_id=current_user.id).filter_by(category_id=blog_category_id).order_by(Blog.id.desc()).paginate(page=page, per_page=10)
    else:
        blogs = ''
    return render_template('user/my_page/my_blog.html', blogs=blogs, blog_categories=blog_categories, blog_category=blog_category)

#著者検索（sandboxブログ）
@blogs.route('/<int:user_id>/user_blog', methods=['GET', 'POST'])
def user_blog(user_id):
    category_form = BlogCategoryForm()
    if category_form.validate_on_submit():
        new_category = BlogCategory(category=category_form.category.data)
        db.session.add(new_category)
        db.session.commit()
        flash('カテゴリが追加されました')
        return redirect(url_for('blogs.blog_list'))
    if Blog.query.filter_by(user_id=user_id).first():
        blog_user = Blog.query.filter_by(user_id=user_id).first()
    else:
        blog_user = ''
    page = request.args.get('page', 1, type=int)
    if Blog.query.filter_by(user_id=user_id).first():
        blogs = Blog.query.filter_by(user_id=user_id).order_by(Blog.id.desc()).paginate(page=page, per_page=10)
    else:
        blogs = ''
    if BlogCategory.query.first():
        blog_categories = BlogCategory.query.order_by(BlogCategory.id.asc()).all()
    else:
        blog_categories = ''
    if OtherBlog.query.first():
        recent_other_blogs = OtherBlog.query.order_by(OtherBlog.id.desc()).limit(3).all()
    else:
        recent_other_blogs = ''
    return render_template('blog/sandbox_blog_list.html', blogs=blogs, blog_categories=blog_categories, category_form=category_form, blog_user=blog_user, recent_other_blogs=recent_other_blogs)

#ブログお気に入り登録
@blogs.route('/<int:blog_id>/blog_favorite', methods=['GET', 'POST'])
@login_required
def blog_favorite(blog_id):
    blog = Blog.query.get_or_404(blog_id)
    favorite_form = BlogFavoriteForm()
    if favorite_form.submit():
        favorite_blog =  BlogFavorite(title=blog.title, summary=blog.summary, text=blog.text, image=blog.image, blog_id=blog_id, favorite_user_id=current_user.id, category_id=blog.category_id)
        db.session.add(favorite_blog)
        db.session.commit()
        flash('ブログがお気に入りに登録されました')
        return redirect(url_for('blogs.blog', blog_id=blog_id))
    else:
        abort(403)

#ブログお気に入り削除
@blogs.route('/<int:blog_id>/blog_favorite_delete', methods=['GET', 'POST'])
@login_required
def blog_favorite_delete(blog_id):
    favorite_form = BlogFavoriteForm()
    if favorite_form.submit():
        favorite_blog = BlogFavorite.query.filter_by(favorite_user_id=current_user.id, blog_id=blog_id).first()
        db.session.delete(favorite_blog)
        db.session.commit()
        flash('ブログがお気に入りから削除されました')
        return redirect(url_for('blogs.blog', blog_id=blog_id))
    return redirect(url_for('blogs.blog', blog_id=blog_id))

#sandboxブログ管理
@blogs.route('/sandbox_blog_maintenance')
@login_required
def sandbox_blog_maintenance():
    if not current_user.is_administrator():
        abort(403)
    page = request.args.get('page', 1, type=int)
    if Blog.query.first():
        blogs = Blog.query.order_by(Blog.id).paginate(page=page, per_page=10)
    else:
        blogs = ''
    return render_template('maintenance/sandbox_blog_maintenance.html', blogs=blogs)

#他ブログ管理
@blogs.route('/other_blog_maintenance')
@login_required
def other_blog_maintenance():
    if not current_user.is_administrator():
        abort(403)
    page = request.args.get('page', 1, type=int)
    if OtherBlog.query.first():
        otherblogs = OtherBlog.query.order_by(OtherBlog.id).paginate(page=page, per_page=10)
    else:
        otherblogs = ''
    return render_template('maintenance/other_blog_maintenance.html', otherblogs=otherblogs)

#ブログカテゴリ管理
@blogs.route('/category_maintenance')
@login_required
def category_maintenance():
    if not current_user.is_administrator():
        abort(403)
    page = request.args.get('page', 1, type=int)
    if BlogCategory.query.first():
        categories = BlogCategory.query.order_by(BlogCategory.id).paginate(page=page, per_page=10)
    else:
        categories = ''
    return render_template('maintenance/category_maintenance.html', categories=categories)
