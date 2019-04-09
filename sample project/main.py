import context
import my_api

app = context.ContextApp()
app.root = "www"
app.api = my_api.api

app.start()