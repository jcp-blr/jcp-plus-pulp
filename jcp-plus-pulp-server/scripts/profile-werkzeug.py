from werkzeug.contrib.profiler import ProfilerMiddleware
from jcp_plus_pulp_server import app

app.config["PROFILE"] = True
app.wsgi_app = ProfilerMiddleware(app.wsgi_app, restrictions=[30])
app.run(debug=True)
