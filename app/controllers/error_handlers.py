from flask import redirect

def register_error_handlers(app):

    @app.errorhandler(404)
    def page_not_found(e):
        return redirect('/')
    
    @app.errorhandler(500)
    def page_not_found(e):
        return redirect('/')