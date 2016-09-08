""" Basic blog using webpy 0.3 """
import web
import model #import module model.py

### Url mappings - defines urls for the whole website

urls = (
    '/', 'Index',
    '/view/(\d+)', 'View',
    '/new', 'New',
    '/delete/(\d+)', 'Delete',
    '/edit/(\d+)', 'Edit',
)


### Templates
# variable t_globals - something to do with date as string ??? global time
t_globals = {
    'datestr': web.datestr
}

# render templates, third variable is adding globals variable to the templates (in this case t_globals which is a variable where you have a date as a string)
render = web.template.render('templates', base='base', globals=t_globals)

# class - tell python to make a new kind of thing
class Index:
    # function
    def GET(self):
        """ Show page """
        posts = model.get_posts() #variable posts is defined by using get_posts function in model.py
        return render.index(posts) #returns and renders index from posts


class View:

    def GET(self, id):
        """ View single post """
        post = model.get_post(int(id)) #variable post, get post(integer(postid))
        return render.view(post) #render this post

#create new post
class New:

    form = web.form.Form(#variable form defines web form with textbox, textarea and a button
        web.form.Textbox('title', web.form.notnull, 
            size=30,
            description="Post title:"),
        web.form.Textarea('content', web.form.notnull, 
            rows=30, cols=80,
            description="Post content:"),
        web.form.Button('Post entry'),
    )

    def GET(self):
        form = self.form()
        return render.new(form)

    def POST(self):
        form = self.form()
        if not form.validates():
            return render.new(form)
        model.new_post(form.d.title, form.d.content)
        raise web.seeother('/')


class Delete:

    def POST(self, id):
        model.del_post(int(id))
        raise web.seeother('/')


class Edit:

    def GET(self, id):
        post = model.get_post(int(id))
        form = New.form()
        form.fill(post)
        return render.edit(post, form)


    def POST(self, id):
        form = New.form()
        post = model.get_post(int(id))
        if not form.validates():
            return render.edit(post, form)
        model.update_post(int(id), form.d.title, form.d.content)
        raise web.seeother('/')


app = web.application(urls, globals())

if __name__ == '__main__':
    app.run()