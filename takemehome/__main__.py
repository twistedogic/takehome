from .app import app, init_db

init_db()

app.run(host="0.0.0.0", port=3000, debug=True)
