#!/usr/bin/env python
# -*- coding=utf-8 -*-

from flask import Blueprint, render_template, request, current_app, redirect, url_for, flash, make_response
from bluelog.models import Post, Comment, Category
from bluelog.forms import CommentForm, AdminCommentForm
from bluelog.emails import send_new_reply_email, send_new_comment_email
from bluelog.extensions import db
from bluelog.utils import redirect_back

blog_bp = Blueprint('blog', __name__)


class Current_user:
    is_authenticated = False

@blog_bp.route('/')
def index():
    page = request.args.get('page', 1, type=int) #查询页数，默认是第一页
    per_page = current_app.config['BLUELOG_POST_PER_PAGE']  #每页博客数量
    pagination = Post.query.order_by(Post.timestamp.desc()).paginate(page, per_page=per_page)  #分页对象
    posts = pagination.items  #当前页数的记录列表
    return render_template('blog/index.html', posts=posts, pagination=pagination)

@blog_bp.route('/about')
def about():
    return render_template('blog/about.html')

@blog_bp.route('/reply/comment/<int:comment_id>')
def reply_comment(comment_id):
    comment = Comment.query.get_or_404(comment_id)
    if not comment.post.can_comment:
        flash('Comment is disabled.', 'warning')
        return redirect(url_for('.show_post', post_id=comment.post.id))
    return redirect(url_for('.show_post', post_id=comment.post_id, reply=comment_id, author=comment.author) + '#comment-form')

#显示某个分类下的所有文章
@blog_bp.route('/category/<int:category_id>')
def show_category(category_id):
    #通过category_id获得某个分类
    category = Category.query.get_or_404(category_id)
    page = request.args.get('page', 1, type=int)  #从查询字符串获取需要查询的页数
    per_page = current_app.config['BLUELOG_POST_PER_PAGE']  #获取每一页的文章数量
    #返回一个分页对象，某个分类下的所有文章
    pagination = Post.query.with_parent(category).order_by(Post.timestamp.desc()).paginate(page, per_page=per_page)
    posts = pagination.items  # items 返回当前页面的记录
    return render_template('blog/category.html', category=category, pagination=pagination, posts=posts)

#展示文章
@blog_bp.route('/post/<int:post_id>', methods=['GET', 'POST'])
def show_post(post_id):
    post = Post.query.get_or_404(post_id)
    page = request.args.get('page', 1, type=int)
    per_page = current_app.config['BLUELOG_POST_PER_PAGE']
    #获取文章的所有评论
    pagination = Comment.query.with_parent(post).filter_by(reviewed=True).order_by(Comment.timestamp.asc()).paginate(page, per_page)
    comments = pagination.items

    if Current_user.is_authenticated:
        form = AdminCommentForm()
        form.author.data = Current_user.name
        form.email.data = current_app.config['BLUELOG_EMAIL']
        form.site.data = url_for('.index')
        from_admin = True
        reviewed = True
    else:
        form = CommentForm()
        from_admin = False
        reviewed = False
    if form.validate_on_submit():
        author = form.author.data
        email = form.email.data
        site = form.site.data
        body = form.body.data
        comment = Comment(author=author, email=email, site=site, body=body, from_admin=from_admin, post=post, reviewed=reviewed)
        replied_id = request.args.get('reply')
        if replied_id:
            replied_comment = Comment.query.get_or_404(replied_id)
            comment.replied = replied_comment
            send_new_reply_email(replied_comment)
        db.session.add(comment)
        db.session.commit()
        if Current_user.is_authenticated:
            flash('Comment published.', 'success')
        else:
            flash('Thanks, your comment will be published after reviewed.', 'info')
            send_new_comment_email(post)
        return redirect(url_for('.show_post', post_id=post_id))
    return render_template('blog/post.html', post=post, pagination=pagination, form=form,  comments=comments) 

@blog_bp.route('/change-theme/<theme_name>')
def change_theme(theme_name):
    if theme_name not in current_app.config['BLUELOG_THEMES']:
        abort(404)
    #手动生成一个响应对象，传入响应主体作为参数
    response = make_response(redirect_back())
    response.set_cookie('theme', theme_name, max_age=30*24*60*60)
    return response



