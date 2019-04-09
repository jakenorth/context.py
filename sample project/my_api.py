import context
api = context.Api()

@api.push
def fetch_greeting(name):
	return f"Welcome to Context, {name}!"

@api.push
def echo(object):
	return object