from flask import *
import json

class Api:
	funcs = {}
	def push(self, function):
		name = function.__name__
		self.funcs[name] = function

depend = """<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.3.1/jquery.min.js"></script>
<script>function kw(pairs) {
	return ["keyword", pairs];
}
</script>
"""

def make_js_func_tag(funcname):
	return """<script>function @funcname(...args) {
		query = "/api/@funcname/" + JSON.stringify(args);
		return new Promise((resolve, reject) => {$.get(query, resp => resolve(JSON.parse(resp)))});
	}</script>""".replace("@funcname", funcname)

def make_func_tags(f_dict):
	out = depend
	for key in f_dict.keys():
		out += make_js_func_tag(key)
	return(out)

class ContextApp:
	root = "www"
	api = Api()
	flask_app = Flask(__name__)
	def __init__(self):
		@self.flask_app.route("/api/<funcname>/")
		def api_call(funcname):
			print("calling niladic " + funcname)
			return json.dumps(self.api.funcs[funcname]())
		@self.flask_app.route("/api/<funcname>/<data>")
		def api_call_w_data(funcname, data):
			print(f"calling function {funcname} with {data}")

			data_all = json.loads(data)
			data_positional = [x for x in data_all if not (isinstance(x, list) and len(x) == 2 and x[0] == "keyword")]
			data_keyword_doubles = [x for x in data_all if (isinstance(x, list) and len(x) == 2 and x[0] == "keyword")]
			data_keyword = {}
			for double in data_keyword_doubles:
				data_keyword = {**double[1], **data_keyword}
			return json.dumps(self.api.funcs[funcname](*data_positional, **data_keyword))
		@self.flask_app.route("/<path:path>", methods=['POST', 'GET'])
		@self.flask_app.route("/", methods=['POST', 'GET'])
		def flask_www_router(path="/"):
			try:
				if path.endswith(".html"):
					return make_func_tags(self.api.funcs) + request_data_string(request) + open(self.root + "/" + path).read()
				else:
					extention = path.split(".")[-1]
					mimemap = {
						"txt":"text",
						"js":"text/javascript",
						"css":"text/css",
						"md":"text",
						"jpeg":"image/jpeg",
						"jpg":"image/jpg",
						"png":"image/png",
						"gif":"image/gif",
						}
					return send_file(self.root+"/"+path,mimetype=mimemap[extention])
			except:
				if not path.endswith("index.html"):
					return redirect("/" + path + "/index.html")
			return "uncaught error"
	def start(self, host="localhost", port=5000):
		self.flask_app.run(host=host, port=port)